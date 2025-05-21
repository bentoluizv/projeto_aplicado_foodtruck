from typing import Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.schemas import Pagination


class CreateProductDTO(SQLModel):
    """
    Data transfer object for creating a product.
    """

    name: str
    price: float
    image_url: str
    description: str | None = None
    category_id: str


class UpdateProductDTO(SQLModel):
    """
    Data transfer object for updating a product.
    """

    name: str | None = None
    description: str | None = None
    price: float | None = None
    image_url: str | None = None
    category_id: str | None = None


class ProductList(SQLModel):
    """
    Response model for listing products with pagination.
    """

    products: Sequence[Product]
    pagination: Pagination


ProductList.model_rebuild()
