from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from projeto_aplicado.auth.password import verify_password
from projeto_aplicado.auth.security import create_access_token
from projeto_aplicado.resources.users.repository import (
    UserRepository,
    get_user_repository,
)

router = APIRouter(tags=['Token'], prefix='/token')

user_repository_dep = Annotated[UserRepository, Depends(get_user_repository)]


def validate_user_credentials(user_repository, username, password):
    user = user_repository.get_by_email(username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    return user


@router.post('/')
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: user_repository_dep,
):
    user = validate_user_credentials(
        user_repository, form_data.username, form_data.password
    )
    access_token = create_access_token(data={'sub': user.email})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }
