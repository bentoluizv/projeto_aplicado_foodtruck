from sqlmodel import Field, Relationship, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class Category(SQLModel, table=True):
    id: str | None = Field(
        default=None, default_factory=get_ulid_as_str, primary_key=True
    )
    name: str
    description: str | None = None
    itens: list['Item'] = Relationship(back_populates='category')


class Item(SQLModel, table=True):
    id: str | None = Field(
        default=None, default_factory=get_ulid_as_str, primary_key=True
    )
    name: str = Field(max_length=80, index=True)
    description: str | None = Field(default=None, max_length=255)
    price: float = Field(nullable=False, gt=0.0)
    image: bytes | None = Field(default=None)
    category_id: int | None = Field(default=None, foreign_key='category.id')
    category: Category = Relationship(back_populates='itens')
