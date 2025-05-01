from http import HTTPStatus
from typing import Annotated, Union

from fastapi import (
    APIRouter,
    Depends,
    Form,
    Header,
    HTTPException,
    Request,
)
from fastapi.templating import Jinja2Templates

from projeto_aplicado.resources.order.model import Order
from projeto_aplicado.resources.order.repository import (
    OrderRepository,
    get_order_repository,
)
from projeto_aplicado.resources.order.schemas import OrderList, UpdateOrderDTO
from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.resources.product.repository import (
    ProductRepository,
    get_product_repository,
)
from projeto_aplicado.schemas import BaseResponse
from projeto_aplicado.settings import get_settings

templates = Jinja2Templates(
    directory='templates',
    auto_reload=True,
    cache_size=0,
)
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
            detail=f'Order with {order_id} not found',
        )

    return order


@router.post('/', response_model=BaseResponse, status_code=HTTPStatus.CREATED)
async def create_order(  # noqa: PLR0913, PLR0917
    request: Request,
    order_itens: Annotated[list[dict], Form()],
    customer_id: Annotated[str, Form()],
    notes: Annotated[str, Form()],
    order_repository: OrderRepo,
    product_repository: ProductRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
):
    """
    Create a new order.
    Args:
        request (Request): The HTTP request object.
        order_itens (list[dict]): A list of order items.
        customer_id (str): The ID of the customer.
        notes (str): Additional notes for the order.
        order_repository (OrderRepo): The order repository.
        product_repository (ProductRepo): The product repository.
        hx_request (Union[str, None]): Optional header for HTMX requests.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    Raises:
        HTTPException: If a product in the order items is not found.
    """

    new_order = Order(
        customer_id=customer_id,
        products=[],
        notes=notes,
    )

    for item in order_itens:
        product = product_repository.get_by_id(item['product_id'])
        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Product with {item["product_id"]} not found',
            )

        order_item = OrderItem(
            quantity=item['quantity'],
            price=product.price,
            order_id=new_order.id,
            product_id=item['product_id'],
        )

        new_order.products.append(order_item)

    order_repository.create(new_order)

    if hx_request:
        pass

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
    request: Request,
    order_id: str,
    repository: OrderRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
):
    """
    Delete an order by ID.
    Args:
        request (Request): The HTTP request object.
        order_id (str): The ID of the order to delete.
        repository (OrderRepo): The order repository.
        hx_request (Union[str, None]): Optional header for HTMX requests.
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

    if hx_request:
        pass

    return BaseResponse(id=existing_order.id, action='deleted')
