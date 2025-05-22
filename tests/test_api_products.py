from http import HTTPStatus

from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_get_products(client, itens):
    response = client.get(f'{API_PREFIX}/products/')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert len(response.json()['products']) == len(itens)
    assert response.json()['products'] == [
        {
            'id': str(item.id),
            'description': item.description,
            'name': item.name,
            'price': item.price,
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat(),
        }
        for item in itens
    ]


def test_get_product_by_id_not_found(client):
    response = client.get(f'{API_PREFIX}/products/nonexistent-id')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product not found'


def test_create_product(client):
    data = {
        'name': 'Test Item',
        'description': 'Test Description',
        'price': 10.99,
    }

    response = client.post(f'{API_PREFIX}/products/', json=data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'created'
    assert response.json()['id'] is not None


def test_create_product_conflict(client, itens):
    data = {
        'name': itens[0].name,
        'description': 'Test Description',
        'price': 10.99,
    }

    response = client.post(
        f'{API_PREFIX}/products/',
        json=data,
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product already exists'


def test_update_product(client, itens):
    payload = {'name': 'Updated Item', 'price': 1599.99}
    response = client.patch(
        f'{API_PREFIX}/products/{itens[0].id}', json=payload
    )

    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'updated'
    assert response.json()['id'] == itens[0].id


def test_update_product_not_found(client):
    update_payload = {'name': 'Nonexistent Item', 'price': 20.99}
    response = client.patch(
        f'{API_PREFIX}/products/nonexistent-id', json=update_payload
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product not found'


def test_delete_product(client, itens):
    response = client.delete(f'{API_PREFIX}/products/{itens[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'deleted'
    assert response.json()['id'] == itens[0].id


def test_delete_product_not_found(client):
    response = client.delete(f'{API_PREFIX}/products/nonexistent-id')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Product not found'
