import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, StaticPool, create_engine

from projeto_aplicado.app import app
from projeto_aplicado.data.utils import create_all, drop_all
from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.category.model import Category
from projeto_aplicado.resources.product.model import Product


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
    create_all(engine)  # noqa: F821

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
        {'name': 'Hambúrgueres', 'icon_url': 'i'},
        {'name': 'Cachorros-quentes', 'icon_url': 'i'},
        {'name': 'Bebidas', 'icon_url': 'i'},
        {'name': 'Acompanhamentos', 'icon_url': 'i'},
        {'name': 'Sobremesas', 'icon_url': 'i'},
    ]
    categories = [
        Category(name=category['name'], icon_url=category['icon_url'])
        for category in categories
    ]
    session.add_all(categories)
    session.commit()
    return categories


@pytest.fixture
def itens(session, categories):
    itens = [
        {
            'name': 'X-Burguer',
            'price': 25.0,
            'category_id': categories[0].id,
            'image_url': 'image_x_burguer.jpg',
        },
        {
            'name': 'X-Salada',
            'price': 20.0,
            'category_id': categories[0].id,
            'image_url': 'image_x_salada.jpg',
        },
        {
            'name': 'Cachorro-quente',
            'price': 10.0,
            'category_id': categories[1].id,
            'image_url': 'image_cachorro_quente.jpg',
        },
        {
            'name': 'Refrigerante',
            'price': 5.0,
            'category_id': categories[2].id,
            'image_url': 'image_refrigerante.jpg',
        },
        {
            'name': 'Batata frita',
            'price': 8.0,
            'category_id': categories[3].id,
            'image_url': 'image_batata_frita.jpg',
        },
        {
            'name': 'Pudim',
            'price': 12.0,
            'category_id': categories[4].id,
            'image_url': 'image_pudim.jpg',
        },
    ]

    itens = [
        Product(
            name=item['name'],
            price=item['price'],
            category_id=item['category_id'],
            image_url=item['image_url'],
        )
        for item in itens
    ]
    session.add_all(itens)
    session.commit()
    return itens
