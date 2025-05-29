from datetime import datetime, timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode

from projeto_aplicado.resources.user.repository import (
    UserRepository,
    get_user_repository,
)
from projeto_aplicado.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_PREFIX}/token',
    auto_error=True,
    scopes={
        'admin': 'Admin access',
        'kitchen': 'Kitchen access',
        'attendant': 'Attendant access',
    },
)
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def create_access_token(data: dict):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    user_repository: UserRepositoryDep,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get('sub')

        if email is None:
            raise credentials_exception

        user = user_repository.get_by_email(email)

        if user is None:
            raise credentials_exception

        return user
    except PyJWTError:
        raise credentials_exception
