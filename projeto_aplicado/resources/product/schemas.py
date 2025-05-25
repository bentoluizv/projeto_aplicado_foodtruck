from typing import Optional, Sequence

from pydantic import Field, validator
from sqlmodel import SQLModel

from projeto_aplicado.resources.product.enums import ProductCategory
from projeto_aplicado.resources.shared.schemas import (
    BaseListResponse,
    BaseModel,
)

# Centralized error messages
PRODUCT_NOT_FOUND = 'Product not found'
PRODUCT_ALREADY_EXISTS = 'Product already exists'


class CreateProductDTO(SQLModel):
    """
    Data transfer object for creating a product.
    """

    name: str
    price: float = Field(gt=0.0)
    description: Optional[str] = None
    category: ProductCategory

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v


class UpdateProductDTO(SQLModel):
    """
    Data transfer object for updating a product.
    """

    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0.0)
    description: Optional[str] = None
    category: Optional[ProductCategory] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name must not be empty')
        return v


class ProductOut(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category: ProductCategory


class ProductList(BaseListResponse[ProductOut]):
    """
    Response model for listing products with pagination.
    """

    items: Sequence[ProductOut] = Field(alias='products')

    class Config:
        populate_by_name = True


ProductList.model_rebuild()
