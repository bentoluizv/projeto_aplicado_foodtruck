from sqlmodel import Field, Relationship, SQLModel

from ...utils import get_ulid_as_str


class Product(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=80, index=True)
    description: str | None = Field(default=None, max_length=255)
    price: float = Field(nullable=False, gt=0.0)
    image_url: str = Field(nullable=False, max_length=255)
    category_id: str = Field(foreign_key='category.id')
    category: 'Category' = Relationship(back_populates='products')  # type: ignore # noqa: F821
    order_items: list['OrderItem'] = Relationship(back_populates='product')  # type: ignore # noqa: F821
