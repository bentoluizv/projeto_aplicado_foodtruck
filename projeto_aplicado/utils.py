from ulid import ULID

from projeto_aplicado.settings import Settings


def get_ulid_as_str():
    """
    Retorna um ULID único.

    :return: str.
    """

    return str(ULID())


def get_db_url(settings: Settings):
    """
    Retorna a URL de conexão com o banco de dados.

    :return: str.
    """
    url = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'

    return url
