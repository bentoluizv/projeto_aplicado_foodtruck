from http import HTTPStatus

from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_token_endpoint_success(client, admin_headers):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin@example.com',
            'password': 'password',
        },
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_token_endpoint_success_kitchen(client, kitchen_headers):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'jane.doe@example.com',
            'password': 'password',
        },
        headers=kitchen_headers,
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_token_endpoint_success_attendant(client, attendant_headers):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'john.doe@example.com',
            'password': 'password',
        },
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_token_endpoint_invalid_credentials(client, admin_headers):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin@example.com',
            'password': 'wrongpassword',
        },
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect email or password'
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'nonexistent@example.com',
            'password': 'password',
        },
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect email or password'


def test_token_endpoint_missing_fields(client, admin_headers):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin@example.com',
        },
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
