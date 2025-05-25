from typing import Optional, Sequence

from pydantic import Field
from sqlmodel import SQLModel

from projeto_aplicado.resources.shared.schemas import (
    BaseListResponse,
    BaseModel,
)


class CreateProductDTO(SQLModel):
    """
    Data transfer object for creating a product.
    """

    name: str
    price: float = Field(gt=0.0)
    description: Optional[str] = None


class UpdateProductDTO(SQLModel):
    """
    Data transfer object for updating a product.
    """

    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0.0)
    description: Optional[str] = None


class ProductOut(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class ProductList(BaseListResponse[ProductOut]):
    """
    Response model for listing products with pagination.
    """

    items: Sequence[ProductOut] = Field(alias='products')

    class Config:
        populate_by_name = True


ProductList.model_rebuild()
