from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.product.repository import (
    ProductRepository,
    get_product_repository,
)
from projeto_aplicado.resources.product.schemas import (
    CreateProductDTO,
    ProductList,
    UpdateProductDTO,
)
from projeto_aplicado.resources.shared.schemas import BaseResponse
from projeto_aplicado.settings import get_settings

settings = get_settings()

ProductRepo = Annotated[ProductRepository, Depends(get_product_repository)]

router = APIRouter(tags=['Product'], prefix=f'{settings.API_PREFIX}/products')


@router.get('/', response_model=ProductList, status_code=HTTPStatus.OK)
def get_products(repository: ProductRepo, offset: int = 0, limit: int = 100):
    """
    Retrieve a list of products with optional pagination.
    Args:
        repository (ProductRepo): The product repository.
        offset (int): The offset for pagination.
        limit (int): The maximum number of products to retrieve.
    Returns:
        ProductList: A list of products with pagination information.
    """
    products = repository.get_all(offset=offset, limit=limit)
    return products


@router.get('/{product_id}')
def get_product_by_id(product_id: str, repository: ProductRepo):
    """
    Get a product by ID.
    """
    product = repository.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )

    return product


@router.post('/', response_model=BaseResponse, status_code=HTTPStatus.CREATED)
async def create_product(
    dto: CreateProductDTO,
    repository: ProductRepo,
):
    """
    Create a new product.
    """

    existing_product = repository.get_by_name(dto.name)

    if existing_product:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Product already exists',
        )

    new_product = Product(
        name=dto.name,
        price=dto.price,
        description=dto.description,
    )

    repository.create(new_product)
    return BaseResponse(id=new_product.id, action='created')


@router.patch('/{product_id}', response_model=BaseResponse)
def update_product(
    product_id: str,
    dto: UpdateProductDTO,
    repository: ProductRepo,
):
    """
    Update an product by ID.
    """
    existing_product = repository.get_by_id(product_id)
    if not existing_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )
    repository.update(existing_product, dto)
    return BaseResponse(id=existing_product.id, action='updated')


@router.delete('/{product_id}', response_model=BaseResponse)
def delete_product(
    product_id: str,
    repository: ProductRepo,
):
    """
    Delete an product by ID.
    """
    existing_product = repository.get_by_id(product_id)

    if not existing_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )

    repository.delete(existing_product)
    return BaseResponse(id=existing_product.id, action='deleted')
