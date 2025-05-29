from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

import pytest
from jwt import decode

from projeto_aplicado.auth.password import get_password_hash, verify_password
from projeto_aplicado.auth.security import create_access_token
from projeto_aplicado.settings import get_settings

settings = get_settings()


def test_password_hashing():
    password = 'test_password'
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('wrong_password', hashed)


def test_password_hashing_empty_password():
    with pytest.raises(ValueError, match='Password cannot be empty'):
        get_password_hash('')


def test_password_hashing_none_password():
    with pytest.raises(ValueError, match='Password must be a string'):
        get_password_hash(None)  # type: ignore


def test_password_hashing_non_string_password():
    with pytest.raises(ValueError, match='Password must be a string'):
        get_password_hash(123)  # type: ignore


def test_verify_password_empty_password():
    assert not verify_password('', 'hashed_password')


def test_verify_password_none_password():
    assert not verify_password(None, 'hashed_password')  # type: ignore
    assert not verify_password('password', None)  # type: ignore


def test_verify_password_non_string_password():
    assert not verify_password(123, 'hashed_password')  # type: ignore
    assert not verify_password('password', 123)  # type: ignore


def test_create_access_token():
    test_data = {'sub': 'test_user', 'role': 'admin'}
    token = create_access_token(test_data)
    assert token is not None
    assert isinstance(token, str)


def test_create_access_token_with_additional_data():
    test_data = {'sub': 'test_user', 'role': 'admin', 'extra': 'data'}
    token = create_access_token(test_data)
    assert token is not None
    assert isinstance(token, str)


def test_create_access_token_with_empty_data():
    test_data = {}
    token = create_access_token(test_data)
    assert token is not None
    assert isinstance(token, str)


def test_create_access_token_with_none_values():
    test_data = {'sub': 'test_user', 'role': None}
    token = create_access_token(test_data)
    assert token is not None
    assert isinstance(token, str)


def test_password_hashing_special_chars():
    password = '!@#$%^&*()'
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('wrongpassword', hashed)


def test_create_access_token_with_special_chars():
    test_data = {'sub': 'test@example.com', 'role': 'admin!@#$%^&*()'}
    token = create_access_token(test_data)
    decoded = decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    assert decoded['sub'] == 'test@example.com'
    assert decoded['role'] == 'admin!@#$%^&*()'
    assert 'exp' in decoded


def test_create_access_token_with_unicode():
    test_data = {'sub': 'test@example.com', 'role': 'admin-áéíóú'}
    token = create_access_token(test_data)
    decoded = decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    assert decoded['sub'] == 'test@example.com'
    assert decoded['role'] == 'admin-áéíóú'
    assert 'exp' in decoded


def test_create_access_token_with_long_data():
    long_string = 'a' * 1000
    test_data = {'sub': 'test@example.com', 'data': long_string}
    token = create_access_token(test_data)
    decoded = decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    assert decoded['sub'] == 'test@example.com'
    assert decoded['data'] == long_string
    assert 'exp' in decoded
