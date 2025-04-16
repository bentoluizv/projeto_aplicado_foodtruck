from http import HTTPStatus

from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_get_categories(client, categories):
    response = client.get(f'{API_PREFIX}/categories/')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == len(categories)
    assert response.json() == [
        {
            'id': category.id,
            'name': category.name,
            'icon_url': category.icon_url,
        }
        for category in categories
    ]


def test_get_category_by_id(client, categories):
    response = client.get(f'{API_PREFIX}/categories/{categories[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': str(categories[0].id),
        'name': categories[0].name,
        'icon_url': categories[0].icon_url,
    }


def test_get_category_by_id_not_found(client, categories):
    response = client.get(f'{API_PREFIX}/categories/99999999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Category with 99999999 not found'}


def test_create_category(client):
    data = {'name': 'New Category', 'icon_url': 'icon_url_value'}
    response = client.post(f'{API_PREFIX}/categories/', json=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['action'] == 'created'


def test_create_category_conflict(client, categories):
    data = {'name': categories[0].name, 'icon_url': 'icon_url_value'}
    response = client.post(f'{API_PREFIX}/categories/', json=data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Category already exists'}


def test_update_category(client, categories):
    data = {'name': 'Updated Category', 'icon_url': 'updated_icon_url_value'}
    response = client.patch(
        f'{API_PREFIX}/categories/{categories[0].id}', json=data
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['action'] == 'updated'


def test_update_category_not_found(client):
    data = {'name': 'Updated Category', 'icon_url': 'updated_icon_url_value'}
    response = client.patch(f'{API_PREFIX}/categories/1', json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Category not found'}


def test_delete_category(client, categories):
    response = client.delete(f'{API_PREFIX}/categories/{categories[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['action'] == 'deleted'


def test_delete_category_not_found(client):
    response = client.delete(f'{API_PREFIX}/categories/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Category not found',
    }
