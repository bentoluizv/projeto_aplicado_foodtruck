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
from projeto_aplicado.settings import get_settings

settings = get_settings()
router = APIRouter(tags=['Token'], prefix=f'{settings.API_PREFIX}/token')

user_repository_dep = Annotated[UserRepository, Depends(get_user_repository)]


def validate_user_credentials(user_repository, username, password):
    user = user_repository.get_by_email(username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    return user


@router.post(
    '/',
    responses={
        200: {
            'description': 'Token gerado com sucesso',
            'content': {
                'application/json': {
                    'example': {
                        'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                        'token_type': 'bearer',
                    }
                }
            },
        },
        401: {
            'description': 'Credenciais inválidas',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Incorrect email or password',
                    }
                }
            },
        },
        429: {
            'description': 'Muitas tentativas de login',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Too many login attempts. Please try again later.',
                    }
                }
            },
            'headers': {
                'Retry-After': {
                    'description': 'Seconds to wait before retrying',
                    'schema': {'type': 'integer'},
                }
            },
        },
    },
)
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: user_repository_dep,
):
    """
    Gera um token de acesso JWT para autenticação.

    Args:
        form_data (OAuth2PasswordRequestForm): Dados de login (email e senha).
        user_repository (UserRepository): Repositório de usuários.

    Returns:
        dict: Token de acesso e tipo do token.

    Raises:
        HTTPException:
            - Se as credenciais forem inválidas (401)
            - Se houver muitas tentativas de login (429)

    Examples:
        ```python
        # Exemplo de requisição
        response = await client.post(
            '/api/v1/token',
            data={
                'username': 'user@example.com',
                'password': 'secure_password123'
            }
        )

        # Exemplo de resposta (200 OK)
        {
            'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
            'token_type': 'bearer'
        }

        # Exemplo de resposta (401 Unauthorized)
        {
            'detail': 'Incorrect email or password'
        }

        # Exemplo de resposta (429 Too Many Requests)
        {
            'detail': 'Too many login attempts. Please try again later.'
        }
        ```
    """
    user = validate_user_credentials(
        user_repository, form_data.username, form_data.password
    )
    access_token = create_access_token(data={'sub': user.email})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }
