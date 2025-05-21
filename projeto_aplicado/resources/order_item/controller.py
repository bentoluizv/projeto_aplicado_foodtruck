from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
)

from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.resources.order_item.repository import (
    OrderItemRepository,
    get_order_item_repository,
)
from projeto_aplicado.resources.order_item.schemas import (
    CreateOrderItemDTO,
    OrderItemList,
    UpdateOrderItemDTO,
)
from projeto_aplicado.schemas import BaseResponse
from projeto_aplicado.settings import get_settings

settings = get_settings()

OrderItemRepo = Annotated[
    OrderItemRepository, Depends(get_order_item_repository)
]

router = APIRouter(
    tags=['OrderItem'], prefix=f'{settings.API_PREFIX}/order_items'
)


@router.get('/', response_model=OrderItemList, status_code=HTTPStatus.OK)
def fetch_order_items(
    repository: OrderItemRepo, offset: int = 0, limit: int = 100
):
    """
    Retrieve a list of order items with optional pagination.
    Args:
        repository (OrderItemRepo): The order item repository.
        offset (int): The offset for pagination.
        limit (int): The maximum number of products to retrieve.
    Returns:
        OrderItemList: A list of order items with pagination information.
    """
    order_items = repository.get_all(offset=offset, limit=limit)
    return order_items


@router.get('/{order_item_id}')
def fetch_order_item_by_id(order_item_id: str, repository: OrderItemRepo):
    """
    Get a order item by ID.
    Args:
        order_item_id (str): The ID of the order item to retrieve.
        repository (OrderItemRepo): The order item repository.
    Returns:
        OrderItem: The order item with the specified ID.
    Raises:
        HTTPException: If the order item with the specified ID is not found.
    """
    order_item = repository.get_by_id(order_item_id)

    if not order_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Order item with {order_item_id} not found',
        )

    return order_item


@router.post('/', response_model=BaseResponse, status_code=HTTPStatus.CREATED)
async def create_order_item(  # noqa: PLR0913, PLR0917
    price: Annotated[float, Form()],
    quantity: Annotated[int, Form()],
    order_id: Annotated[str, Form()],
    product_id: Annotated[str, Form()],
    repository: OrderItemRepo,
):
    """
    Create a new order item.
    Args:
        price (float): The price of the order item.
        quantity (int): The quantity of the order item.
        order_id (str): The ID of the order.
        product_id (str): The ID of the product.
        repository (OrderItemRepo): The order item repository.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    """
    data = CreateOrderItemDTO(
        quantity=quantity,
        price=price,
        order_id=order_id,
        product_id=product_id,
    )

    new_order_item = OrderItem(**data.model_dump())
    repository.create(new_order_item)
    return BaseResponse(id=new_order_item.id, action='created')


@router.patch('/{order_item_id}', response_model=BaseResponse)
def update_order_item(
    order_item_id: str,
    dto: UpdateOrderItemDTO,
    repository: OrderItemRepo,
):
    """
    Update an order item by ID.
    Args:
        order_item_id (str): The ID of the order item to update.
        dto (UpdateOrderItemDTO): The data transfer object containing the updated order item information.
        repository (OrderItemRepo): The order item repository.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    Raises:
        HTTPException: If the order item with the specified ID is not found.
    """
    existing_order_item = repository.get_by_id(order_item_id)

    if not existing_order_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='order item not found',
        )

    repository.update(existing_order_item, dto)
    return BaseResponse(id=existing_order_item.id, action='updated')


@router.delete('/{order_item_id}', response_model=BaseResponse)
def delete_order_item(
    order_item_id: str,
    repository: OrderItemRepo,
):
    """
    Delete an order item by ID.
    Args:
        order_item_id (str): The ID of the order item to delete.
        repository (OrderItemRepo): The order item repository.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    Raises:
        HTTPException: If the order item with the specified ID is not found.
    """
    existing_order_item = repository.get_by_id(order_item_id)

    if not existing_order_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='order item not found',
        )

    repository.delete(existing_order_item)
    return BaseResponse(id=existing_order_item.id, action='deleted')
