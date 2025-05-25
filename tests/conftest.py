import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, StaticPool, create_engine

from projeto_aplicado.app import app
from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order.model import Order, OrderItem
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.users.model import User, UserRole
from projeto_aplicado.utils import create_all, drop_all


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
def itens(session):
    itens = [
        {
            'name': 'X-Burguer',
            'price': 25.0,
            'image_url': 'image_x_burguer.jpg',
        },
        {
            'name': 'X-Salada',
            'price': 20.0,
            'image_url': 'image_x_salada.jpg',
        },
        {
            'name': 'Cachorro-quente',
            'price': 10.0,
            'image_url': 'image_cachorro_quente.jpg',
        },
        {
            'name': 'Refrigerante',
            'price': 5.0,
            'image_url': 'image_refrigerante.jpg',
        },
        {
            'name': 'Batata frita',
            'price': 8.0,
            'image_url': 'image_batata_frita.jpg',
        },
        {
            'name': 'Pudim',
            'price': 12.0,
            'image_url': 'image_pudim.jpg',
        },
    ]

    itens = [
        Product(
            name=item['name'],
            price=item['price'],
        )
        for item in itens
    ]
    session.add_all(itens)
    session.commit()
    return itens


@pytest.fixture
def orders(session):
    orders = [
        {
            'status': 'pending',
            'total': 0.0,
            'notes': 'First order',
        },
        {
            'status': 'completed',
            'total': 0.0,
            'notes': 'Second order',
        },
        {
            'status': 'cancelled',
            'total': 0.0,
            'notes': 'Third order',
        },
    ]
    orders = [Order(**order) for order in orders]
    session.add_all(orders)
    session.commit()
    return orders


@pytest.fixture
def order_items(session, orders, itens):
    order_items = [
        {
            'order_id': orders[0].id,
            'product_id': itens[0].id,
            'quantity': 2,
            'price': itens[0].price,
            'subtotal': itens[0].price * 2,
        },
        {
            'order_id': orders[0].id,
            'product_id': itens[2].id,
            'quantity': 1,
            'price': itens[2].price,
            'subtotal': itens[2].price,
        },
        {
            'order_id': orders[1].id,
            'product_id': itens[1].id,
            'quantity': 3,
            'price': itens[1].price,
            'subtotal': itens[1].price * 3,
        },
    ]
    order_items = [OrderItem(**item) for item in order_items]
    session.add_all(order_items)
    session.commit()
    return order_items


@pytest.fixture
def users(session):
    users = [
        {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'password',
            'role': UserRole.ATTENDANT,
        },
        {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'password': 'password',
            'role': UserRole.KITCHEN,
        },
    ]
    users = [User(**user) for user in users]
    session.add_all(users)
    session.commit()
    return users
