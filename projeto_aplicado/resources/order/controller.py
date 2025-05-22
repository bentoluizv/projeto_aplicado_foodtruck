from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from projeto_aplicado.resources.order.model import Order, OrderItem
from projeto_aplicado.resources.order.repository import (
    OrderRepository,
    get_order_repository,
)
from projeto_aplicado.resources.order.schemas import (
    CreateOrderDTO,
    OrderItemList,
    OrderList,
    UpdateOrderDTO,
)
from projeto_aplicado.resources.product.repository import (
    ProductRepository,
    get_product_repository,
)
from projeto_aplicado.resources.shared.schemas import BaseResponse, Pagination
from projeto_aplicado.settings import get_settings

settings = get_settings()

OrderRepo = Annotated[OrderRepository, Depends(get_order_repository)]
ProductRepo = Annotated[ProductRepository, Depends(get_product_repository)]
router = APIRouter(tags=['Order'], prefix=f'{settings.API_PREFIX}/orders')


@router.get('/', response_model=OrderList, status_code=HTTPStatus.OK)
def fetch_orders(repository: OrderRepo, offset: int = 0, limit: int = 100):
    """
    Get all orders.
    Args:
        repository (OrderRepo): The order repository.
        offset (int): The offset for pagination.
        limit (int): The maximum number of orders to retrieve.
    Returns:
        OrderList: A list of orders with pagination information.
    """
    orders = repository.get_all(offset=offset, limit=limit)
    return orders


@router.get('/{order_id}', response_model=Order)
def fetch_order_by_id(order_id: str, repository: OrderRepo):
    """
    Get a order by ID.
    Args:
        order_id (str): The ID of the order to retrieve.
        repository (OrderRepo): The order repository.
    Returns:
        Order: The order with the specified ID.
    Raises:
        HTTPException: If the order with the specified ID is not found.
    """
    order = repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    return order


@router.get('/{order_id}/items', response_model=OrderItemList)
def fetch_order_items(
    order_id: str, repository: OrderRepo, offset: int = 0, limit: int = 100
):
    """
    Get all items of an order.
    """
    order = repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    return OrderItemList(
        order_items=order.products,
        pagination=Pagination(
            total_count=len(order.products),
            page=offset // limit + 1,
            total_pages=1,
            offset=offset,
            limit=limit,
        ),
    )


@router.post('/', response_model=BaseResponse, status_code=HTTPStatus.CREATED)
async def create_order(  # noqa: PLR0913, PLR0917
    dto: CreateOrderDTO,
    order_repository: OrderRepo,
    product_repository: ProductRepo,
):
    """
    Create a new order.
    Args:
        dto (CreateOrderDTO): The order data.
        order_repository (OrderRepo): The order repository.
        product_repository (ProductRepo): The product repository.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    Raises:
        HTTPException: If a product in the order items is not found.
    """

    new_order = Order.create(dto)

    for item in dto.items:
        product = product_repository.get_by_id(item.product_id)

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product not found',
            )

        order_item = OrderItem.create(item)
        new_order.products.append(order_item)

    order_repository.create(new_order)
    return BaseResponse(id=new_order.id, action='created')


@router.patch('/{order_id}', response_model=BaseResponse)
def update_order(
    order_id: str,
    dto: UpdateOrderDTO,
    repository: OrderRepo,
):
    """
    Update an order by ID.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    Raises:
        HTTPException: If the order with the specified ID is not found.
    """
    existing_order = repository.get_by_id(order_id)

    if not existing_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    repository.update(existing_order, dto)
    return BaseResponse(id=existing_order.id, action='updated')


@router.delete('/{order_id}', response_model=BaseResponse)
def delete_order(
    order_id: str,
    repository: OrderRepo,
):
    """
    Delete an order by ID.
    Args:
        order_id (str): The ID of the order to delete.
        repository (OrderRepo): The order repository.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    Raises:
        HTTPException: If the order with the specified ID is not found.
    """
    existing_order = repository.get_by_id(order_id)

    if not existing_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    repository.delete(existing_order)
    return BaseResponse(id=existing_order.id, action='deleted')
