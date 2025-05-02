from typing import Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.category.model import Category
from projeto_aplicado.schemas import Pagination


class CreateCategoryDTO(SQLModel):
    name: str
    icon_url: str


class UpdateCategoryDTO(SQLModel):
    name: str | None = None


class CategoryList(SQLModel):
    categories: Sequence['Category']
    pagination: Pagination


CategoryList.model_rebuild()
