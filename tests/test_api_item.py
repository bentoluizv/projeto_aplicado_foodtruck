from http import HTTPStatus

from projeto_aplicado.settings import get_settings

settings = get_settings()

API_PREFIX = settings.API_PREFIX


def test_get_itens(client, itens):
    response = client.get(f'{API_PREFIX}/itens/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(itens)


def test_get_item_by_id_not_found(client):
    response = client.get(f'{API_PREFIX}/itens/nonexistent-id')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Item with nonexistent-id not found'


def test_create_item(client, categories):
    payload = {
        'name': 'Test Item',
        'price': 10.99,
        'category_id': categories[0].id,
    }
    response = client.post(f'{API_PREFIX}/itens/', json=payload)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['action'] == 'created'
    assert response.json()['id'] is not None


def test_create_item_conflict(client, itens):
    payload = {
        'name': itens[0].name,
        'price': itens[0].price,
        'category_id': itens[0].category_id,
    }
    response = client.post(f'{API_PREFIX}/itens/', json=payload)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Item already exists'


def test_update_item(client, itens):
    payload = {'name': 'Updated Item', 'price': 1599.99}
    response = client.patch(f'{API_PREFIX}/itens/{itens[0].id}', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json()['action'] == 'updated'
    assert response.json()['id'] == itens[0].id


def test_update_item_not_found(client):
    update_payload = {'name': 'Nonexistent Item', 'price': 20.99}
    response = client.patch(
        f'{API_PREFIX}/itens/nonexistent-id', json=update_payload
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Item not found'


def test_delete_item(client, itens):
    response = client.delete(f'{API_PREFIX}/itens/{itens[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['action'] == 'deleted'
    assert response.json()['id'] == itens[0].id


def test_delete_item_not_found(client):
    response = client.delete(f'{API_PREFIX}/itens/nonexistent-id')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Item not found'
