from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Query,
)

from projeto_aplicado.resources.category.model import Category
from projeto_aplicado.resources.category.repository import (
    CategoryRepository,
    get_category_repository,
)
from projeto_aplicado.resources.category.schemas import (
    CategoryList,
    UpdateCategoryDTO,
)
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.schemas import BaseResponse
from projeto_aplicado.settings import get_settings

settings = get_settings()

router = APIRouter(
    tags=['Category'], prefix=f'{settings.API_PREFIX}/categories'
)

CategoryRepo = Annotated[CategoryRepository, Depends(get_category_repository)]


@router.get('/', response_model=CategoryList, status_code=HTTPStatus.OK)
def get_categories(
    repository: CategoryRepo,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """
    Retrieve a list of categories with optional pagination.
    Args:
        repository (CategoryRepo): The repository instance to fetch categories from.
        offset (int, optional): The starting point for fetching categories. Defaults to 0.
        limit (int, optional): The maximum number of categories to fetch, with a
            default of 100 and a maximum of 100.
    Returns:
        CategoryList: A list of categories with pagination information.
    """
    categories = repository.get_all(offset=offset, limit=limit)
    return categories


@router.get('/{category_id}', response_model=Category)
def get_category_by_id(
    category_id: str,
    repository: CategoryRepo,
):
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


@router.get('/{category_id}/products', response_model=list[Product])
def get_products_by_category(
    category_id: str,
    repository: CategoryRepo,
):
    """
    Get products by category ID.
    """
    category = repository.get_by_id(category_id)

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Category with {category_id} not found',
        )

    return category.products


@router.post(
    '/',
    response_model=BaseResponse,
    status_code=HTTPStatus.CREATED,
)
def create_category(
    icon_url: Annotated[str, Form()],
    name: Annotated[str, Form()],
    repository: CategoryRepo,
):
    """
    Create a new category.
    """
    existing_category = repository.get_by_name(name)

    if existing_category:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Category already exists',
        )

    if icon_url == 'undefined':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Icon URL is required',
        )

    new_category = Category(name=name, icon_url=icon_url)
    repository.create(new_category)

    return BaseResponse(id=new_category.id, action='created')


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
    return BaseResponse(id=existing_category.id, action='updated')


@router.delete('/{category_id}', response_model=BaseResponse)
def delete_category(
    category_id: str,
    repository: CategoryRepo,
):
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
    return BaseResponse(id=existing_category.id, action='deleted')
