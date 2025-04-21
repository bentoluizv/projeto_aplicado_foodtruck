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

from projeto_aplicado.data.schemas import (
    BaseResponse,
    UpdateCategoryDTO,
)

# from projeto_aplicado.ext.cache.redis import get_many
from projeto_aplicado.item.model import Item
from projeto_aplicado.item_category.model import ItemCategory
from projeto_aplicado.item_category.repository import (
    ItemCategoryRepository,
    get_category_repository,
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

ItemCategoryRepo = Annotated[
    ItemCategoryRepository, Depends(get_category_repository)
]


@router.get('/', response_model=list[ItemCategory])
def get_categories(  # noqa: PLR0913, PLR0917
    request: Request,
    repository: ItemCategoryRepo,
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

    if hx_request and source == 'categories':
        return templates.TemplateResponse(
            request, 'categories.html', context={'categories': categories}
        )

    if hx_request and source == 'categories_new':
        return templates.TemplateResponse(
            request, 'categories_new.html', context={'categories': categories}
        )

    return categories


@router.get('/{category_id}', response_model=ItemCategory)
def get_category_by_id(category_id: str, repository: ItemCategoryRepo):
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


@router.get('/{category_id}/itens', response_model=list[Item])
def get_items_by_category(
    request: Request,
    category_id: str,
    repository: ItemCategoryRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
    source: Annotated[Union[str, None], Header()] = None,
):
    """
    Get items by category ID.
    """
    category = repository.get_by_id(category_id)

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Category with {category_id} not found',
        )

    if hx_request and source == 'categories':
        return templates.TemplateResponse(
            request,
            'category_itens.html',
            context={
                'itens': category.itens,
                'category': category,
            },
        )

    if hx_request and source == 'category-itens':
        return templates.TemplateResponse(
            request,
            'category_item_list.html',
            context={
                'itens': category.itens,
                'category': category,
            },
        )

    return category.itens


@router.post(
    '/',
    response_model=BaseResponse,
    status_code=HTTPStatus.CREATED,
)
def create_category(
    request: Request,
    icon_url: Annotated[str, Form()],
    name: Annotated[str, Form()],
    repository: ItemCategoryRepo,
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

    new_category = ItemCategory(name=name, icon_url=icon_url)
    repository.create(new_category)

    if hx_request:
        return templates.TemplateResponse(
            request,
            'categories_new.html',
            headers={'HX-Trigger': 'categoriesUpdated'},
            context={'categories': repository.get_all()},
        )

    return {
        'id': new_category.id,
        'action': 'created',
    }


@router.patch('/{category_id}', response_model=BaseResponse)
def update_category(
    category_id: str, dto: UpdateCategoryDTO, repository: ItemCategoryRepo
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
    repository: ItemCategoryRepo,
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
            'categories_new.html',
            headers={'HX-Trigger': 'categoriesUpdated'},
            context={'categories': repository.get_all()},
        )

    return {
        'id': existing_category.id,
        'action': 'deleted',
    }
