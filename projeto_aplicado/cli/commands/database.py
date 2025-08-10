"""Database management commands following clean architecture principles."""

from typing import Optional

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.ext.database import DatabaseService
from projeto_aplicado.cli.schemas import (
    DatabaseInfo,
    MigrationResult,
    MigrationStatus,
)
from projeto_aplicado.cli.services.migration import MigrationService


class DatabaseCommand(BaseCommand):
    """Manage database operations and migrations.

    Provides commands for database initialization, status checking,
    migration management, and maintenance operations.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize database command.

        Args:
            console: Console for output formatting
        """
        super().__init__(console)
        self.database_service = self.get_service(DatabaseService)
        self.migration_service = self.get_service(MigrationService)

    def execute(self) -> int:
        """Show database management help and available commands.

        Returns:
            0 (always successful)
        """
        msg = (
            '[bold blue]🗄️ Database Management Commands[/bold blue]\n'
            '[blue]Available commands:[/blue]\n'
            '  • [cyan]init[/cyan]      - Initialize database with migrations\n'  # noqa: E501
            '  • [cyan]status[/cyan]    - Show database and migration status\n'
            '  • [cyan]upgrade[/cyan]   - Upgrade to latest migrations\n'
            '  • [cyan]downgrade[/cyan] - Downgrade migrations\n'
            '  • [cyan]current[/cyan]   - Show current migration\n'
            '  • [cyan]history[/cyan]   - Show migration history\n'
            '  • [cyan]create[/cyan]    - Create new migration\n'
            '  • [cyan]reset[/cyan]     - Reset database (destructive)\n'
            '\n[yellow]Use --help with any command for details[/yellow]'
        )
        self.console.print(msg)
        return 0


class InitDatabaseCommand(BaseCommand):
    """Initialize the database with tables and migrations.

    Sets up the database schema and applies initial migrations.
    Use this for first-time database setup.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService()

    def execute(self) -> int:
        """Initialize database with migrations.

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Database Initialization', '🚀')

        try:
            result: MigrationResult = self.migration_service.execute_operation(
                'init'
            )

            msg_parts = []
            if result.success:
                msg_parts.append(f'[green]{result.message}[/green]')
                if result.details:
                    msg_parts.append(f'[blue]{result.details}[/blue]')
            else:
                msg_parts.append(f'[red]{result.message}[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to initialize database: {str(e)}')
            return 1


class DatabaseStatusCommand(BaseCommand):
    """Check database connection and migration status.

    Shows current database state, connection status,
    and migration information.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.database_service = self.get_service(DatabaseService)
        self.migration_service = self.get_service(MigrationService)

    def execute(self) -> int:
        """Show database status.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Database Status', '📊')

        try:
            # Get migration status
            status: MigrationStatus = self.migration_service.execute_operation(
                'status'
            )

            # Build status message
            connection_status = (
                '[green]OK[/green]'
                if status.connection == 'OK'
                else '[red]FAILED[/red]'
            )
            alembic_status = (
                '[green]OK[/green]'
                if status.alembic_configured
                else '[red]Missing[/red]'
            )
            migrations_status = (
                '[green]Found[/green]'
                if status.migrations_dir
                else '[red]Missing[/red]'
            )
            current = status.current_migration
            migration_status = (
                f'[blue]{current}[/blue]'
                if current and current != 'Unknown'
                else '[yellow]None[/yellow]'
            )

            msg_parts = [
                '[bold blue]📊 Database Status[/bold blue]\n',
                f'Database connection: {connection_status}',
                f'Alembic configuration: {alembic_status}',
                f'Migrations directory: {migrations_status}',
                f'Current migration: {migration_status}',
            ]

            # Add database info if connected
            if status.connection == 'OK':
                db_info: DatabaseInfo = (
                    self.database_service.get_database_info()
                )
                msg_parts.extend([
                    '[dim]Database details:[/dim]',
                    f'  Database: {db_info.database}',
                    f'  Host: {db_info.host}  Port: {db_info.port}',
                ])

            msg = '\n'.join(msg_parts)
            self.console.print(msg)

            return 0

        except Exception as e:
            self.print_error(f'Failed to get database status: {str(e)}')
            return 1


class UpgradeDatabaseCommand(BaseCommand):
    """Database upgrade command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService()

    def execute(self, revision: str = 'head') -> int:
        """Upgrade database to specified revision.

        Args:
            revision: Target revision (default: head)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header(f'Database Upgrade to {revision}', '⬆️')

        try:
            result: MigrationResult = self.migration_service.execute_operation(
                'upgrade', revision=revision
            )

            msg_parts = []
            if result.success:
                msg_parts.append(f'[green]{result.message}[/green]')
                if result.details:
                    msg_parts.append(f'[blue]{result.details}[/blue]')
            else:
                msg_parts.append(f'[red]{result.message}[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to upgrade database: {str(e)}')
            return 1


class DowngradeDatabaseCommand(BaseCommand):
    """Database downgrade command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService()

    def execute(self, revision: str = '-1') -> int:
        """Downgrade database to specified revision.

        Args:
            revision: Target revision (default: -1 for one step back)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header(f'Database Downgrade to {revision}', '⬇️')

        try:
            result: MigrationResult = self.migration_service.execute_operation(
                'downgrade', revision=revision
            )

            msg_parts = []
            if result.success:
                msg_parts.append(f'[green]{result.message}[/green]')
                if result.details:
                    msg_parts.append(f'[blue]{result.details}[/blue]')
            else:
                msg_parts.append(f'[red]{result.message}[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to downgrade database: {str(e)}')
            return 1


class CurrentMigrationCommand(BaseCommand):
    """Current migration command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService()

    def execute(self) -> int:
        """Show current migration.

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Current Migration', '📍')

        try:
            result: MigrationResult = self.migration_service.execute_operation(
                'current'
            )

            msg_parts = []
            if result.success:
                if result.current and result.current != 'None':
                    msg_parts.append(
                        f'[green]Current migration: {result.current}[/green]'
                    )
                else:
                    msg_parts.append('[yellow]No migrations applied[/yellow]')
            else:
                msg_parts.append(f'[red]{result.message}[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to get current migration: {str(e)}')
            return 1


class MigrationHistoryCommand(BaseCommand):
    """Migration history command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService()

    def execute(self, verbose: bool = False) -> int:
        """Show migration history.

        Args:
            verbose: Include verbose output

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Migration History', '📚')

        try:
            result: MigrationResult = self.migration_service.execute_operation(
                'history', verbose=verbose
            )

            msg_parts = []
            if result.success:
                if result.history and result.history != 'No history available':
                    msg_parts.append(result.history)
                else:
                    msg_parts.append(
                        '[yellow]No migration history found[/yellow]'
                    )
            else:
                msg_parts.append(f'[red]{result.message}[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to get migration history: {str(e)}')
            return 1


class CreateMigrationCommand(BaseCommand):
    """Create migration command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService()

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
            result: MigrationResult = self.migration_service.execute_operation(
                'create', message=message
            )

            msg_parts = []
            if result.success:
                msg_parts.append(f'[green]{result.message}[/green]')
                if result.details:
                    msg_parts.append(f'[blue]{result.details}[/blue]')
            else:
                msg_parts.append(f'[red]{result.message}[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to create migration: {str(e)}')
            return 1


class ResetDatabaseCommand(BaseCommand):
    """Reset database command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.migration_service = MigrationService()

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
            result: MigrationResult = self.migration_service.execute_operation(
                'reset', force=force
            )

            msg_parts = []
            if result.success:
                msg_parts.append(f'[green]{result.message}[/green]')
                if result.details:
                    msg_parts.append(f'[blue]{result.details}[/blue]')
            else:
                msg_parts.append(f'[red]{result.message}[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

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
def database_default() -> int:
    """Manage database operations - init, status, migrations, and maintenance.

    Use subcommands to perform specific database operations.
    """
    command = DatabaseCommand()
    return command.execute()


@database_app.command
def init() -> int:
    """Initialize database with migrations."""
    command = InitDatabaseCommand()
    return command.execute()


@database_app.command
def status() -> int:
    """Show database and migration status."""
    command = DatabaseStatusCommand()
    return command.execute()


@database_app.command
def upgrade(revision: str = 'head') -> int:
    """Upgrade database to specified revision.

    Args:
        revision: Target migration revision (default: head)
    """
    command = UpgradeDatabaseCommand()
    return command.execute(revision)


@database_app.command
def downgrade(revision: str = '-1') -> int:
    """Downgrade database to specified revision.

    Args:
        revision: Target migration revision (default: -1 for one step back)
    """
    command = DowngradeDatabaseCommand()
    return command.execute(revision)


@database_app.command
def current() -> int:
    """Show current migration revision."""
    command = CurrentMigrationCommand()
    return command.execute()


@database_app.command
def history(verbose: bool = False) -> int:
    """Show migration history.

    Args:
        verbose: Include verbose output
    """
    command = MigrationHistoryCommand()
    return command.execute(verbose)


@database_app.command
def create(message: str) -> int:
    """Create a new migration.

    Args:
        message: Migration message/description
    """
    command = CreateMigrationCommand()
    return command.execute(message)


@database_app.command
def reset(force: bool = False) -> int:
    """Reset database (destructive operation).

    Args:
        force: Force reset without confirmation
    """
    command = ResetDatabaseCommand()
    return command.execute(force)
