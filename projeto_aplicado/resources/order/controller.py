from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from projeto_aplicado.auth.security import get_current_user
from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.resources.order.model import Order, OrderItem
from projeto_aplicado.resources.order.repository import (
    OrderRepository,
    get_order_repository,
)
from projeto_aplicado.resources.order.schemas import (
    CreateOrderDTO,
    OrderItemList,
    OrderList,
    OrderOut,
    UpdateOrderDTO,
)
from projeto_aplicado.resources.product.repository import (
    ProductRepository,
    get_product_repository,
)
from projeto_aplicado.resources.shared.schemas import BaseResponse, Pagination
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.settings import get_settings

settings = get_settings()

OrderRepo = Annotated[OrderRepository, Depends(get_order_repository)]
ProductRepo = Annotated[ProductRepository, Depends(get_product_repository)]
router = APIRouter(tags=['Pedidos'], prefix=f'{settings.API_PREFIX}/orders')
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/',
    response_model=OrderList,
    status_code=HTTPStatus.OK,
    responses={
        200: {
            'description': 'Lista de pedidos retornada com sucesso',
            'content': {
                'application/json': {
                    'example': {
                        'orders': [
                            {
                                'id': '1',
                                'status': 'pending',
                                'total': 41.80,
                                'created_at': '2024-03-20T10:00:00',
                                'updated_at': '2024-03-20T10:00:00',
                                'locator': 'A123',
                                'notes': 'Sem cebola',
                            },
                            {
                                'id': '2',
                                'status': 'preparing',
                                'total': 25.90,
                                'created_at': '2024-03-20T10:00:00',
                                'updated_at': '2024-03-20T10:00:00',
                                'locator': 'B456',
                                'notes': None,
                            },
                        ],
                        'pagination': {
                            'offset': 0,
                            'limit': 100,
                            'total_count': 2,
                            'total_pages': 1,
                            'page': 1,
                        },
                    }
                }
            },
        },
        401: {
            'description': 'Não autorizado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Not authenticated',
                    }
                }
            },
        },
    },
)
def fetch_orders(
    repository: OrderRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retorna a lista de pedidos do sistema.

    Args:
        repository (OrderRepository): Repositório de pedidos.
        current_user (User): Usuário autenticado.
        offset (int, optional): Número de registros para pular. Padrão: 0.
        limit (int, optional): Limite de registros por página. Padrão: 100.

    Returns:
        OrderList: Lista de pedidos com informações de paginação.

    Examples:
        ```python
        # Exemplo de requisição
        response = await client.get(
            '/api/v1/orders',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
        )

        # Exemplo de resposta (200 OK)
        {
            'orders': [
                {
                    'id': '1',
                    'status': 'pending',
                    'total': 41.80,
                    'created_at': '2024-03-20T10:00:00',
                    'updated_at': '2024-03-20T10:00:00',
                    'locator': 'A123',
                    'notes': 'Sem cebola'
                }
            ],
            'pagination': {
                'offset': 0,
                'limit': 100,
                'total_count': 1,
                'total_pages': 1,
                'page': 1
            }
        }
        ```
    """  # noqa: E501
    orders = repository.get_all(offset=offset, limit=limit)
    total_count = repository.get_total_count()
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
    page = (offset // limit) + 1 if limit > 0 else 1

    order_list = [
        OrderOut(
            id=order.id,
            products=order.products,
            status=OrderStatus(order.status.upper()),
            total=order.total,
            rating=order.rating,
            created_at=order.created_at.isoformat()
            if hasattr(order.created_at, 'isoformat')
            else str(order.created_at),
            updated_at=order.updated_at.isoformat()
            if hasattr(order.updated_at, 'isoformat')
            else str(order.updated_at),
            locator=order.locator,
            notes=order.notes,
        )
        for order in orders
    ]
    return OrderList(
        orders=order_list,
        pagination=Pagination(
            offset=offset,
            limit=limit,
            total_count=total_count,
            total_pages=total_pages,
            page=page,
        ),
    )


@router.get('/{order_id}', response_model=Order)
def fetch_order_by_id(
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
):
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
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
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


@router.post(
    '/',
    response_model=BaseResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        201: {
            'description': 'Pedido criado com sucesso',
            'content': {
                'application/json': {
                    'example': {
                        'id': '3',
                        'action': 'created',
                    }
                }
            },
        },
        400: {
            'description': 'Dados inválidos',
            'content': {
                'application/json': {
                    'examples': {
                        'empty_items': {
                            'value': {
                                'detail': 'Order must have at least one item'
                            },
                            'summary': 'Lista de itens vazia',
                        },
                        'invalid_quantity': {
                            'value': {
                                'detail': 'Quantity must be greater than zero'
                            },
                            'summary': 'Quantidade inválida',
                        },
                    }
                }
            },
        },
        401: {
            'description': 'Não autorizado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Not authenticated',
                    }
                }
            },
        },
        403: {
            'description': 'Acesso negado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'You are not allowed to create orders',
                    }
                }
            },
        },
        422: {
            'description': 'Entidade não processável',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Product not found',
                    }
                }
            },
        },
    },
)
async def create_order(
    dto: CreateOrderDTO,
    order_repository: OrderRepo,
    product_repository: ProductRepo,
    current_user: CurrentUser,
):
    """
    Cria um novo pedido no sistema.

    Args:
        dto (CreateOrderDTO): Dados do pedido a ser criado.
        order_repository (OrderRepository): Repositório de pedidos.
        product_repository (ProductRepository): Repositório de produtos.
        current_user (User): Usuário autenticado.

    Returns:
        BaseResponse: Resposta indicando o resultado da operação.

    Raises:
        HTTPException:
            - Se os dados forem inválidos (400)
            - Se o usuário não estiver autenticado (401)
            - Se o usuário não tiver permissão (403)
            - Se algum produto não for encontrado (422)

    Examples:
        ```python
        # Exemplo de requisição
        response = await client.post(
            '/api/v1/orders',
            json={
                'items': [
                    {
                        'product_id': '1',
                        'quantity': 1
                    },
                    {
                        'product_id': '2',
                        'quantity': 2
                    }
                ],
                'notes': 'Sem cebola'
            },
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
        )

        # Exemplo de resposta (201 Created)
        {
            'id': '3',
            'action': 'created'
        }
        ```
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to create orders',
        )

    new_order = Order.create(dto)

    for item in dto.items:
        product = product_repository.get_by_id(item.product_id)

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Product not found',
            )

        order_item = OrderItem.create(item)
        new_order.products.append(order_item)

    new_order.total = sum(
        item.calculate_total() for item in new_order.products
    )
    order_repository.create(new_order)
    return BaseResponse(id=new_order.id, action='created')


@router.patch('/{order_id}', response_model=BaseResponse)
def update_order(
    order_id: str,
    dto: UpdateOrderDTO,
    repository: OrderRepo,
    current_user: CurrentUser,
):
    """
    Update an order by ID.
    Returns:
        BaseResponse: A response indicating the result of the operation.
    Raises:
        HTTPException: If the order with the specified ID is not found.
    """
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.ATTENDANT,
        UserRole.KITCHEN,
    }:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to update orders',
        )

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
    current_user: CurrentUser,
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
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to delete orders',
        )

    existing_order = repository.get_by_id(order_id)

    if not existing_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    if existing_order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Order is not pending',
        )

    repository.delete(existing_order)
    return BaseResponse(id=existing_order.id, action='deleted')
