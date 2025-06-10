from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlmodel import Session # Importe Session aqui
from projeto_aplicado.ext.database.db import get_session # Importe get_session aqui

from projeto_aplicado.auth.security import get_current_user
from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.resources.order.model import Order, OrderItem
from projeto_aplicado.resources.order.repository import (
    OrderRepository,
    get_order_repository,
)
from projeto_aplicado.resources.order.schemas import (
    CreateOrderDTO,
    CreateOrderItemDTO,
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

# Definição dos tipos anotados para injeção de dependência via FastAPI.
OrderRepo = Annotated[OrderRepository, Depends(get_order_repository)]
ProductRepo = Annotated[ProductRepository, Depends(get_product_repository)]
router = APIRouter(tags=['Pedidos'], prefix=f'{settings.API_PREFIX}/orders')
CurrentUser = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[Session, Depends(get_session)] # Novo tipo para a sessão do banco de dados


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
                                'items': [
                                    {'quantity': 1, 'product_id': 'some_product_id_1', 'price': 20.0},
                                    {'quantity': 2, 'product_id': 'some_product_id_2', 'price': 10.90},
                                ],
                            },
                            {
                                'id': '2',
                                'status': 'preparing',
                                'total': 25.90,
                                'created_at': '2024-03-20T10:00:00',
                                'updated_at': '2024-03-20T10:00:00',
                                'locator': 'B456',
                                'notes': None,
                                'items': [
                                    {'quantity': 1, 'product_id': 'some_product_id_3', 'price': 25.90},
                                ],
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
async def fetch_orders(
    repository: OrderRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retorna a lista de pedidos do sistema. Inclui paginação e os detalhes dos itens de cada pedido.
    """
    orders = repository.get_all(offset=offset, limit=limit)
    total_count = repository.get_total_count()
    
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
    page = (offset // limit) + 1 if limit > 0 else 1

    orders_out = []
    for order in orders:
        items_out = []
        if order.products:
            for item in order.products:
                items_out.append(
                    CreateOrderItemDTO(
                        quantity=item.quantity,
                        product_id=item.product_id,
                        price=item.price,
                    )
                )

        orders_out.append(
            OrderOut(
                id=order.id,
                status=OrderStatus(order.status.upper()),
                total=order.total,
                created_at=order.created_at.isoformat()
                if hasattr(order.created_at, 'isoformat')
                else str(order.created_at),
                updated_at=order.updated_at.isoformat()
                if hasattr(order.updated_at, 'isoformat')
                else str(order.updated_at),
                locator=order.locator,
                notes=order.notes,
                items=items_out,
            )
        )

    return OrderList(
        orders=orders_out,
        pagination=Pagination(
            offset=offset,
            limit=limit,
            total_count=total_count,
            total_pages=total_pages,
            page=page,
        ),
    )


@router.get('/{order_id}', response_model=OrderOut)
async def fetch_order_by_id(
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
):
    """
    Obtém um pedido específico pelo ID.
    """
    order = repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    items_out = []
    if order.products:
        for item in order.products:
            items_out.append(
                CreateOrderItemDTO(
                    quantity=item.quantity,
                    product_id=item.product_id,
                    price=item.price,
                )
            )

    return OrderOut(
        id=order.id,
        status=OrderStatus(order.status.upper()),
        total=order.total,
        created_at=order.created_at.isoformat()
        if hasattr(order.created_at, 'isoformat')
        else str(order.created_at),
        updated_at=order.updated_at.isoformat()
        if hasattr(order.updated_at, 'isoformat')
        else str(order.updated_at),
        locator=order.locator,
        notes=order.notes,
        items=items_out,
    )


@router.get('/{order_id}/items', response_model=OrderItemList)
async def fetch_order_items(
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    """
    Obtém todos os itens de um pedido específico.
    """
    order = repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    paginated_products = order.products[offset : offset + limit]
    total_products = len(order.products)


    return OrderItemList(
        order_items=paginated_products,
        pagination=Pagination(
            total_count=total_products,
            page=offset // limit + 1 if limit > 0 else 1,
            total_pages=(total_products + limit - 1) // limit if limit > 0 else 0,
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
            }
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
            }
        },
        401: {
            'description': 'Não autorizado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Not authenticated',
                    }
                }
            }
        },
        403: {
            'description': 'Acesso negado',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'You are not allowed to create orders',
                    }
                }
            }
        },
        422: {
            'description': 'Entidade não processável',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Product not found',
                    }
                }
            }
        },
    },
)
async def create_order(
    dto: CreateOrderDTO,
    product_repository: ProductRepo,
    current_user: CurrentUser,
    session: DBSession, # Injeta a sessão do banco de dados
):
    """
    Cria um novo pedido no sistema.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to create orders',
        )

    new_order = Order.create(dto)
    
    session.add(new_order)
    # Removido 'await' de session.flush() pois pode ser síncrono.
    # Se get_session fornece AsyncSession, 'await' é necessário.
    # Mas dado os erros anteriores, presumimos que a sessão é síncrona.
    session.flush() 

    for item_dto in dto.items:
        product = product_repository.get_by_id(item_dto.product_id)

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Product not found',
            )

        order_item = OrderItem.create(item_dto)
        order_item.order_id = new_order.id 
        
        new_order.products.append(order_item)

    new_order.total = sum(item.calculate_total() for item in new_order.products)

    # Removido 'session.add_all(items_to_persist)' pois new_order.products.append()
    # já os adiciona à sessão via relação, e o session.add(new_order) já os inclui na transação.
    
    # Removido 'await' de session.commit() pois pode ser síncrono.
    session.commit()
    # Removido 'await' de session.refresh() pois pode ser síncrono.
    session.refresh(new_order) 

    return BaseResponse(id=new_order.id, action='created')


@router.patch('/{order_id}', response_model=BaseResponse)
async def update_order(
    order_id: str,
    dto: UpdateOrderDTO,
    repository: OrderRepo,
    current_user: CurrentUser,
):
    """
    Atualiza um pedido existente pelo ID.
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
async def delete_order(
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
):
    """
    Exclui um pedido pelo ID.
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

    repository.delete(existing_order)
    return BaseResponse(id=existing_order.id, action='deleted')