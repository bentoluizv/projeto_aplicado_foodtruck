import random
import string

from sqlalchemy import Engine
from sqlmodel import MetaData, SQLModel
from ulid import ULID

from projeto_aplicado.settings import Settings


def get_ulid_as_str():
    """
    Retorna um ULID único.

    :return: str.
    """

    return str(ULID())


def get_db_url(settings: Settings, cli: bool = False):
    """
    Retorna a URL de conexão com o banco de dados.

    :return: str.
    """

    if cli:
        url = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME_CLI}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
    else:
        url = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'

    return url


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


def generate_locator():
    """
    Gera um localizador composto por uma letra e três números.
    :return: str.
    """
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(string.digits, k=3))
    return f'{letter}{numbers}'
