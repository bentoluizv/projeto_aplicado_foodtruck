"""Test configuration for CLI commands."""

from unittest.mock import Mock

import pytest
from rich.console import Console


@pytest.fixture
def mock_console():
    """Provide a mock console for testing."""
    return Mock(spec=Console)


@pytest.fixture
def mock_user():
    """Provide a mock user for testing."""
    from projeto_aplicado.resources.user.model import (  # noqa: PLC0415
        User,
        UserRole,
    )

    user = Mock(spec=User)
    user.id = 1
    user.username = 'testuser'
    user.email = 'test@example.com'
    user.full_name = 'Test User'
    user.role = UserRole.ADMIN
    user.is_active = True
    return user


@pytest.fixture
def valid_user_data():
    """Provide valid user creation data."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'full_name': 'Test User',
    }


@pytest.fixture
def mock_database_info():
    """Provide mock database information."""
    from projeto_aplicado.cli.schemas import DatabaseInfo  # noqa: PLC0415

    return DatabaseInfo(
        database='foodtruck',
        host='localhost',
        container='localhost',
        port='5432',
        status='connected',
    )


@pytest.fixture
def mock_health_check_details():
    """Provide mock health check details."""
    from projeto_aplicado.cli.schemas import HealthCheckDetail  # noqa: PLC0415

    return [
        HealthCheckDetail(
            name='Database Connection',
            passed=True,
            message='Database connection OK',
        ),
        HealthCheckDetail(
            name='Admin Users', passed=True, message='Admin users found: 2'
        ),
        HealthCheckDetail(
            name='Configuration',
            passed=True,
            message='All settings configured',
        ),
    ]


@pytest.fixture
def mock_migration_status():
    """Provide mock migration status."""
    from projeto_aplicado.cli.schemas import MigrationStatus

    return MigrationStatus(
        success=True,
        message='Database status retrieved',
        connection='OK',
        current_migration='abc123def456',
        alembic_configured=True,
        migrations_dir=True,
    )


@pytest.fixture
def mock_shell_path_info():
    """Provide mock shell path information."""
    from projeto_aplicado.cli.schemas import ShellPathInfo

    return ShellPathInfo(
        project_root='/home/user/foodtruck',
        venv_path='/home/user/foodtruck/.venv',
        venv_bin_path='/home/user/foodtruck/.venv/bin',
        cli_path='/home/user/foodtruck/.venv/bin/foodtruck-cli',
        activation_script='/home/user/foodtruck/.venv/bin/activate',
        cli_exists=True,
        current_shell='bash',
        shell_config_file='/home/user/.bashrc',
        cli_in_path=True,
    )


@pytest.fixture
def mock_completion_shells():
    """Provide mock completion shell statuses."""
    from projeto_aplicado.cli.schemas import CompletionShellStatus

    return {
        'bash': CompletionShellStatus(
            installed=True,
            path='/home/user/.local/share/bash-completion/completions/foodtruck-cli',
        ),
        'zsh': CompletionShellStatus(installed=False, path=None),
        'fish': CompletionShellStatus(installed=False, path=None),
    }
