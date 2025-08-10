"""Integration tests for admin commands."""

from unittest.mock import Mock, patch

import pytest

from projeto_aplicado.cli.commands.admin import (
    CheckUserCommand,
    CreateAdminCommand,
    ListAdminsCommand,
)
from projeto_aplicado.cli.schemas import UserListResult, UserOperationResult
from projeto_aplicado.resources.user.model import User, UserRole


class TestCreateAdminCommand:
    """Integration tests for CreateAdminCommand."""

    def test_create_admin_success(self):
        """Test successful admin creation."""
        command = CreateAdminCommand()

        # Mock user data
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.username = 'testadmin'
        mock_user.email = 'admin@test.com'

        # Mock successful result
        mock_result = UserOperationResult(
            success=True, data=mock_user, error=None
        )

        with patch.object(
            command.user_service, 'create_admin', return_value=mock_result
        ):
            result = command.execute(
                username='testadmin',
                email='admin@test.com',
                password='password123',
                full_name='Test Admin',
                force=True,  # Skip confirmation
            )

            assert result == 0

            # Verify service was called with correct raw data
            command.user_service.create_admin.assert_called_once_with({
                'username': 'testadmin',
                'email': 'admin@test.com',
                'password': 'password123',
                'full_name': 'Test Admin',
            })

    def test_create_admin_validation_error(self):
        """Test admin creation with validation error."""
        command = CreateAdminCommand()

        # Mock validation error result
        mock_result = UserOperationResult(
            success=False,
            data=None,
            error='Validation error: Invalid email format',
        )

        with patch.object(
            command.user_service, 'create_admin', return_value=mock_result
        ):
            result = command.execute(
                username='testadmin',
                email='invalid-email',
                password='password123',
                full_name='Test Admin',
                force=True,
            )

            assert result == 1

    def test_create_admin_cancelled_by_user(self):
        """Test admin creation cancelled by user."""
        command = CreateAdminCommand()

        with patch.object(command, '_confirm_creation', return_value=False):
            result = command.execute(
                username='testadmin',
                email='admin@test.com',
                password='password123',
                full_name='Test Admin',
                force=False,
            )

            assert result == 0

    def test_create_admin_with_confirmation(self):
        """Test admin creation with user confirmation."""
        command = CreateAdminCommand()

        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.username = 'testadmin'
        mock_user.email = 'admin@test.com'

        mock_result = UserOperationResult(
            success=True, data=mock_user, error=None
        )

        with (
            patch.object(command, '_confirm_creation', return_value=True),
            patch.object(
                command.user_service, 'create_admin', return_value=mock_result
            ),
        ):
            result = command.execute(
                username='testadmin',
                email='admin@test.com',
                password='password123',
                full_name='Test Admin',
                force=False,
            )

            assert result == 0
            # Verify confirmation was called
            command._confirm_creation.assert_called_once()


class TestCheckUserCommand:
    """Integration tests for CheckUserCommand."""

    def test_check_user_found(self):
        """Test checking existing user."""
        command = CheckUserCommand()

        # Mock found user
        mock_user = Mock(spec=User)
        mock_user.username = 'testuser'
        mock_user.email = 'test@example.com'
        mock_user.role = UserRole.ADMIN
        mock_user.full_name = 'Test User'
        mock_user.created_at = '2024-01-01 10:00:00'

        mock_result = UserOperationResult(
            success=True, data=mock_user, error=None
        )

        with patch.object(
            command.user_service, 'check_user', return_value=mock_result
        ):
            result = command.execute(email='test@example.com')

            assert result == 0

            # Verify service was called with correct data
            command.user_service.check_user.assert_called_once_with({
                'email': 'test@example.com'
            })

    def test_check_user_not_found(self):
        """Test checking user that doesn't exist."""
        command = CheckUserCommand()

        # Service succeeds but returns None user data
        mock_result = UserOperationResult(success=True, data=None, error=None)

        with patch.object(
            command.user_service, 'check_user', return_value=mock_result
        ):
            result = command.execute(email='nonexistent@example.com')

            assert result == 1

    def test_check_user_service_error(self):
        """Test checking user with service error."""
        command = CheckUserCommand()

        mock_result = UserOperationResult(
            success=False, data=None, error='Database connection failed'
        )

        with patch.object(
            command.user_service, 'check_user', return_value=mock_result
        ):
            result = command.execute(email='test@example.com')

            assert result == 1

    def test_check_user_no_email(self):
        """Test checking user without email."""
        command = CheckUserCommand()

        result = command.execute(email=None)

        assert result == 1


class TestListAdminsCommand:
    """Integration tests for ListAdminsCommand."""

    def test_list_admins_found(self):
        """Test listing admin users when admins exist."""
        command = ListAdminsCommand()

        # Mock admin users
        mock_users = [
            Mock(
                spec=User,
                username='admin1',
                email='admin1@test.com',
                full_name='Admin One',
            ),
            Mock(
                spec=User,
                username='admin2',
                email='admin2@test.com',
                full_name='Admin Two',
            ),
        ]

        mock_result = UserListResult(success=True, data=mock_users, error=None)

        with patch.object(
            command.user_service, 'list_admins', return_value=mock_result
        ):
            result = command.execute()

            assert result == 0

            # Verify service was called
            command.user_service.list_admins.assert_called_once()

    def test_list_admins_none_found(self):
        """Test listing admin users when no admins exist."""
        command = ListAdminsCommand()

        mock_result = UserListResult(success=True, data=[], error=None)

        with patch.object(
            command.user_service, 'list_admins', return_value=mock_result
        ):
            result = command.execute()

            assert result == 0

    def test_list_admins_error(self):
        """Test listing admin users with service error."""
        command = ListAdminsCommand()

        mock_result = UserListResult(
            success=False, data=None, error='Database connection failed'
        )

        with patch.object(
            command.user_service, 'list_admins', return_value=mock_result
        ):
            result = command.execute()

            assert result == 1
