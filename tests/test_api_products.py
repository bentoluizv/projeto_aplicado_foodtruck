from http import HTTPStatus

from fastapi.testclient import TestClient

from projeto_aplicado.resources.product.enums import ProductCategory
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_get_products(client, itens, admin_headers):
    response = client.get(f'{API_PREFIX}/products/', headers=admin_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert len(response.json()['products']) == len(itens)
    assert response.json()['products'] == [
        {
            'id': str(item.id),
            'description': item.description,
            'name': item.name,
            'price': item.price,
            'category': item.category,
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat(),
        }
        for item in itens
    ]


def test_get_product_by_id_not_found(client, admin_headers):
    response = client.get(
        f'{API_PREFIX}/products/nonexistent-id', headers=admin_headers
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product not found'


def test_create_product(client, admin_headers):
    data = {
        'name': 'Test Item',
        'description': 'Test Description',
        'price': 10.99,
        'category': 'FOOD',
    }
    response = client.post(
        f'{API_PREFIX}/products/', json=data, headers=admin_headers
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'created'
    assert response.json()['id'] is not None


def test_create_product_conflict(client, itens, admin_headers):
    data = {
        'name': itens[0].name,
        'description': 'Test Description',
        'price': 10.99,
        'category': itens[0].category.value,
    }
    response = client.post(
        f'{API_PREFIX}/products/',
        json=data,
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product already exists'


def test_update_product(client, itens, admin_headers):
    payload = {'name': 'Updated Item', 'price': 1599.99}
    response = client.patch(
        f'{API_PREFIX}/products/{itens[0].id}',
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'updated'
    assert response.json()['id'] == itens[0].id


def test_update_product_not_found(client, admin_headers):
    update_payload = {'name': 'Nonexistent Item', 'price': 20.99}
    response = client.patch(
        f'{API_PREFIX}/products/nonexistent-id',
        json=update_payload,
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product not found'


def test_delete_product(client, itens, admin_headers):
    response = client.delete(
        f'{API_PREFIX}/products/{itens[0].id}', headers=admin_headers
    )
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'deleted'
    assert response.json()['id'] == itens[0].id


def test_delete_product_not_found(client, admin_headers):
    response = client.delete(
        f'{API_PREFIX}/products/nonexistent-id', headers=admin_headers
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product not found'


def test_kitchen_cannot_access_products_api(client, kitchen_headers):
    response = client.get(f'{API_PREFIX}/products/', headers=kitchen_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'


def test_attendant_cannot_access_products_api(client, attendant_headers):
    response = client.get(f'{API_PREFIX}/products/', headers=attendant_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'


def test_get_products_unauthorized(
    client: TestClient, products: list[Product]
):
    response = client.get(f'{API_PREFIX}/products/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_products_invalid_token(
    client: TestClient, products: list[Product]
):
    response = client.get(
        f'{API_PREFIX}/products/',
        headers={'Authorization': 'Bearer invalid_token'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_product_with_invalid_price(client: TestClient, admin_headers):
    data = {
        'name': 'New Product',
        'description': 'A new product',
        'price': -10.0,  # Invalid negative price
        'category': ProductCategory.FOOD,
    }
    response = client.post(
        f'{API_PREFIX}/products/', json=data, headers=admin_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_product_with_invalid_category(
    client: TestClient, admin_headers
):
    data = {
        'name': 'New Product',
        'description': 'A new product',
        'price': 10.0,
        'category': 'INVALID_CATEGORY',
    }
    response = client.post(
        f'{API_PREFIX}/products/', json=data, headers=admin_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_product_with_missing_required_fields(
    client: TestClient, admin_headers
):
    data = {
        'name': 'New Product',
        # Missing description, price, and category
    }
    response = client.post(
        f'{API_PREFIX}/products/', json=data, headers=admin_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_product_with_invalid_price(
    client: TestClient, products: list[Product], admin_headers
):
    data = {
        'name': 'Updated Product',
        'description': 'An updated product',
        'price': -5.0,  # Invalid negative price
        'category': ProductCategory.DRINK,
    }
    response = client.patch(
        f'{API_PREFIX}/products/{products[0].id}',
        json=data,
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_product_with_invalid_category(
    client: TestClient, products: list[Product], admin_headers
):
    data = {
        'name': 'Updated Product',
        'description': 'An updated product',
        'price': 5.0,
        'category': 'INVALID_CATEGORY',
    }
    response = client.patch(
        f'{API_PREFIX}/products/{products[0].id}',
        json=data,
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_kitchen_cannot_create_product(client: TestClient, kitchen_headers):
    data = {
        'name': 'New Product',
        'description': 'A new product',
        'price': 10.0,
        'category': ProductCategory.FOOD,
    }
    response = client.post(
        f'{API_PREFIX}/products/', json=data, headers=kitchen_headers
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_attendant_cannot_create_product(
    client: TestClient, attendant_headers
):
    data = {
        'name': 'New Product',
        'description': 'A new product',
        'price': 10.0,
        'category': ProductCategory.FOOD,
    }
    response = client.post(
        f'{API_PREFIX}/products/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
