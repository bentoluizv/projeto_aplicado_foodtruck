from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from projeto_aplicado.models.entities import Item
from projeto_aplicado.models.schemas import (
    BaseResponse,
    CreateItemDTO,
    UpdateItemDTO,
)
from projeto_aplicado.repositories.item_repository import (
    ItemRepository,
    get_item_repository,
)

router = APIRouter(tags=['Item'], prefix='/itens')

ItemRepo = Annotated[ItemRepository, Depends(get_item_repository)]


@router.get('/', response_model=list[Item])
def get_itens(repository: ItemRepo, offset: int = 0, limit: int = 100):
    """
    Get all items.
    """
    items = repository.get_all(offset=offset, limit=limit)

    return items


@router.get('/{item_id}')
def get_item_by_id(item_id: str, repository: ItemRepo):
    """
    Get an item by ID.
    """
    item = repository.get_by_id(item_id)

    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Item with {item_id} not found',
        )

    return item


@router.post('/', response_model=BaseResponse, status_code=HTTPStatus.CREATED)
def create_item(data: CreateItemDTO, repository: ItemRepo):
    """
    Create a new item.
    """

    existing_item = repository.get_by_name(data.name)

    if existing_item:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Item already exists',
        )

    new_item = Item(
        name=data.name, price=data.price, category_id=data.category_id
    )

    repository.create(new_item)

    return BaseResponse(id=new_item.id, action='created')


@router.patch('/{item_id}', response_model=BaseResponse)
def update_item(
    item_id: str,
    dto: UpdateItemDTO,
    repository: ItemRepo,
):
    """
    Update an item by ID.
    """

    existing_item = repository.get_by_id(item_id)
    if not existing_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item not found',
        )
    repository.update(existing_item, dto)
    return BaseResponse(id=existing_item.id, action='updated')


@router.delete('/{item_id}', response_model=BaseResponse)
def delete_item(item_id: str, repository: ItemRepo):
    """
    Delete an item by ID.
    """

    existing_item = repository.get_by_id(item_id)

    if not existing_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item not found',
        )

    repository.delete(existing_item)
    return BaseResponse(id=existing_item.id, action='deleted')
