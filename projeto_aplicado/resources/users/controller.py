from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from projeto_aplicado.auth.security import get_current_user
from projeto_aplicado.resources.shared.schemas import Pagination
from projeto_aplicado.resources.users.model import User, UserRole
from projeto_aplicado.resources.users.repository import (
    UserRepository,
    get_user_repository,
)
from projeto_aplicado.resources.users.schemas import (
    CreateUserDTO,
    UpdateUserDTO,
    UserList,
    UserOut,
)
from projeto_aplicado.settings import get_settings

settings = get_settings()
UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
router = APIRouter(tags=['User'], prefix=f'{settings.API_PREFIX}/users')
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/',
    response_model=UserList,
    status_code=HTTPStatus.OK,
    responses={
        200: {
            'description': 'Lista de usuários retornada com sucesso',
            'content': {
                'application/json': {
                    'example': {
                        'items': [
                            {
                                'id': '1',
                                'name': 'Admin User',
                                'email': 'admin@example.com',
                                'role': 'admin',
                                'created_at': '2024-03-20T10:00:00',
                                'updated_at': '2024-03-20T10:00:00',
                            },
                            {
                                'id': '2',
                                'name': 'Attendant User',
                                'email': 'attendant@example.com',
                                'role': 'attendant',
                                'created_at': '2024-03-20T10:00:00',
                                'updated_at': '2024-03-20T10:00:00',
                            },
                        ],
                        'pagination': {
                            'offset': 0,
                            'limit': 100,
                            'total_count': 2,
                            'total_pages': 1,
                            'page': 1,
                        },
                    }
                }
            },
        },
        401: {
            'description': 'Não autorizado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Not authenticated',
                    }
                }
            },
        },
        403: {
            'description': 'Acesso negado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'You are not allowed to fetch users',
                    }
                }
            },
        },
    },
)
def fetch_users(
    repository: UserRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retorna a lista de usuários do sistema.

    Args:
        repository (UserRepository): Repositório de usuários.
        current_user (User): Usuário autenticado.
        offset (int, optional): Número de registros para pular. Padrão: 0.
        limit (int, optional): Limite de registros por página. Padrão: 100.

    Returns:
        UserList: Lista de usuários com informações de paginação.

    Raises:
        HTTPException:
            - Se o usuário não estiver autenticado (401)
            - Se o usuário não tiver permissão (403)

    Examples:
        ```python
        # Exemplo de requisição
        response = await client.get(
            '/api/v1/users',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
        )

        # Exemplo de resposta (200 OK)
        {
            'items': [
                {
                    'id': '1',
                    'name': 'Admin User',
                    'email': 'admin@example.com',
                    'role': 'admin',
                    'created_at': '2024-03-20T10:00:00',
                    'updated_at': '2024-03-20T10:00:00'
                }
            ],
            'pagination': {
                'offset': 0,
                'limit': 100,
                'total_count': 1,
                'total_pages': 1,
                'page': 1
            }
        }
        ```
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to fetch users',
        )

    users = repository.get_all(offset=offset, limit=limit)
    total_count = repository.get_total_count()
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
    page = (offset // limit) + 1 if limit > 0 else 1
    return UserList(
        items=[
            UserOut(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ],
        pagination=Pagination(
            offset=offset,
            limit=limit,
            total_count=total_count,
            total_pages=total_pages,
            page=page,
        ),
    )


@router.get('/{user_id}', response_model=UserOut)
def fetch_user_by_id(
    user_id: str,
    repository: UserRepo,
    current_user: CurrentUser,
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to fetch users',
        )

    user = repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post(
    '/',
    response_model=UserOut,
    status_code=HTTPStatus.CREATED,
    responses={
        201: {
            'description': 'Usuário criado com sucesso',
            'content': {
                'application/json': {
                    'example': {
                        'id': '3',
                        'name': 'New User',
                        'email': 'new@example.com',
                        'role': 'attendant',
                        'created_at': '2024-03-20T10:00:00',
                        'updated_at': '2024-03-20T10:00:00',
                    }
                }
            },
        },
        400: {
            'description': 'Dados inválidos',
            'content': {
                'application/json': {
                    'examples': {
                        'invalid_email': {
                            'value': {'detail': 'Invalid email format'},
                            'summary': 'Email inválido',
                        },
                        'weak_password': {
                            'value': {'detail': 'Password is too weak'},
                            'summary': 'Senha fraca',
                        },
                    }
                }
            },
        },
        401: {
            'description': 'Não autorizado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Not authenticated',
                    }
                }
            },
        },
        403: {
            'description': 'Acesso negado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'You are not allowed to create users',
                    }
                }
            },
        },
        409: {
            'description': 'Conflito',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Email already registered',
                    }
                }
            },
        },
    },
)
def create_user(
    dto: CreateUserDTO,
    repository: UserRepo,
    current_user: CurrentUser,
):
    """
    Cria um novo usuário no sistema.

    Args:
        dto (CreateUserDTO): Dados do usuário a ser criado.
        repository (UserRepository): Repositório de usuários.
        current_user (User): Usuário autenticado.

    Returns:
        UserOut: Dados do usuário criado.

    Raises:
        HTTPException:
            - Se os dados forem inválidos (400)
            - Se o usuário não estiver autenticado (401)
            - Se o usuário não tiver permissão (403)
            - Se o email já estiver registrado (409)

    Examples:
        ```python
        # Exemplo de requisição
        response = await client.post(
            '/api/v1/users',
            json={
                'name': 'New User',
                'email': 'new@example.com',
                'password': 'secure_password123',
                'role': 'attendant'
            },
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
        )

        # Exemplo de resposta (201 Created)
        {
            'id': '3',
            'name': 'New User',
            'email': 'new@example.com',
            'role': 'attendant',
            'created_at': '2024-03-20T10:00:00',
            'updated_at': '2024-03-20T10:00:00'
        }
        ```
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to create users',
        )

    user = User(**dto.model_dump())
    repository.create(user)
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.patch('/{user_id}', response_model=UserOut)
def update_user(
    user_id: str,
    dto: UpdateUserDTO,
    repository: UserRepo,
    current_user: CurrentUser,
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to update users',
        )

    user = repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    repository.update(user, dto)
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.delete('/{user_id}', status_code=HTTPStatus.OK)
def delete_user(
    user_id: str,
    repository: UserRepo,
    current_user: CurrentUser,
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to delete users',
        )

    user = repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    repository.delete(user)
    return {'action': 'deleted', 'id': user_id}
