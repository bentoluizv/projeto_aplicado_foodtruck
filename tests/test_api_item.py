from http import HTTPStatus
from io import BytesIO

from projeto_aplicado.settings import get_settings

settings = get_settings()

API_PREFIX = settings.API_PREFIX


def test_get_products(client, itens):
    response = client.get(f'{API_PREFIX}/products/')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == len(itens)
    assert response.json()['products'] == [
        {
            'id': str(item.id),
            'description': item.description,
            'image_url': item.image_url,
            'name': item.name,
            'price': item.price,
            'category_id': item.category_id,
        }
        for item in itens
    ]


def test_get_item_by_id_not_found(client):
    response = client.get(f'{API_PREFIX}/itens/nonexistent-id')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Not Found'


def test_create_item(client, categories):
    file_content = BytesIO(b'fake image content')

    data = {
        'name': 'Test Item',
        'description': 'Test Description',
        'price': 10.99,
        'category_id': categories[0].id,
    }

    response = client.post(
        f'{API_PREFIX}/products/', data=data, files={'image': file_content}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['action'] == 'created'
    assert response.json()['id'] is not None


def test_create_products_conflict(client, itens):
    file_content = BytesIO(b'fake image content')

    data = {
        'name': itens[0].name,
        'description': 'Test Description',
        'price': 10.99,
        'category_id': itens[0].category_id,
    }

    response = client.post(
        f'{API_PREFIX}/products/', data=data, files={'image': file_content}
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Product already exists'


def test_update_item(client, itens):
    payload = {'name': 'Updated Item', 'price': 1599.99}
    response = client.patch(
        f'{API_PREFIX}/products/{itens[0].id}', json=payload
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['action'] == 'updated'
    assert response.json()['id'] == itens[0].id


def test_update_item_not_found(client):
    update_payload = {'name': 'Nonexistent Item', 'price': 20.99}
    response = client.patch(
        f'{API_PREFIX}/itens/nonexistent-id', json=update_payload
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Not Found'


def test_delete_item(client, itens):
    response = client.delete(f'{API_PREFIX}/products/{itens[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['action'] == 'deleted'
    assert response.json()['id'] == itens[0].id


def test_delete_item_not_found(client):
    response = client.delete(f'{API_PREFIX}/itens/nonexistent-id')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Not Found'
