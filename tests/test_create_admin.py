"""Unit tests for create_admin script (core logic and safe CLI tests only)."""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.resources.user.schemas import CreateUserDTO
from projeto_aplicado.scripts.create_admin import create_admin_user, main


@pytest.fixture
def admin_dto():
    return CreateUserDTO(
        username='testadmin',
        email='admin@test.com',
        password='testpass123',
        role=UserRole.ADMIN,
        full_name='Test Admin',
    )


def test_create_admin_user_success(session, admin_dto):
    user = create_admin_user(session, admin_dto)
    assert user is not None
    assert user.username == admin_dto.username
    assert user.email == admin_dto.email
    assert user.role == UserRole.ADMIN
    assert user.full_name == admin_dto.full_name


def test_create_admin_user_duplicate(session, admin_dto):
    first_user = create_admin_user(session, admin_dto)
    assert first_user is not None
    second_user = create_admin_user(session, admin_dto)
    assert second_user is None
    users = session.query(User).filter(User.email == admin_dto.email).all()
    assert len(users) == 1


def test_create_admin_cli_success(session):
    runner = CliRunner()
    with patch(
        'projeto_aplicado.scripts.create_admin.get_engine'
    ) as mock_get_engine:
        mock_get_engine.return_value = session.get_bind()
        result = runner.invoke(
            main,
            input='testadmin\ntest@example.com\ntestpass123\nTest Admin\n',
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert 'created successfully' in result.output
    user = session.query(User).filter(User.email == 'test@example.com').first()
    assert user is not None
    assert user.username == 'testadmin'
    assert user.full_name == 'Test Admin'


def test_create_admin_cli_duplicate(session):
    runner = CliRunner()
    with patch(
        'projeto_aplicado.scripts.create_admin.get_engine'
    ) as mock_get_engine:
        mock_get_engine.return_value = session.get_bind()
        # Create first user
        runner.invoke(
            main,
            input='testadmin\ntest@example.com\ntestpass123\nTest Admin\n',
            catch_exceptions=False,
        )
        # Try to create duplicate
        result = runner.invoke(
            main,
            input='testadmin2\ntest@example.com\ntestpass123\nTest Admin 2\n',
            catch_exceptions=False,
        )
    assert result.exit_code == 1
    assert 'already exists' in result.output
