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
    CreateOrderItemDTO, # Importado para mapear os itens do pedido
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
                                'items': [ # Exemplo de como os itens serão retornados
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
async def fetch_orders( # A função é assíncrona para ser um endpoint FastAPI
    repository: OrderRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retorna a lista de pedidos do sistema. Inclui paginação e os detalhes dos itens de cada pedido.

    Args:
        repository (OrderRepository): Repositório de pedidos para acesso aos dados.
        current_user (User): Objeto do usuário autenticado.
        offset (int, optional): Número de registros para pular (para paginação). Padrão: 0.
        limit (int, optional): Limite de registros por página (para paginação). Padrão: 100.

    Returns:
        OrderList: Uma lista de objetos OrderOut (pedidos) com informações de paginação.
    """
    # Chama os métodos do repositório de forma síncrona.
    # FastAPI gerencia a execução em um worker thread para que a aplicação não bloqueie.
    orders = repository.get_all(offset=offset, limit=limit)
    total_count = repository.get_total_count()
    
    # Calcula informações de paginação
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
    page = (offset // limit) + 1 if limit > 0 else 1

    orders_out = []
    for order in orders:
        items_out = []
        # Itera sobre a relação 'products' do objeto Order (que são os OrderItems)
        # e mapeia cada OrderItem para um CreateOrderItemDTO.
        if order.products:
            for item in order.products:
                items_out.append(
                    CreateOrderItemDTO(
                        quantity=item.quantity,
                        product_id=item.product_id,
                        price=item.price,
                    )
                )

        # Constrói o objeto OrderOut, preenchendo o campo 'items' com os DTOs dos itens.
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

    # Retorna a lista de pedidos e as informações de paginação.
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
async def fetch_order_by_id( # A função é assíncrona
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
):
    """
    Obtém um pedido específico pelo ID.

    Args:
        order_id (str): O ID único do pedido a ser recuperado.
        repository (OrderRepo): Repositório de pedidos para acesso aos dados.
        current_user (User): Objeto do usuário autenticado.

    Returns:
        OrderOut: O pedido com o ID especificado, incluindo todos os seus itens.

    Raises:
        HTTPException: Se o pedido com o ID especificado não for encontrado (HTTP 404 NOT FOUND).
    """
    # Busca o pedido pelo ID usando o repositório de forma síncrona.
    order = repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    items_out = []
    # Mapeia os OrderItems da relação 'products' para CreateOrderItemDTOs.
    if order.products:
        for item in order.products:
            items_out.append(
                CreateOrderItemDTO(
                    quantity=item.quantity,
                    product_id=item.product_id,
                    price=item.price,
                )
            )

    # Retorna uma instância de OrderOut com todos os detalhes do pedido e seus itens.
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
async def fetch_order_items( # A função é assíncrona
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    """
    Obtém todos os itens de um pedido específico.

    Args:
        order_id (str): O ID do pedido cujos itens serão recuperados.
        repository (OrderRepo): Repositório de pedidos para acesso aos dados.
        current_user (User): Objeto do usuário autenticado.
        offset (int, optional): Número de registros para pular (para paginação). Padrão: 0.
        limit (int, optional): Limite de registros por página (para paginação). Padrão: 100.

    Returns:
        OrderItemList: Uma lista de objetos OrderItem com informações de paginação.

    Raises:
        HTTPException: Se o pedido com o ID especificado não for encontrado (HTTP 404 NOT FOUND).
    """
    # Busca o pedido pelo ID. Os itens (products) já são carregados.
    order = repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    # Acessa a lista de produtos diretamente do objeto Order carregado.
    # A paginação é feita em memória para a lista de itens.
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
async def create_order( # A função é assíncrona
    dto: CreateOrderDTO,
    order_repository: OrderRepo,
    product_repository: ProductRepo,
    current_user: CurrentUser,
):
    """
    Cria um novo pedido no sistema.

    Args:
        dto (CreateOrderDTO): Objeto de transferência de dados contendo os detalhes do pedido a ser criado.
        order_repository (OrderRepository): Repositório de pedidos.
        product_repository (ProductRepository): Repositório de produtos para validação.
        current_user (User): Objeto do usuário autenticado.

    Returns:
        BaseResponse: Resposta básica indicando o ID do pedido criado e a ação.

    Raises:
        HTTPException:
            - 403 Forbidden: Se o usuário não tiver permissão para criar pedidos.
            - 422 Unprocessable Entity: Se algum produto no pedido não for encontrado.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to create orders',
        )

    new_order = Order.create(dto)

    for item in dto.items:
        # Busca o produto pelo ID de forma síncrona.
        product = product_repository.get_by_id(item.product_id)

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Product not found',
            )

        order_item = OrderItem.create(item)
        new_order.products.append(order_item)

    # Salva o novo pedido no banco de dados de forma síncrona.
    order_repository.create(new_order)
    return BaseResponse(id=new_order.id, action='created')


@router.patch('/{order_id}', response_model=BaseResponse)
async def update_order( # A função é assíncrona
    order_id: str,
    dto: UpdateOrderDTO,
    repository: OrderRepo,
    current_user: CurrentUser,
):
    """
    Atualiza um pedido existente pelo ID.

    Args:
        order_id (str): O ID do pedido a ser atualizado.
        dto (UpdateOrderDTO): Objeto de transferência de dados com as informações de atualização.
        repository (OrderRepo): Repositório de pedidos.
        current_user (User): Objeto do usuário autenticado.

    Returns:
        BaseResponse: Resposta básica indicando o ID do pedido atualizado e a ação.

    Raises:
        HTTPException:
            - 403 Forbidden: Se o usuário não tiver permissão para atualizar pedidos.
            - 404 Not Found: Se o pedido com o ID especificado não for encontrado.
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

    # Busca o pedido existente pelo ID de forma síncrona.
    existing_order = repository.get_by_id(order_id)

    if not existing_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    # Atualiza o pedido no banco de dados de forma síncrona.
    repository.update(existing_order, dto)
    return BaseResponse(id=existing_order.id, action='updated')


@router.delete('/{order_id}', response_model=BaseResponse)
async def delete_order( # A função é assíncrona
    order_id: str,
    repository: OrderRepo,
    current_user: CurrentUser,
):
    """
    Exclui um pedido pelo ID.

    Args:
        order_id (str): O ID do pedido a ser excluído.
        repository (OrderRepo): Repositório de pedidos.
        current_user (User): Objeto do usuário autenticado.

    Returns:
        BaseResponse: Resposta básica indicando o ID do pedido excluído e a ação.

    Raises:
        HTTPException:
            - 403 Forbidden: Se o usuário não tiver permissão para excluir pedidos.
            - 404 Not Found: Se o pedido com o ID especificado não for encontrado.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to delete orders',
        )

    # Busca o pedido existente pelo ID de forma síncrona.
    existing_order = repository.get_by_id(order_id)

    if not existing_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order not found',
        )

    # Exclui o pedido do banco de dados de forma síncrona.
    repository.delete(existing_order)
    return BaseResponse(id=existing_order.id, action='deleted')