"""Tests for CLI commands following clean architecture principles."""

from unittest.mock import Mock, patch

from rich.console import Console

from projeto_aplicado.cli.commands.admin import (
    CheckUserCommand,
    CreateAdminCommand,
    ListAdminsCommand,
)
from projeto_aplicado.cli.commands.completions import (
    CompletionsCommand,
    GenerateCompletionsCommand,
    InstallCompletionsCommand,
    StatusCompletionsCommand,
    UninstallCompletionsCommand,
)
from projeto_aplicado.cli.commands.health import HealthCommand
from projeto_aplicado.cli.commands.setup import (
    AutoInstallCommand,
    CheckSetupCommand,
    GenerateAliasCommand,
    SetupCommand,
    ShowPathCommand,
)
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
                'port': '5432',
            },
        }

        with patch.object(
            command.health_service,
            'execute_operation',
            return_value=mock_result,
        ):
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
                'port': '5432',
            },
        }

        with patch.object(
            command.health_service,
            'execute_operation',
            return_value=mock_result,
        ):
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

        with (
            patch.object(
                command.user_service, 'validate_input', return_value=True
            ),
            patch.object(
                command.user_service,
                'execute_operation',
                return_value=mock_user,
            ),
            patch.object(command, '_confirm_creation', return_value=True),
        ):
            exit_code = command.execute(
                username='testuser',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=False,
            )

            assert exit_code == 0

    def test_execute_validation_failure(self):
        """Test execute method with validation failure."""
        command = CreateAdminCommand()

        with patch.object(
            command.user_service, 'validate_input', return_value=False
        ):
            exit_code = command.execute(
                username='',  # Invalid username
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=True,
            )

            assert exit_code == 1

    def test_execute_user_already_exists(self):
        """Test execute method when user already exists."""
        command = CreateAdminCommand()

        with (
            patch.object(
                command.user_service, 'validate_input', return_value=True
            ),
            patch.object(
                command.user_service, 'execute_operation', return_value=None
            ),
        ):  # None = already exists
            exit_code = command.execute(
                username='testuser',
                email='existing@example.com',
                password='password123',
                full_name='Test User',
                force=True,
            )

            assert exit_code == 1

    def test_execute_with_exception(self):
        """Test execute method with unexpected exception."""
        command = CreateAdminCommand()

        with (
            patch.object(
                command.user_service, 'validate_input', return_value=True
            ),
            patch.object(
                command.user_service,
                'execute_operation',
                side_effect=Exception('Database error'),
            ),
        ):
            exit_code = command.execute(
                username='testuser',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=True,
            )

            assert exit_code == 1

    def test_execute_cancelled_by_user(self):
        """Test execute method when user cancels operation."""
        command = CreateAdminCommand()

        with (
            patch.object(
                command.user_service, 'validate_input', return_value=True
            ),
            patch.object(command, '_confirm_creation', return_value=False),
        ):  # User cancels
            exit_code = command.execute(
                username='testuser',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=False,  # Not forced, so confirmation is required
            )

            assert exit_code == 0  # Cancel is successful exit

    def test_confirm_creation_yes(self):
        """Test _confirm_creation with user saying yes."""
        command = CreateAdminCommand()

        with patch.object(command.console, 'input', return_value='y'):
            result = command._confirm_creation(
                'testuser', 'test@example.com', 'Test User'
            )
            assert result is True

    def test_confirm_creation_no(self):
        """Test _confirm_creation with user saying no."""
        command = CreateAdminCommand()

        with patch.object(command.console, 'input', return_value='n'):
            result = command._confirm_creation(
                'testuser', 'test@example.com', 'Test User'
            )
            assert result is False

    def test_confirm_creation_default_no(self):
        """Test _confirm_creation with default (empty) response."""
        command = CreateAdminCommand()

        with patch.object(command.console, 'input', return_value=''):
            result = command._confirm_creation(
                'testuser', 'test@example.com', 'Test User'
            )
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

        with patch.object(
            command.user_service, 'execute_operation', return_value=mock_user
        ):
            exit_code = command.execute(email='test@example.com')
            assert exit_code == 0

    def test_execute_user_not_found(self):
        """Test execute method when user is not found."""
        command = CheckUserCommand()

        with patch.object(
            command.user_service, 'execute_operation', return_value=None
        ):
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

        with patch.object(
            command.user_service,
            'execute_operation',
            side_effect=Exception('Database error'),
        ):
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

        with patch.object(
            command.user_service, 'execute_operation', return_value=mock_admins
        ):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_no_admins_found(self):
        """Test execute method when no admin users are found."""
        command = ListAdminsCommand()

        with patch.object(
            command.user_service, 'execute_operation', return_value=[]
        ):
            exit_code = command.execute()
            assert exit_code == 0  # No admins is not an error, just a warning

    def test_execute_with_exception(self):
        """Test execute method with unexpected exception."""
        command = ListAdminsCommand()

        with patch.object(
            command.user_service,
            'execute_operation',
            side_effect=Exception('Database error'),
        ):
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

        command.print_success('Test success')
        mock_console.print.assert_called_with('[green]✓ Test success[/green]')

        command.print_error('Test error')
        mock_console.print.assert_called_with('[red]✗ Test error[/red]')

        command.print_warning('Test warning')
        mock_console.print.assert_called_with(
            '[yellow]⚠ Test warning[/yellow]'
        )

        command.print_info('Test info')
        mock_console.print.assert_called_with('[blue]ℹ Test info[/blue]')

        command.print_header('Test Header', '🎯')
        mock_console.print.assert_called_with(
            '[bold blue]🎯 Test Header[/bold blue]'
        )


class TestSetupCommand:
    """Test SetupCommand following SOLID principles."""

    def test_initialization(self):
        """Test SetupCommand initialization."""
        command = SetupCommand()
        assert command.console is not None
        assert hasattr(command, 'shell_service')

    def test_initialization_with_custom_console(self):
        """Test SetupCommand initialization with custom console."""
        console = Console()
        command = SetupCommand(console=console)
        assert command.console == console

    def test_execute(self):
        """Test execute method shows help information."""
        command = SetupCommand()
        exit_code = command.execute()
        assert exit_code == 0


class TestShowPathCommand:
    """Test ShowPathCommand following SOLID principles."""

    def test_initialization(self):
        """Test ShowPathCommand initialization."""
        command = ShowPathCommand()
        assert command.console is not None
        assert hasattr(command, 'shell_service')

    def test_execute_success(self):
        """Test execute method with successful path check."""
        command = ShowPathCommand()

        mock_result = {
            'project_root': '/home/user/foodtruck',
            'venv_path': '/home/user/foodtruck/.venv',
            'cli_path': '/home/user/foodtruck/.venv/bin/foodtruck-cli',
            'cli_in_path': True,
            'activation_script': '/home/user/foodtruck/.venv/bin/activate',
            'venv_bin_path': '/home/user/foodtruck/.venv/bin',
            'shell_config_file': '/home/user/.bashrc',  # Added missing field
        }

        with patch.object(command.shell_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failed path check."""
        command = ShowPathCommand()

        with patch.object(command.shell_service, 'execute_operation', side_effect=Exception("Service error")):
            exit_code = command.execute()
            assert exit_code == 1


class TestGenerateAliasCommand:
    """Test GenerateAliasCommand following SOLID principles."""

    def test_initialization(self):
        """Test GenerateAliasCommand initialization."""
        command = GenerateAliasCommand()
        assert command.console is not None
        assert hasattr(command, 'shell_service')

    def test_execute_auto_shell(self):
        """Test execute method with auto shell detection."""
        command = GenerateAliasCommand()

        mock_result = {
            'success': True,
            'aliases': {
                'ftcli': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app',
                'ft-health': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app health',
                'ft-admin': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app admin',
                'ft-db': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app database',
            },
            'shell': 'zsh',
            'config_file': '/home/user/.zshrc',
        }

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='auto')
            assert exit_code == 0

    def test_execute_specific_shell(self):
        """Test execute method with specific shell."""
        command = GenerateAliasCommand()

        mock_result = {
            'success': True,
            'aliases': {
                'ftcli': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app',
                'ft-health': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app health',
            },
            'shell': 'bash',
            'config_file': '/home/user/.bashrc',
        }

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='bash')
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failure."""
        command = GenerateAliasCommand()

        mock_result = {'success': False, 'error': 'Failed to generate aliases'}

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute()
            assert exit_code == 1


class TestAutoInstallCommand:
    """Test AutoInstallCommand following SOLID principles."""

    def test_initialization(self):
        """Test AutoInstallCommand initialization."""
        command = AutoInstallCommand()
        assert command.console is not None
        assert hasattr(command, 'shell_service')

    def test_execute_auto_shell_success(self):
        """Test execute method with auto shell detection and success."""
        command = AutoInstallCommand()

        mock_result = {
            'success': True,
            'config_file': '/home/user/.zshrc',
            'aliases_installed': True,
            'shell': 'zsh',
        }

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='auto')
            assert exit_code == 0

    def test_execute_specific_shell_success(self):
        """Test execute method with specific shell and success."""
        command = AutoInstallCommand()

        mock_result = {
            'success': True,
            'config_file': '/home/user/.bashrc',
            'aliases_installed': True,
            'shell': 'bash',
        }

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='bash')
            assert exit_code == 0

    def test_execute_with_force(self):
        """Test execute method with force flag."""
        command = AutoInstallCommand()

        mock_result = {
            'success': True,
            'config_file': '/home/user/.zshrc',
            'aliases_installed': True,
            'shell': 'zsh',
        }

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='auto', force=True)
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failure."""
        command = AutoInstallCommand()

        mock_result = {'success': False, 'error': 'Failed to install aliases'}

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute()
            assert exit_code == 1


class TestCheckSetupCommand:
    """Test CheckSetupCommand following SOLID principles."""

    def test_initialization(self):
        """Test CheckSetupCommand initialization."""
        command = CheckSetupCommand()
        assert command.console is not None
        assert hasattr(command, 'shell_service')

    def test_execute_all_good(self):
        """Test execute method with all checks passing."""
        command = CheckSetupCommand()

        mock_result = {
            'cli_in_path': True,
            'venv_active': True,
            'aliases_found': ['alias ftcli="cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app"'],
            'current_shell': 'zsh',  # Changed from 'shell' to 'current_shell'
            'config_file': '/home/user/.zshrc',
            'project_root': '/home/user/foodtruck',
            'venv_path': '/home/user/foodtruck/.venv',
        }

        with patch.object(command.shell_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_partial_setup(self):
        """Test execute method with partial setup."""
        command = CheckSetupCommand()

        mock_result = {
            'cli_in_path': False,
            'venv_active': True,
            'aliases_found': [],  # Changed from 'aliases_configured' to 'aliases_found'
            'current_shell': 'bash',  # Changed from 'shell' to 'current_shell'
            'config_file': '/home/user/.bashrc',
            'project_root': '/home/user/foodtruck',
            'venv_path': '/home/user/foodtruck/.venv',
        }

        with patch.object(command.shell_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_no_setup(self):
        """Test execute method with no setup."""
        command = CheckSetupCommand()

        mock_result = {
            'cli_in_path': False,
            'venv_active': False,
            'aliases_found': [],  # Changed from 'aliases_configured' to 'aliases_found'
            'current_shell': 'unknown',  # Changed from 'shell' to 'current_shell'
            'config_file': '/home/user/.profile',
            'project_root': None,
            'venv_path': None,
        }

        with patch.object(command.shell_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failure."""
        command = CheckSetupCommand()

        with patch.object(
            command.shell_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            exit_code = command.execute()
            assert exit_code == 1


class TestCompletionsCommand:
    """Test CompletionsCommand following SOLID principles."""

    def test_initialization(self):
        """Test CompletionsCommand initialization."""
        command = CompletionsCommand()
        assert command.console is not None
        assert hasattr(command, 'completions_service')

    def test_initialization_with_custom_console(self):
        """Test CompletionsCommand initialization with custom console."""
        console = Console()
        command = CompletionsCommand(console=console)
        assert command.console == console

    def test_execute(self):
        """Test execute method shows help information."""
        command = CompletionsCommand()
        exit_code = command.execute()
        assert exit_code == 0


class TestGenerateCompletionsCommand:
    """Test GenerateCompletionsCommand following SOLID principles."""

    def test_initialization(self):
        """Test GenerateCompletionsCommand initialization."""
        command = GenerateCompletionsCommand()
        assert command.console is not None
        assert hasattr(command, 'completions_service')

    def test_execute_bash_success(self):
        """Test execute method with bash shell and success."""
        command = GenerateCompletionsCommand()

        mock_result = {
            'success': True,
            'script': 'complete -W "health admin database" foodtruck-cli',
            'shell': 'bash',
            'install_instructions': [
                'source ~/.bashrc',
                'Add to ~/.bash_completion',
            ],
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='bash')
            assert exit_code == 0

    def test_execute_zsh_success(self):
        """Test execute method with zsh shell and success."""
        command = GenerateCompletionsCommand()

        mock_result = {
            'success': True,
            'script': '_foodtruck_cli() { _arguments "1: :(health admin database)" }',
            'shell': 'zsh',
            'install_instructions': ['Add to ~/.zshrc', 'Restart shell'],
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='zsh')
            assert exit_code == 0

    def test_execute_with_output_file(self):
        """Test execute method with output file."""
        command = GenerateCompletionsCommand()

        mock_result = {
            'success': True,
            'script': 'complete -W "health admin database" foodtruck-cli',
            'shell': 'bash',
            'output_file': '/tmp/foodtruck-cli.bash',
            'install_instructions': ['source /tmp/foodtruck-cli.bash'],
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(
                shell='bash', output='/tmp/foodtruck-cli.bash'
            )
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failure."""
        command = GenerateCompletionsCommand()

        mock_result = {'success': False, 'error': 'Unsupported shell'}

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='invalid')
            assert exit_code == 1


class TestInstallCompletionsCommand:
    """Test InstallCompletionsCommand following SOLID principles."""

    def test_initialization(self):
        """Test InstallCompletionsCommand initialization."""
        command = InstallCompletionsCommand()
        assert command.console is not None
        assert hasattr(command, 'completions_service')

    def test_execute_auto_shell_success(self):
        """Test execute method with auto shell detection and success."""
        command = InstallCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'zsh',
            'install_path': '/home/user/.zshrc',
            'script_installed': True,
            'reload_command': 'source ~/.zshrc',  # Added missing field
        }

        with patch.object(command.completions_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute(shell='auto')
            assert exit_code == 0

    def test_execute_specific_shell_success(self):
        """Test execute method with specific shell and success."""
        command = InstallCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'bash',
            'install_path': '/home/user/.bashrc',
            'script_installed': True,
            'reload_command': 'source ~/.bashrc',  # Added missing field
        }

        with patch.object(command.completions_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute(shell='bash')
            assert exit_code == 0

    def test_execute_with_force(self):
        """Test execute method with force flag."""
        command = InstallCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'zsh',
            'install_path': '/home/user/.zshrc',
            'script_installed': True,
            'reload_command': 'source ~/.zshrc',  # Added missing field
        }

        with patch.object(command.completions_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute(shell='auto', force=True)
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failure."""
        command = InstallCompletionsCommand()

        mock_result = {
            'success': False,
            'error': 'Failed to install completions',
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute()
            assert exit_code == 1


class TestStatusCompletionsCommand:
    """Test StatusCompletionsCommand following SOLID principles."""

    def test_initialization(self):
        """Test StatusCompletionsCommand initialization."""
        command = StatusCompletionsCommand()
        assert command.console is not None
        assert hasattr(command, 'completions_service')

    def test_execute_installed(self):
        """Test execute method with completions installed."""
        command = StatusCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'zsh',
            'installed': True,
            'install_path': '/home/user/.zshrc',
            'script_found': True,
            'completion_dir': '/home/user/.oh-my-zsh/completions',
            'current_shell': 'zsh',
            'completion_support': True,
            'shells': {
                'bash': {'installed': False, 'path': None},
                'zsh': {'installed': True, 'path': '/home/user/.zshrc'},
                'fish': {'installed': False, 'path': None},
            },
            'can_test': True,  # Added missing field
        }

        with patch.object(command.completions_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_not_installed(self):
        """Test execute method with completions not installed."""
        command = StatusCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'bash',
            'installed': False,
            'install_path': None,
            'script_found': False,
            'completion_dir': None,
            'current_shell': 'bash',
            'completion_support': True,
            'shells': {
                'bash': {'installed': False, 'path': None},
                'zsh': {'installed': False, 'path': None},
                'fish': {'installed': False, 'path': None},
            },
            'can_test': False,  # Added missing field
        }

        with patch.object(command.completions_service, 'execute_operation', return_value=mock_result):
            exit_code = command.execute()
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failure."""
        command = StatusCompletionsCommand()

        mock_result = {'success': False, 'error': 'Failed to check status'}

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute()
            assert exit_code == 1


class TestUninstallCompletionsCommand:
    """Test UninstallCompletionsCommand following SOLID principles."""

    def test_initialization(self):
        """Test UninstallCompletionsCommand initialization."""
        command = UninstallCompletionsCommand()
        assert command.console is not None
        assert hasattr(command, 'completions_service')

    def test_execute_auto_shell_success(self):
        """Test execute method with auto shell detection and success."""
        command = UninstallCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'zsh',
            'uninstalled': True,
            'removed_files': ['/home/user/.zshrc'],
            'backup_created': True,
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='auto')
            assert exit_code == 0

    def test_execute_specific_shell_success(self):
        """Test execute method with specific shell and success."""
        command = UninstallCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'bash',
            'uninstalled': True,
            'removed_files': ['/home/user/.bashrc'],
            'backup_created': True,
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='bash')
            assert exit_code == 0

    def test_execute_not_installed(self):
        """Test execute method with completions not installed."""
        command = UninstallCompletionsCommand()

        mock_result = {
            'success': True,
            'shell': 'zsh',
            'uninstalled': False,
            'message': 'Completions not found',
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute(shell='auto')
            assert exit_code == 0

    def test_execute_failure(self):
        """Test execute method with failure."""
        command = UninstallCompletionsCommand()

        mock_result = {
            'success': False,
            'error': 'Failed to uninstall completions',
        }

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            exit_code = command.execute()
            assert exit_code == 1
