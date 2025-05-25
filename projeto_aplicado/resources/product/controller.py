from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlmodel import Session

from projeto_aplicado.auth.security import get_current_user
from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.product.repository import ProductRepository
from projeto_aplicado.resources.product.schemas import (
    PRODUCT_ALREADY_EXISTS,
    PRODUCT_NOT_FOUND,
    CreateProductDTO,
    ProductList,
    ProductOut,
    UpdateProductDTO,
)
from projeto_aplicado.resources.shared.schemas import BaseResponse
from projeto_aplicado.resources.users.model import User, UserRole
from projeto_aplicado.settings import get_settings

settings = get_settings()

router = APIRouter(tags=['Produtos'], prefix=f'{settings.API_PREFIX}/products')


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admin users can perform this action',
        )
    return current_user


@router.get(
    '/',
    response_model=ProductList,
    status_code=HTTPStatus.OK,
    responses={
        200: {
            'description': 'Lista de produtos retornada com sucesso',
            'content': {
                'application/json': {
                    'example': {
                        'items': [
                            {
                                'id': '1',
                                'name': 'X-Burger',
                                'description': 'Hambúrguer artesanal com queijo',
                                'price': 25.90,
                                'category': 'burger',
                                'image_url': 'https://example.com/x-burger.jpg',
                                'is_available': True,
                                'created_at': '2024-03-20T10:00:00',
                                'updated_at': '2024-03-20T10:00:00',
                            },
                            {
                                'id': '2',
                                'name': 'Batata Frita',
                                'description': 'Porção de batata frita crocante',
                                'price': 15.90,
                                'category': 'side',
                                'image_url': 'https://example.com/fries.jpg',
                                'is_available': True,
                                'created_at': '2024-03-20T10:00:00',
                                'updated_at': '2024-03-20T10:00:00',
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
def fetch_products(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Retorna a lista de produtos do sistema.

    Args:
        offset (int, optional): Número de registros para pular. Padrão: 0.
        limit (int, optional): Limite de registros por página. Padrão: 100.
        session (Session): Sessão do banco de dados.
        current_user (User): Usuário autenticado.

    Returns:
        ProductList: Lista de produtos com informações de paginação.

    Examples:
        ```python
        # Exemplo de requisição
        response = await client.get(
            '/api/v1/products',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
        )

        # Exemplo de resposta (200 OK)
        {
            'items': [
                {
                    'id': '1',
                    'name': 'X-Burger',
                    'description': 'Hambúrguer artesanal com queijo',
                    'price': 25.90,
                    'category': 'burger',
                    'image_url': 'https://example.com/x-burger.jpg',
                    'is_available': True,
                    'created_at': '2024-03-20T10:00:00',
                    'updated_at': '2024-03-20T10:00:00'
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
    """
    repository = ProductRepository(session)
    return repository.get_all(offset=offset, limit=limit)


@router.get('/{product_id}', response_model=ProductOut)
def get_product_by_id(
    product_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get a product by its ID.
    """
    repository = ProductRepository(session)
    product = repository.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PRODUCT_NOT_FOUND,
        )
    return product


@router.post(
    '/',
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            'description': 'Produto criado com sucesso',
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
                        'invalid_price': {
                            'value': {
                                'detail': 'Price must be greater than zero'
                            },
                            'summary': 'Preço inválido',
                        },
                        'invalid_category': {
                            'value': {'detail': 'Invalid category'},
                            'summary': 'Categoria inválida',
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
                        'detail': 'Only admin users can perform this action',
                    }
                }
            },
        },
        409: {
            'description': 'Conflito',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Product already exists',
                    }
                }
            },
        },
    },
)
def create_product(
    product_dto: CreateProductDTO,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
):
    """
    Cria um novo produto no sistema.

    Args:
        product_dto (CreateProductDTO): Dados do produto a ser criado.
        session (Session): Sessão do banco de dados.
        current_user (User): Usuário autenticado.

    Returns:
        BaseResponse: Resposta indicando o resultado da operação.

    Raises:
        HTTPException:
            - Se os dados forem inválidos (400)
            - Se o usuário não estiver autenticado (401)
            - Se o usuário não tiver permissão (403)
            - Se o produto já existir (409)

    Examples:
        ```python
        # Exemplo de requisição
        response = await client.post(
            '/api/v1/products',
            json={
                'name': 'X-Bacon',
                'description': 'Hambúrguer com bacon e queijo',
                'price': 29.90,
                'category': 'burger',
                'image_url': 'https://example.com/x-bacon.jpg',
                'is_available': True
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
    repository = ProductRepository(session)
    existing_product = repository.find_by_name(product_dto.name)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=PRODUCT_ALREADY_EXISTS,
        )
    product = Product.create(product_dto)
    repository.create(product)
    return BaseResponse(id=product.id, action='created')


@router.put('/{product_id}', response_model=BaseResponse)
def update_product(
    product_id: str,
    product_dto: UpdateProductDTO,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
):
    """
    Update an existing product.
    """
    repository = ProductRepository(session)
    product = repository.update(product_id, product_dto)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PRODUCT_NOT_FOUND,
        )
    return BaseResponse(id=product.id, action='updated')


@router.patch('/{product_id}', response_model=BaseResponse)
def patch_product(
    product_id: str,
    product_dto: UpdateProductDTO,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
):
    """
    Partially update an existing product.
    """
    repository = ProductRepository(session)
    product = repository.update(product_id, product_dto)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PRODUCT_NOT_FOUND,
        )
    return BaseResponse(id=product.id, action='updated')


@router.delete(
    '/{product_id}', response_model=BaseResponse, status_code=HTTPStatus.OK
)
def delete_product(
    product_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
):
    """
    Delete a product.
    """
    repository = ProductRepository(session)
    if not repository.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PRODUCT_NOT_FOUND,
        )
    return BaseResponse(id=product_id, action='deleted')
