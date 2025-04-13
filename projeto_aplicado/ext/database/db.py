from contextlib import contextmanager

from sqlmodel import Session, create_engine

from projeto_aplicado.utils import get_db_url

from ...settings import get_settings

settings = get_settings()

url = get_db_url(settings)

config = {
    'url': url,
    'echo': settings.DB_ECHO,
}

engine = create_engine(**config)


def get_engine():
    """
    Retorna uma engine de banco de dados.

    :return: engine.
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
