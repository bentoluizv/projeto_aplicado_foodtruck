from http import HTTPStatus
from typing import Annotated, Union

from fastapi import (
    APIRouter,
    Depends,
    Form,
    Header,
    HTTPException,
    Query,
    Request,
)
from fastapi.templating import Jinja2Templates

from projeto_aplicado.resources.category.model import Category
from projeto_aplicado.resources.category.repository import (
    CategoryRepository,
    get_category_repository,
)

# from projeto_aplicado.ext.cache.redis import get_many
from projeto_aplicado.resources.category.schemas import UpdateCategoryDTO
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.schemas import (
    BaseResponse,
)
from projeto_aplicado.settings import get_settings

templates = Jinja2Templates(
    directory='templates',
    auto_reload=True,
    cache_size=0,
)

settings = get_settings()

router = APIRouter(
    tags=['Category'], prefix=f'{settings.API_PREFIX}/categories'
)

CategoryRepo = Annotated[CategoryRepository, Depends(get_category_repository)]


@router.get('/', response_model=list[Category])
def get_categories(  # noqa: PLR0913, PLR0917
    request: Request,
    repository: CategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
    source: Annotated[Union[str, None], Header()] = None,
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

    if hx_request and source == 'menu_categories_list':
        return templates.TemplateResponse(
            request,
            'menu_categories_list.html',
            context={'categories': categories},
        )

    if hx_request and source == 'menu_new_category_list':
        return templates.TemplateResponse(
            request,
            'menu_new_category_list.html',
            context={'categories': categories},
        )

    return categories


@router.get('/{category_id}', response_model=Category)
def get_category_by_id(
    request: Request,
    category_id: str,
    repository: CategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
    source: Annotated[Union[str, None], Header()] = None,
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

    if hx_request and source == 'menu_categories_list':
        return templates.TemplateResponse(
            request,
            'selected_category.html',
            context={
                'category': category,
            },
        )
    return category


@router.get('/{category_id}/products', response_model=list[Product])
def get_products_by_category(
    request: Request,
    category_id: str,
    repository: CategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
    source: Annotated[Union[str, None], Header()] = None,
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

    if hx_request and source == 'selected_category_products':
        return templates.TemplateResponse(
            request,
            'selected_category_products.html',
            context={
                'products': category.products,
                'category': category,
            },
        )

    if hx_request and source == 'edit_category_products':
        return templates.TemplateResponse(
            request,
            'selected_category_new_products.html',
            context={
                'products': category.products,
                'category': category,
            },
        )

    return category.products


@router.post(
    '/',
    response_model=BaseResponse,
    status_code=HTTPStatus.CREATED,
)
def create_category(
    request: Request,
    icon_url: Annotated[str, Form()],
    name: Annotated[str, Form()],
    repository: CategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
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

    if hx_request:
        return templates.TemplateResponse(
            request,
            'menu_new_category_list.html',
            headers={'HX-Trigger': 'categoriesUpdated'},
            context={'categories': repository.get_all()},
            status_code=HTTPStatus.CREATED,
        )

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
def delete_category(
    request: Request,
    category_id: str,
    repository: CategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
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

    if hx_request:
        return templates.TemplateResponse(
            request,
            'menu_new_category_list.html',
            headers={'HX-Trigger': 'categoriesUpdated'},
            context={'categories': repository.get_all()},
        )

    return {
        'id': existing_category.id,
        'action': 'deleted',
    }
