from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from projeto_aplicado.auth.security import verify_password
from projeto_aplicado.resources.users.model import User, UserRole
from projeto_aplicado.resources.users.schemas import (
    CreateUserDTO,
    UpdateUserDTO,
)
from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_get_users(client: TestClient, users: list[User]):
    response = client.get(f'{API_PREFIX}/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert len(response.json()['users']) == len(users)
    assert response.json()['users'] == [
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
    assert response.json()['pagination'] == {
        'offset': 0,
        'limit': 100,
        'total_count': len(users),
        'page': 1,
        'total_pages': 1,
    }


def test_get_user_by_id(client: TestClient, users: list[User]):
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


def test_get_user_by_id_not_found(client: TestClient):
    response = client.get(f'{API_PREFIX}/users/99999999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'User not found'}


def test_create_user(client: TestClient):
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


def test_update_user(client: TestClient, users: list[User]):
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


def test_update_user_not_found(client: TestClient):
    data = {
        'name': 'Updated User',
        'email': 'updated@example.com',
        'role': UserRole.ATTENDANT,
    }
    response = client.patch(f'{API_PREFIX}/users/99999999', json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client: TestClient, users: list[User]):
    response = client.delete(f'{API_PREFIX}/users/{users[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'action': 'deleted', 'id': users[0].id}


def test_delete_user_not_found(client: TestClient):
    response = client.delete(f'{API_PREFIX}/users/99999999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'User not found'}


def test_create_user_dto_password_hashing():
    # Arrange
    password = 'test123'
    dto = CreateUserDTO(
        name='Test User',
        email='test@example.com',
        password=password,
        role=UserRole.KITCHEN,
    )

    # Assert
    assert dto.password != password  # Password should be hashed
    assert verify_password(
        password, dto.password
    )  # Should verify against original


def test_update_user_dto_password_hashing():
    # Arrange
    password = 'newpass123'
    dto = UpdateUserDTO(
        name='Updated User',
        email='updated@example.com',
        password=password,
        role=UserRole.KITCHEN,
    )

    # Assert
    assert dto.password is not None  # Password should be set
    assert dto.password != password  # Password should be hashed
    assert verify_password(
        password, dto.password
    )  # Should verify against original


def test_update_user_dto_password_optional():
    # Arrange
    dto = UpdateUserDTO(
        name='Updated User',
        email='updated@example.com',
        role=UserRole.KITCHEN,
    )

    # Assert
    assert (
        dto.password is None
    )  # Password should remain None when not provided


def test_create_user_dto_password_min_length():
    # Arrange & Act & Assert
    with pytest.raises(ValueError):  # noqa: PT011
        CreateUserDTO(
            name='Test User',
            email='test@example.com',
            password='12345',  # Too short
            role=UserRole.KITCHEN,
        )


def test_update_user_dto_password_min_length():
    # Arrange & Act & Assert
    with pytest.raises(ValueError):  # noqa: PT011
        UpdateUserDTO(
            name='Test User',
            email='test@example.com',
            password='12345',  # Too short
            role=UserRole.KITCHEN,
        )
