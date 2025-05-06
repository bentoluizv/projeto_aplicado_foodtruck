from typing import List

from sqlmodel import Field, Relationship, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class Category(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=20, index=True, unique=True)
    icon_url: str = Field(nullable=False)
    products: List['Product'] = Relationship()  # type: ignore # noqa: F821

    @classmethod
    def create(cls, dto: 'CreateCategoryDTO'):  # type: ignore # noqa: F821
        return cls(**dto.model_dump())
