import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, StaticPool, create_engine
from testcontainers.postgres import PostgresContainer

from projeto_aplicado.app import app
from projeto_aplicado.auth.password import get_password_hash
from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order.model import Order, OrderItem
from projeto_aplicado.resources.product.enums import ProductCategory
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.users.model import User, UserRole
from projeto_aplicado.settings import get_settings
from projeto_aplicado.utils import create_all, drop_all

settings = get_settings()


@pytest.fixture(scope='session')
def postgres_container():
    """Start the Postgres test container."""
    container = PostgresContainer(
        'postgres:16',
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        dbname=settings.POSTGRES_DB,
        driver='psycopg2',
    )
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope='session')
def engine(postgres_container):
    engine = create_engine(
        postgres_container.get_connection_url(),
        echo=settings.DB_ECHO,
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
            'category': ProductCategory.FOOD,
        },
        {
            'name': 'X-Salada',
            'price': 20.0,
            'image_url': 'image_x_salada.jpg',
            'category': ProductCategory.FOOD,
        },
        {
            'name': 'Cachorro-quente',
            'price': 10.0,
            'image_url': 'image_cachorro_quente.jpg',
            'category': ProductCategory.FOOD,
        },
        {
            'name': 'Refrigerante',
            'price': 5.0,
            'image_url': 'image_refrigerante.jpg',
            'category': ProductCategory.DRINK,
        },
        {
            'name': 'Batata frita',
            'price': 8.0,
            'image_url': 'image_batata_frita.jpg',
            'category': ProductCategory.SNACK,
        },
        {
            'name': 'Pudim',
            'price': 12.0,
            'image_url': 'image_pudim.jpg',
            'category': ProductCategory.DESSERT,
        },
    ]

    itens = [
        Product(
            name=item['name'],
            price=item['price'],
            category=item['category'],
        )
        for item in itens
    ]
    session.add_all(itens)
    session.commit()
    return itens


@pytest.fixture
def products(itens):
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
            'password': get_password_hash('password'),
            'role': UserRole.ATTENDANT,
        },
        {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'password': get_password_hash('password'),
            'role': UserRole.KITCHEN,
        },
        {
            'name': 'Admin',
            'email': 'admin@example.com',
            'password': get_password_hash('password'),
            'role': UserRole.ADMIN,
        },
    ]
    users = [User(**user) for user in users]
    session.add_all(users)
    session.commit()
    return users


@pytest.fixture
def admin_headers(client, users):
    response = client.post(
        f'{settings.API_PREFIX}/token/',
        data={'username': users[2].email, 'password': 'password'},
    )
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    return headers


@pytest.fixture
def kitchen_headers(client, users):
    response = client.post(
        f'{settings.API_PREFIX}/token/',
        data={'username': users[1].email, 'password': 'password'},
    )
    headers = {'Authorization': f'Bearer {response.json()["access_token"]}'}
    return headers


@pytest.fixture
def attendant_headers(client, users):
    response = client.post(
        f'{settings.API_PREFIX}/token/',
        data={'username': users[0].email, 'password': 'password'},
    )
    headers = {'Authorization': f'Bearer {response.json()["access_token"]}'}
    return headers
