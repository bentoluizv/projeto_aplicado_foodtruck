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
from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.resources.product.repository import (
    ProductRepository,
    get_product_repository,
)
from projeto_aplicado.schemas import (
    BaseResponse,
    UpdateProductDTO,
)
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


@router.get('/', response_model=list[Order])
def get_orders(repository: OrderRepo, offset: int = 0, limit: int = 100):
    """
    Get all orders.
    """
    orders = repository.get_all(offset=offset, limit=limit)

    return orders


@router.get('/{order_id}', response_model=Order)
def get_product_by_id(order_id: str, repository: OrderRepo):
    """
    Get a order by ID.
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
            order_id='',
            product_id=item['product_id'],
        )

        new_order.products.append(order_item)

    order_repository.create(new_order)

    # if hx_request:
    #     return templates.TemplateResponse(
    #         request,
    #         'selected_category_new_products.html',
    #         headers={'HX-Trigger': 'productsUpdated'},
    #         context={
    #             'product': order_repository.get_all(),
    #         },
    #         status_code=HTTPStatus.CREATED,
    #     )

    return BaseResponse(id=new_order.id, action='created')


@router.patch('/{product_id}', response_model=BaseResponse)
def update_product(
    product_id: str,
    dto: UpdateProductDTO,
    repository: OrderRepo,
):
    """
    Update an product by ID.
    """

    existing_product = repository.get_by_id(product_id)
    if not existing_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='product not found',
        )
    repository.update(existing_product, dto)
    return BaseResponse(id=existing_product.id, action='updated')


@router.delete('/{product_id}', response_model=BaseResponse)
def delete_product(
    request: Request,
    product_id: str,
    repository: OrderRepo,
    hx_request: Annotated[Union[str, None], Header()] = None,
):
    """
    Delete an product by ID.
    """

    existing_product = repository.get_by_id(product_id)

    if not existing_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='product not found',
        )

    repository.delete(existing_product)

    if hx_request:
        return templates.TemplateResponse(
            request,
            'selected_category_new_products.html',
            headers={'HX-Trigger': 'productsUpdated'},
            context={'categories': repository.get_all()},
            status_code=HTTPStatus.OK,
        )

    return BaseResponse(id=existing_product.id, action='deleted')
