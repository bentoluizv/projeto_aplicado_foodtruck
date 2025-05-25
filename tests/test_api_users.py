from http import HTTPStatus

from projeto_aplicado.resources.users.model import UserRole
from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_get_users(client, users):
    response = client.get(f'{API_PREFIX}/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert len(response.json()['items']) == len(users)
    assert response.json()['items'] == [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role.value,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat(),
        }
        for user in users
    ]


def test_get_user_by_id(client, users):
    response = client.get(f'{API_PREFIX}/users/{users[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {
        'id': users[0].id,
        'name': users[0].name,
        'email': users[0].email,
        'role': users[0].role.value,
        'created_at': users[0].created_at.isoformat(),
        'updated_at': users[0].updated_at.isoformat(),
    }


def test_get_user_by_id_not_found(client):
    response = client.get(f'{API_PREFIX}/users/99999999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'User not found'}


def test_create_user(client):
    data = {
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'password123',
        'role': UserRole.KITCHEN,
    }
    response = client.post(f'{API_PREFIX}/users/', json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['name'] == data['name']
    assert response.json()['email'] == data['email']
    assert response.json()['role'] == data['role'].value


def test_update_user(client, users):
    data = {
        'name': 'Updated User',
        'email': 'updated@example.com',
        'role': UserRole.ATTENDANT,
    }
    response = client.patch(f'{API_PREFIX}/users/{users[0].id}', json=data)
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['name'] == data['name']
    assert response.json()['email'] == data['email']
    assert response.json()['role'] == data['role'].value


def test_update_user_not_found(client):
    data = {
        'name': 'Updated User',
        'email': 'updated@example.com',
        'role': UserRole.ATTENDANT,
    }
    response = client.patch(f'{API_PREFIX}/users/99999999', json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, users):
    response = client.delete(f'{API_PREFIX}/users/{users[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'action': 'deleted', 'id': users[0].id}


def test_delete_user_not_found(client):
    response = client.delete(f'{API_PREFIX}/users/99999999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'User not found'}
