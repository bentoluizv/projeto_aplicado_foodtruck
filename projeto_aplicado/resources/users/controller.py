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


@router.get('/', response_model=UserList, status_code=HTTPStatus.OK)
def fetch_users(
    repository: UserRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
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
        items=[  # type: ignore
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


@router.post('/', response_model=UserOut, status_code=HTTPStatus.CREATED)
def create_user(
    dto: CreateUserDTO,
    repository: UserRepo,
    current_user: CurrentUser,
):
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
