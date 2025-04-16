from http import HTTPStatus
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates

# from projeto_aplicado.ext.cache.redis import get_many
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

templates = Jinja2Templates(
    directory='templates',
    auto_reload=True,
    cache_size=0,
)


router = APIRouter(tags=['Category'], prefix='/categories')

CategoryRepo = Annotated[CategoryRepository, Depends(get_category_repository)]


@router.get('/', response_model=list[Category])
def get_categories(
    request: Request,
    repository: CategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """
    Get all categories.

    """

    # cache = get_many('categories')

    # if cache:
    #     return cache

    categories = repository.get_all(offset=offset, limit=limit)

    if hx_request:
        return templates.TemplateResponse(
            request, 'categories.html', context={'categories': categories}
        )

    return categories


@router.get('/{category_id}', response_model=Category)
def get_category_by_id(category_id: str, repository: CategoryRepo):
    """
    Get a category by ID.
    """
    category = repository.get_by_id(category_id)

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Category with {category_id} not found',
        )

    return category


@router.post('/', response_model=BaseResponse)
def create_category(
    request: Request,
    data: CreateCategoryDTO,
    repository: CategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
):
    """
    Create a new category.
    """

    existing_category = repository.get_by_name(data.name)

    if existing_category:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Category already exists',
        )

    new_category = Category(name=data.name, icon_url=data.icon_url)
    repository.create(new_category)

    return {
        'id': new_category.id,
        'action': 'created',
    }


@router.patch('/{category_id}', response_model=BaseResponse)
def update_category(
    category_id: str, dto: UpdateCategoryDTO, repository: CategoryRepo
):
    """
    Update a category by ID.
    """

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


@router.delete('/{category_id}', response_model=BaseResponse)
def delete_category(category_id: str, repository: CategoryRepo):
    """
    Delete a category by ID.
    """

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
