from sqlmodel import Field, Relationship, SQLModel

from ..data.utils import get_ulid_as_str


class Item(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=80, index=True)
    description: str | None = Field(default=None, max_length=255)
    price: float = Field(nullable=False, gt=0.0)
    image: bytes | None = Field(default=None)
    category_id: str = Field(foreign_key='itemcategory.id')
    category: 'ItemCategory' = Relationship(back_populates='itens')


from projeto_aplicado.item_category.model import (  # noqa: E402, PLC0415
    ItemCategory,
)

Item.model_rebuild()
