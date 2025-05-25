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

router = APIRouter(tags=['Product'], prefix=f'{settings.API_PREFIX}/products')


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admin users can perform this action',
        )
    return current_user


@router.get('/', response_model=ProductList, status_code=HTTPStatus.OK)
def fetch_products(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Fetch a list of products with pagination.
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
    '/', response_model=BaseResponse, status_code=status.HTTP_201_CREATED
)
def create_product(
    product_dto: CreateProductDTO,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
):
    """
    Create a new product.
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
