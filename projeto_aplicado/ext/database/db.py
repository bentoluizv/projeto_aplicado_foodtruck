from contextlib import contextmanager

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from projeto_aplicado.utils import get_db_url

from ...settings import get_settings

settings = get_settings()

url = get_db_url(settings)

config = {
    'url': url,
    'echo': settings.DB_ECHO,
}

engine = create_engine(**config)


def get_engine() -> Engine:
    """
    Retorna a instância do engine do banco de dados.

    :return: Engine.
    """
    return engine


@contextmanager
def get_session():
    """
    Retorna uma sessão de banco de dados.

    :return: Session.
    """
    session = Session(engine)

    try:
        yield session

    finally:
        session.close()


def create_all(engine: Engine):
    from projeto_aplicado.models import entities  # noqa: F401, PLC0415

    SQLModel.metadata.create_all(engine)


def drop_all(engine: Engine):
    SQLModel.metadata.drop_all(engine)
