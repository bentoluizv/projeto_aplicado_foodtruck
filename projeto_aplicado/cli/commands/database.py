"""Database management commands following clean architecture principles."""

from typing import Optional

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.database import DatabaseService
from projeto_aplicado.cli.services.migration import MigrationService


class DatabaseCommand(BaseCommand):
    """Database operations command with clean architecture.

    Implements database management following SOLID principles:
    - Single Responsibility: Only handles database command coordination
    - Open/Closed: Easy to extend with new database operations
    - Dependency Inversion: Depends on service abstractions
    """

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize database command with dependency injection.

        Args:
            db_host: Database hostname for connections
            console: Rich console for output (injected dependency)
        """
        super().__init__(console)
        self.database_service = DatabaseService(db_host)
        self.migration_service = MigrationService(db_host)

    def execute(self) -> int:
        """Execute database command (shows help).

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Database Management Commands', '🗄️')
        self.console.print('[blue]Available commands:[/blue]')
        self.console.print(
            '  • [cyan]init[/cyan]      - Initialize database with migrations'
        )
        self.console.print(
            '  • [cyan]status[/cyan]    - Show database and migration status'
        )
        self.console.print(
            '  • [cyan]upgrade[/cyan]   - Upgrade to latest migrations'
        )
        self.console.print('  • [cyan]downgrade[/cyan] - Downgrade migrations')
        self.console.print(
            '  • [cyan]current[/cyan]   - Show current migration'
        )
        self.console.print(
            '  • [cyan]history[/cyan]   - Show migration history'
        )
        self.console.print('  • [cyan]create[/cyan]    - Create new migration')
        self.console.print(
            '  • [cyan]reset[/cyan]     - Reset database (destructive)'
        )
        self.console.print(
            '\n[yellow]Use --help with any command for details[/yellow]'
        )
        return 0


class InitDatabaseCommand(BaseCommand):
    """Initialize database command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService(db_host)

    def execute(self) -> int:
        """Initialize database with migrations.

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Database Initialization', '🚀')

        try:
            result = self.migration_service.execute_operation('init')

            if result['success']:
                self.print_success(result['message'])
                if result.get('details'):
                    self.print_info(result['details'])
                return 0
            else:
                self.print_error(result['message'])
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to initialize database: {str(e)}')
            return 1


class DatabaseStatusCommand(BaseCommand):
    """Database status command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.database_service = DatabaseService(db_host)
        self.migration_service = MigrationService(db_host)

    def execute(self) -> int:
        """Show database status.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Database Status', '📊')

        try:
            # Get migration status
            status = self.migration_service.execute_operation('status')

            # Display connection status
            if status['connection'] == 'OK':
                self.print_success('Database connection: OK')
            else:
                self.print_error('Database connection: FAILED')

            # Display Alembic configuration
            if status['alembic_configured']:
                self.print_success('Alembic configuration: OK')
            else:
                self.print_error('Alembic configuration: Missing')

            if status['migrations_dir']:
                self.print_success('Migrations directory: Found')
            else:
                self.print_error('Migrations directory: Missing')

            # Display current migration
            current = status.get('current_migration', 'Unknown')
            if current and current != 'Unknown':
                self.print_info(f'Current migration: {current}')
            else:
                self.print_warning('Current migration: None')

            # Get database info if connection is OK
            if status['connection'] == 'OK':
                db_info = self.database_service.get_database_info()
                if db_info:
                    self.console.print(
                        f'  Database: {db_info.get("database", "Unknown")}'
                    )
                    self.console.print(
                        f'  Host: {db_info.get("host", "Unknown")}:{db_info.get("port", "5432")}'
                    )

            return 0

        except Exception as e:
            self.print_error(f'Failed to get database status: {str(e)}')
            return 1


class UpgradeDatabaseCommand(BaseCommand):
    """Database upgrade command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService(db_host)

    def execute(self, revision: str = 'head') -> int:
        """Upgrade database to specified revision.

        Args:
            revision: Target revision (default: head)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header(f'Database Upgrade to {revision}', '⬆️')

        try:
            result = self.migration_service.execute_operation(
                'upgrade', revision=revision
            )

            if result['success']:
                self.print_success(result['message'])
                if result.get('details'):
                    self.print_info(result['details'])
                return 0
            else:
                self.print_error(result['message'])
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to upgrade database: {str(e)}')
            return 1


class DowngradeDatabaseCommand(BaseCommand):
    """Database downgrade command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService(db_host)

    def execute(self, revision: str = '-1') -> int:
        """Downgrade database to specified revision.

        Args:
            revision: Target revision (default: -1 for one step back)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header(f'Database Downgrade to {revision}', '⬇️')

        try:
            result = self.migration_service.execute_operation(
                'downgrade', revision=revision
            )

            if result['success']:
                self.print_success(result['message'])
                if result.get('details'):
                    self.print_info(result['details'])
                return 0
            else:
                self.print_error(result['message'])
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to downgrade database: {str(e)}')
            return 1


class CurrentMigrationCommand(BaseCommand):
    """Current migration command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService(db_host)

    def execute(self) -> int:
        """Show current migration.

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Current Migration', '📍')

        try:
            result = self.migration_service.execute_operation('current')

            if result['success']:
                current = result.get('current', 'None')
                if current and current != 'None':
                    self.print_success(f'Current migration: {current}')
                else:
                    self.print_warning('No migrations applied')
                return 0
            else:
                self.print_error(result['message'])
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to get current migration: {str(e)}')
            return 1


class MigrationHistoryCommand(BaseCommand):
    """Migration history command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService(db_host)

    def execute(self, verbose: bool = False) -> int:
        """Show migration history.

        Args:
            verbose: Include verbose output

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Migration History', '📚')

        try:
            result = self.migration_service.execute_operation(
                'history', verbose=verbose
            )

            if result['success']:
                history = result.get('history', 'No history available')
                if history and history != 'No history available':
                    self.console.print(history)
                else:
                    self.print_warning('No migration history found')
                return 0
            else:
                self.print_error(result['message'])
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to get migration history: {str(e)}')
            return 1


class CreateMigrationCommand(BaseCommand):
    """Create migration command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService(db_host)

    def execute(self, message: str) -> int:
        """Create a new migration.

        Args:
            message: Migration message/description

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header(f'Create Migration: {message}', '📝')

        if not message.strip():
            self.print_error('Migration message is required')
            return 1

        try:
            result = self.migration_service.execute_operation(
                'create', message=message
            )

            if result['success']:
                self.print_success(result['message'])
                if result.get('details'):
                    self.print_info(result['details'])
                return 0
            else:
                self.print_error(result['message'])
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to create migration: {str(e)}')
            return 1


class ResetDatabaseCommand(BaseCommand):
    """Reset database command."""

    def __init__(
        self, db_host: str = 'localhost', console: Optional[Console] = None
    ):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService(db_host)

    def execute(self, force: bool = False) -> int:
        """Reset database (destructive operation).

        Args:
            force: Force reset without confirmation

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Database Reset', '💥')

        if not force:
            self.print_warning('This is a destructive operation!')
            self.print_error('Use --force flag to confirm database reset')
            return 1

        try:
            result = self.migration_service.execute_operation(
                'reset', force=force
            )

            if result['success']:
                self.print_success(result['message'])
                if result.get('details'):
                    self.print_info(result['details'])
                return 0
            else:
                self.print_error(result['message'])
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to reset database: {str(e)}')
            return 1


# Create the database app with sub-commands
database_app = cyclopts.App(
    name='database',
    help='Database management commands',
)


# Register database commands
@database_app.default
def database_default(db_host: str = 'localhost') -> int:
    """Database management commands."""
    command = DatabaseCommand(db_host)
    return command.execute()


@database_app.command
def init(db_host: str = 'localhost') -> int:
    """Initialize database with migrations."""
    command = InitDatabaseCommand(db_host)
    return command.execute()


@database_app.command
def status(db_host: str = 'localhost') -> int:
    """Show database and migration status."""
    command = DatabaseStatusCommand(db_host)
    return command.execute()


@database_app.command
def upgrade(revision: str = 'head', db_host: str = 'localhost') -> int:
    """Upgrade database to specified revision.

    Args:
        revision: Target migration revision (default: head)
        db_host: Database hostname (default: localhost)
    """
    command = UpgradeDatabaseCommand(db_host)
    return command.execute(revision)


@database_app.command
def downgrade(revision: str = '-1', db_host: str = 'localhost') -> int:
    """Downgrade database to specified revision.

    Args:
        revision: Target migration revision (default: -1 for one step back)
        db_host: Database hostname (default: localhost)
    """
    command = DowngradeDatabaseCommand(db_host)
    return command.execute(revision)


@database_app.command
def current(db_host: str = 'localhost') -> int:
    """Show current migration revision."""
    command = CurrentMigrationCommand(db_host)
    return command.execute()


@database_app.command
def history(verbose: bool = False, db_host: str = 'localhost') -> int:
    """Show migration history.

    Args:
        verbose: Include verbose output
        db_host: Database hostname (default: localhost)
    """
    command = MigrationHistoryCommand(db_host)
    return command.execute(verbose)


@database_app.command
def create(message: str, db_host: str = 'localhost') -> int:
    """Create a new migration.

    Args:
        message: Migration message/description
        db_host: Database hostname (default: localhost)
    """
    command = CreateMigrationCommand(db_host)
    return command.execute(message)


@database_app.command
def reset(force: bool = False, db_host: str = 'localhost') -> int:
    """Reset database (destructive operation).

    Args:
        force: Force reset without confirmation
        db_host: Database hostname (default: localhost)
    """
    command = ResetDatabaseCommand(db_host)
    return command.execute(force)
