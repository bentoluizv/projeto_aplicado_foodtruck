from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from projeto_aplicado.models.entities import Category
from projeto_aplicado.models.schemas import (
    BaseResponse,
    CreateCategoryDTO,
    UpdateCategoryDTO,
)
from projeto_aplicado.repositories.category_repository import (
    CategoryRepository,
    get_category_repository,
)

router = APIRouter(tags=['Category'], prefix='/categories')

CategoryRepo = Annotated[CategoryRepository, Depends(get_category_repository)]


@router.get('/', response_model=list[Category])
def get_categories(
    repository: CategoryRepo,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """
    Get all categories.

    """
    try:
        categories = repository.get_all(offset=offset, limit=limit)

        return categories

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Error retrieving categories: {str(e)}',
        )


@router.get('/{category_id}', response_model=Category)
def get_category_by_id(category_id: str, repository: CategoryRepo):
    """
    Get a category by ID.
    """
    try:
        category = repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Category not found',
            )

        return category

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Error retrieving category: {str(e)}',
        )


@router.post('/', response_model=BaseResponse)
def create_category(data: CreateCategoryDTO, repository: CategoryRepo):
    """
    Create a new category.
    """
    try:
        existing_category = repository.get_by_name(data.name)

        if existing_category:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Category already exists',
            )

        new_category = Category(name=data.name)

        repository.create(new_category)

        return {
            'id': new_category.id,
            'action': 'created',
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Error creating category: {str(e)}',
        )


@router.patch('/{category_id}', response_model=BaseResponse)
def update_category(
    category_id: str, dto: UpdateCategoryDTO, repository: CategoryRepo
):
    """
    Update a category by ID.
    """
    try:
        existing_category = repository.get_by_id(category_id)

        if not existing_category:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Category not found',
            )

        repository.update(existing_category, dto)

        return {
            'id': existing_category.id,
            'action': 'updated',
        }

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Error updating category: {str(e)}',
        )


@router.delete('/{category_id}', response_model=BaseResponse)
def delete_category(category_id: str, repository: CategoryRepo):
    """
    Delete a category by ID.
    """
    try:
        existing_category = repository.get_by_id(category_id)

        if not existing_category:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Category not found',
            )
        repository.delete(existing_category)

        return {
            'id': existing_category.id,
            'action': 'deleted',
        }

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Error deleting category: {str(e)}',
        )
