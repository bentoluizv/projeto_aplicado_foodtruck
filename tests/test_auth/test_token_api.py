from http import HTTPStatus

from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_token_endpoint_success(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_token_endpoint_success_kitchen(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'janedoe',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_token_endpoint_success_attendant(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'johndoe',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_token_endpoint_invalid_credentials(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin',
            'password': 'wrongpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect username or password'
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'nonexistent',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect username or password'


def test_token_endpoint_missing_fields(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response = client.post(
        f'{API_PREFIX}/token/',
        data={},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_token_endpoint_invalid_content_type(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        json={  # Using json instead of form data
            'username': 'admin',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_token_endpoint_empty_credentials(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': '',
            'password': '',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_token_endpoint_whitespace_credentials(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': '   ',
            'password': '   ',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_token_endpoint_special_chars_credentials(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin',
            'password': '!@#$%^&*()',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_endpoint_long_credentials(client, users):
    long_username = 'a' * 256
    long_password = 'b' * 256
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': long_username,
            'password': long_password,
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_endpoint_case_sensitive_username(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'ADMIN',  # Different case
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_endpoint_case_sensitive_password(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin',
            'password': 'PASSWORD',  # Different case
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_endpoint_with_extra_fields(client, users):
    response = client.post(
        f'{API_PREFIX}/token/',
        data={
            'username': 'admin',
            'password': 'password',
            'extra_field': 'should_be_ignored',
        },
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
