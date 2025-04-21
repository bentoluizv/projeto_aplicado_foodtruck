from http import HTTPStatus
from typing import Annotated, Union

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.templating import Jinja2Templates
from supabase import Client

from projeto_aplicado.data.schemas import (
    BaseResponse,
    CreateProductDTO,
    UpdateProductDTO,
)
from projeto_aplicado.ext.supabase.client import get_supabase_client
from projeto_aplicado.ext.supabase.storage import uploadProductImage
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.product.repository import (
    ProductRepository,
    get_product_repository,
)
from projeto_aplicado.settings import get_settings

templates = Jinja2Templates(
    directory='templates',
    auto_reload=True,
    cache_size=0,
)
settings = get_settings()

ProductRepo = Annotated[ProductRepository, Depends(get_product_repository)]
Supabase = Annotated[Client, Depends(get_supabase_client)]

router = APIRouter(tags=['Product'], prefix=f'{settings.API_PREFIX}/products')


@router.get('/', response_model=list[Product])
def get_products(repository: ProductRepo, offset: int = 0, limit: int = 100):
    """
    Get all products.
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
            detail=f'Product with {product_id} not found',
        )

    return product


@router.post('/', response_model=BaseResponse, status_code=HTTPStatus.CREATED)
async def create_product(  # noqa: PLR0913, PLR0917
    request: Request,
    price: Annotated[float, Form()],
    image: Annotated[UploadFile, File()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    category_id: Annotated[str, Form()],
    repository: ProductRepo,
    supabase: Supabase,
    hx_request: Annotated[Union[str, None], Header()] = None,
):
    """
    Create a new product.
    """

    img_url = await uploadProductImage(supabase, image)

    data = CreateProductDTO(
        name=name,
        price=price,
        img_url=img_url,
        description=description,
        category_id=category_id,
    )

    existing_product = repository.get_by_name(data.name)

    if existing_product:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Product already exists',
        )

    new_product = Product(
        name=data.name,
        price=data.price,
        category_id=data.category_id,
        image_url=data.img_url,
        description=data.description,
    )

    repository.create(new_product)

    if hx_request:
        return templates.TemplateResponse(
            request,
            'product_item.html',
            headers={'HX-Trigger': 'productsUpdated'},
            context={
                'product': repository.get_all(),
            },
            status_code=HTTPStatus.CREATED,
        )
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
            detail='product not found',
        )
    repository.update(existing_product, dto)
    return BaseResponse(id=existing_product.id, action='updated')


@router.delete('/{product_id}', response_model=BaseResponse)
def delete_product(product_id: str, repository: ProductRepo):
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
    return BaseResponse(id=existing_product.id, action='deleted')
