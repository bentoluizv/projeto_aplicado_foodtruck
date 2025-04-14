import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, StaticPool, create_engine

from projeto_aplicado.app import app
from projeto_aplicado.ext.database.db import create_all, drop_all, get_session
from projeto_aplicado.models.entities import Category


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(
        'sqlite+pysqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    return engine


@pytest.fixture
def session(engine):
    create_all(engine)

    with Session(engine) as session:
        yield session

    drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def categories(session: Session):
    categories = [
        {'name': 'Hambúrgueres'},
        {'name': 'Cachorros-quentes'},
        {'name': 'Bebidas'},
        {'name': 'Acompanhamentos'},
        {'name': 'Sobremesas'},
    ]
    categories = [Category(name=category['name']) for category in categories]
    session.add_all(categories)
    session.commit()
    return categories
