"""Tests for CLI commands following clean architecture principles."""

from unittest.mock import Mock, patch

from rich.console import Console

from projeto_aplicado.cli.commands.admin import (
    CheckUserCommand,
    CreateAdminCommand,
    ListAdminsCommand,
)
from projeto_aplicado.cli.commands.health import HealthCommand
from projeto_aplicado.resources.user.model import UserRole


class TestHealthCommand:
    """Test HealthCommand following SOLID principles."""

    def test_initialization(self):
        """Test HealthCommand initialization."""
        command = HealthCommand()
        assert command.console is not None
        assert hasattr(command, 'database_service')
        assert hasattr(command, 'user_service')
        assert hasattr(command, 'health_service')

    def test_initialization_with_custom_db_host(self):
        """Test HealthCommand initialization with custom database host."""
        command = HealthCommand(db_host='postgres')
        assert command.database_service.db_host == 'postgres'

    def test_initialization_with_custom_console(self):
        """Test HealthCommand initialization with custom console."""
        console = Console()
        command = HealthCommand(console=console)
        assert command.console == console

    def test_execute_all_checks_pass(self):
        """Test execute method with all health checks passing."""
        command = HealthCommand()

        # Mock the health service to return successful results
        mock_result = {
            'passed': 3,
            'total': 3,
            'success': True,
            'details': [
                ('Database Connection', True, 'Database connection: OK'),
                ('Admin Users', True, 'Admin users: 2 found'),
                ('Settings', True, 'Settings loaded: OK'),
            ],
            'database_info': {
                'database': 'foodtruck',
                'host': 'localhost',
                'port': '5432'
            }
        }

        with patch.object(command.health_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()

            assert exit_code == 0  # Success

    def test_execute_some_checks_fail(self):
        """Test execute method with some health checks failing."""
        command = HealthCommand()

        # Mock the health service to return mixed results
        mock_result = {
            'passed': 2,
            'total': 3,
            'success': False,
            'details': [
                ('Database Connection', False, 'Database connection: FAILED'),
                ('Admin Users', True, 'Admin users: 1 found'),
                ('Settings', True, 'Settings loaded: OK'),
            ],
            'database_info': {
                'database': 'foodtruck',
                'host': 'localhost',
                'port': '5432'
            }
        }

        with patch.object(command.health_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()

            assert exit_code == 1  # Failure


class TestCreateAdminCommand:
    """Test CreateAdminCommand following SOLID principles."""

    def test_initialization(self):
        """Test CreateAdminCommand initialization."""
        command = CreateAdminCommand()
        assert command.console is not None
        assert hasattr(command, 'database_service')
        assert hasattr(command, 'user_service')

    def test_initialization_with_custom_db_host(self):
        """Test CreateAdminCommand initialization with custom database host."""
        command = CreateAdminCommand(db_host='postgres')
        assert command.database_service.db_host == 'postgres'

    def test_execute_success(self):
        """Test execute method with successful user creation."""
        command = CreateAdminCommand()

        # Mock successful validation and creation
        mock_user = Mock()
        mock_user.username = 'testuser'
        mock_user.id = 'test-id-123'

        with patch.object(command.user_service, 'validate_input', return_value=True), \
             patch.object(command.user_service, 'execute_operation', return_value=mock_user), \
             patch.object(command, '_confirm_creation', return_value=True):

            exit_code = command.execute(
                username='testuser',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=False
            )

            assert exit_code == 0

    def test_execute_validation_failure(self):
        """Test execute method with validation failure."""
        command = CreateAdminCommand()

        with patch.object(command.user_service, 'validate_input', return_value=False):
            exit_code = command.execute(
                username='',  # Invalid username
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=True
            )

            assert exit_code == 1

    def test_execute_user_already_exists(self):
        """Test execute method when user already exists."""
        command = CreateAdminCommand()

        with patch.object(command.user_service, 'validate_input', return_value=True), \
             patch.object(command.user_service, 'execute_operation', return_value=None):  # None = already exists

            exit_code = command.execute(
                username='testuser',
                email='existing@example.com',
                password='password123',
                full_name='Test User',
                force=True
            )

            assert exit_code == 1

    def test_execute_with_exception(self):
        """Test execute method with unexpected exception."""
        command = CreateAdminCommand()

        with patch.object(command.user_service, 'validate_input', return_value=True), \
             patch.object(command.user_service, 'execute_operation', side_effect=Exception("Database error")):

            exit_code = command.execute(
                username='testuser',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=True
            )

            assert exit_code == 1

    def test_execute_cancelled_by_user(self):
        """Test execute method when user cancels operation."""
        command = CreateAdminCommand()

        with patch.object(command.user_service, 'validate_input', return_value=True), \
             patch.object(command, '_confirm_creation', return_value=False):  # User cancels

            exit_code = command.execute(
                username='testuser',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=False  # Not forced, so confirmation is required
            )

            assert exit_code == 0  # Cancel is successful exit

    def test_confirm_creation_yes(self):
        """Test _confirm_creation with user saying yes."""
        command = CreateAdminCommand()

        with patch.object(command.console, 'input', return_value='y'):
            result = command._confirm_creation('testuser', 'test@example.com', 'Test User')
            assert result is True

    def test_confirm_creation_no(self):
        """Test _confirm_creation with user saying no."""
        command = CreateAdminCommand()

        with patch.object(command.console, 'input', return_value='n'):
            result = command._confirm_creation('testuser', 'test@example.com', 'Test User')
            assert result is False

    def test_confirm_creation_default_no(self):
        """Test _confirm_creation with default (empty) response."""
        command = CreateAdminCommand()

        with patch.object(command.console, 'input', return_value=''):
            result = command._confirm_creation('testuser', 'test@example.com', 'Test User')
            assert result is False


class TestCheckUserCommand:
    """Test CheckUserCommand following SOLID principles."""

    def test_initialization(self):
        """Test CheckUserCommand initialization."""
        command = CheckUserCommand()
        assert command.console is not None
        assert hasattr(command, 'database_service')
        assert hasattr(command, 'user_service')

    def test_execute_user_found(self):
        """Test execute method when user is found."""
        command = CheckUserCommand()

        # Mock user found
        mock_user = Mock()
        mock_user.username = 'testuser'
        mock_user.email = 'test@example.com'
        mock_user.role = UserRole.ADMIN
        mock_user.full_name = 'Test User'
        mock_user.created_at = '2023-01-01 00:00:00'

        with patch.object(command.user_service, 'execute_operation', return_value=mock_user):
            exit_code = command.execute(email='test@example.com')
            assert exit_code == 0

    def test_execute_user_not_found(self):
        """Test execute method when user is not found."""
        command = CheckUserCommand()

        with patch.object(command.user_service, 'execute_operation', return_value=None):
            exit_code = command.execute(email='notfound@example.com')
            assert exit_code == 1

    def test_execute_no_email(self):
        """Test execute method with no email provided."""
        command = CheckUserCommand()

        exit_code = command.execute()  # No email parameter
        assert exit_code == 1

    def test_execute_with_exception(self):
        """Test execute method with unexpected exception."""
        command = CheckUserCommand()

        with patch.object(command.user_service, 'execute_operation', side_effect=Exception("Database error")):
            exit_code = command.execute(email='test@example.com')
            assert exit_code == 1


class TestListAdminsCommand:
    """Test ListAdminsCommand following SOLID principles."""

    def test_initialization(self):
        """Test ListAdminsCommand initialization."""
        command = ListAdminsCommand()
        assert command.console is not None
        assert hasattr(command, 'database_service')
        assert hasattr(command, 'user_service')

    def test_execute_admins_found(self):
        """Test execute method when admin users are found."""
        command = ListAdminsCommand()

        # Mock admin users
        mock_admin1 = Mock()
        mock_admin1.username = 'admin1'
        mock_admin1.email = 'admin1@example.com'
        mock_admin1.full_name = 'Admin One'

        mock_admin2 = Mock()
        mock_admin2.username = 'admin2'
        mock_admin2.email = 'admin2@example.com'
        mock_admin2.full_name = 'Admin Two'

        mock_admins = [mock_admin1, mock_admin2]

        with patch.object(command.user_service, 'execute_operation', return_value=mock_admins):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_no_admins_found(self):
        """Test execute method when no admin users are found."""
        command = ListAdminsCommand()

        with patch.object(command.user_service, 'execute_operation', return_value=[]):
            exit_code = command.execute()
            assert exit_code == 0  # No admins is not an error, just a warning

    def test_execute_with_exception(self):
        """Test execute method with unexpected exception."""
        command = ListAdminsCommand()

        with patch.object(command.user_service, 'execute_operation', side_effect=Exception("Database error")):
            exit_code = command.execute()
            assert exit_code == 1


class TestBaseCommandFeatures:
    """Test BaseCommand features used by all commands."""

    def test_print_methods(self):
        """Test BaseCommand print methods."""
        command = HealthCommand()

        # Mock console to verify calls
        mock_console = Mock()
        command.console = mock_console

        command.print_success("Test success")
        mock_console.print.assert_called_with('[green]✓ Test success[/green]')

        command.print_error("Test error")
        mock_console.print.assert_called_with('[red]✗ Test error[/red]')

        command.print_warning("Test warning")
        mock_console.print.assert_called_with('[yellow]⚠ Test warning[/yellow]')

        command.print_info("Test info")
        mock_console.print.assert_called_with('[blue]ℹ Test info[/blue]')

        command.print_header("Test Header", "🎯")
        mock_console.print.assert_called_with('[bold blue]🎯 Test Header[/bold blue]')
