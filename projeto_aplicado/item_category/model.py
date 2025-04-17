from sqlmodel import Field, Relationship, SQLModel

from projeto_aplicado.data.utils import get_ulid_as_str


class ItemCategory(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=20, index=True, unique=True)
    icon_url: str = Field(nullable=False)
    itens: list['Item'] = Relationship(back_populates='category')


from projeto_aplicado.item.model import Item  # noqa: E402, PLC0415

ItemCategory.model_rebuild()
