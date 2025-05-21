from typing import Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.category.model import Category
from projeto_aplicado.schemas import Pagination


class CreateCategoryDTO(SQLModel):
    """
    Data transfer object for creating a category.
    """

    name: str
    icon_url: str


class UpdateCategoryDTO(SQLModel):
    """
    Data transfer object for updating a category.
    """

    name: str | None = None
    icon_url: str | None = None


class CategoryList(SQLModel):
    """
    Response model for listing categories with pagination.
    """

    categories: Sequence[Category]
    pagination: Pagination
