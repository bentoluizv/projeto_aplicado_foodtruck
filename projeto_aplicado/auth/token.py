from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from projeto_aplicado.auth.security import (
    create_access_token,
    verify_password,
)
from projeto_aplicado.resources.users.repository import (
    UserRepository,
    get_user_repository,
)

router = APIRouter(tags=['Token'], prefix='/token')

user_repository_dep = Annotated[UserRepository, Depends(get_user_repository)]


@router.post('/')
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Security()],
    user_repository: user_repository_dep,
):
    user = user_repository.get_by_email(form_data.username)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    access_token = create_access_token(data={'sub': user.email})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }
