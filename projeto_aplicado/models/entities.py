from sqlalchemy import Engine, MetaData
from sqlmodel import Field, Relationship, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class Category(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=20, index=True, unique=True)
    itens: list['Item'] = Relationship(back_populates='category')
    icon_url: str = Field(nullable=False)


class Item(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=80, index=True)
    description: str | None = Field(default=None, max_length=255)
    price: float = Field(nullable=False, gt=0.0)
    image: bytes | None = Field(default=None)
    category_id: str = Field(foreign_key='category.id')
    category: Category = Relationship(back_populates='itens')


def create_all(engine: Engine):
    """
    Cria todas as tabelas do banco de dados.
    :param engine: Engine do banco de dados.
    """
    SQLModel.metadata.create_all(engine)


def drop_all(engine: Engine):
    """
    Remove todas as tabelas do banco de dados.
    :param engine: Engine do banco de dados.
    """
    SQLModel.metadata.drop_all(engine)


def get_metadata() -> MetaData:
    """
    Retorna a instância do metadata do SQLModel.

    :return: Metadata do SQLModel.
    """
    return SQLModel.metadata
