from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import decode

from projeto_aplicado.auth.password import get_password_hash, verify_password
from projeto_aplicado.auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


def test_password_hashing():
    password = 'testpassword123'
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('wrongpassword', hashed)


def test_password_hashing_empty_password():
    password = ''
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('wrongpassword', hashed)


def test_password_hashing_special_chars():
    password = '!@#$%^&*()'
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('wrongpassword', hashed)


def test_create_access_token():
    test_data = {'sub': 'test@example.com'}
    token = create_access_token(test_data)
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded['sub'] == 'test@example.com'
    assert 'exp' in decoded
    exp_time = datetime.fromtimestamp(decoded['exp'], tz=ZoneInfo('UTC'))
    expected_exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    assert (
        abs((exp_time - expected_exp).total_seconds()) < 60  # noqa: PLR2004
    )  # allow some clock drift


def test_create_access_token_with_additional_data():
    test_data = {'sub': 'test@example.com', 'role': 'admin'}
    token = create_access_token(test_data)
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded['sub'] == 'test@example.com'
    assert decoded['role'] == 'admin'
    assert 'exp' in decoded


def test_create_access_token_with_empty_data():
    test_data = {}
    token = create_access_token(test_data)
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert 'exp' in decoded
    assert 'sub' not in decoded
