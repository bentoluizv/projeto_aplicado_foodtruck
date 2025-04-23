from sqlmodel import Field, Relationship, SQLModel

from projeto_aplicado.data.utils import get_ulid_as_str


class Category(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=20, index=True, unique=True)
    icon_url: str = Field(nullable=False)
    products: list['Product'] = Relationship(back_populates='category')


from projeto_aplicado.resources.product.model import (  # noqa: E402, PLC0415
    Product,
)

Category.model_rebuild()
