from typing import Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.schemas import Pagination


class CreateProductDTO(SQLModel):
    name: str
    price: float
    img_url: str
    description: str | None = None
    category_id: str


class UpdateProductDTO(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    image: bytes | None = None
    category_id: str | None = None


class ProductList(SQLModel):
    pagination: Pagination
    products: Sequence['Product']


ProductList.model_rebuild()
