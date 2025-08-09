"""Health command implementation following SOLID principles."""

from typing import Any

import cyclopts

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.database import DatabaseService
from projeto_aplicado.cli.services.health import HealthService
from projeto_aplicado.cli.services.user import UserService


class HealthCommand(BaseCommand):
    """Health check command.

    Follows Single Responsibility Principle: only handles health check display.
    Follows Dependency Inversion Principle: depends on service abstractions.
    """

    def __init__(self, db_host: str = 'localhost', **kwargs):
        """Initialize the health command.

        Args:
            db_host: Database hostname
            **kwargs: Additional arguments for base class
        """
        super().__init__(**kwargs)

        # Dependency injection - create services
        self.database_service = DatabaseService(db_host)
        self.user_service = UserService(self.database_service)
        self.health_service = HealthService(
            self.database_service, self.user_service
        )

    def execute(self, **kwargs: Any) -> int:
        """Execute the health check command.

        Args:
            **kwargs: Command arguments

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        self.print_header('System Health Check', '🏥')

        # Execute health checks
        health_result = self.health_service.execute_operation(**kwargs)

        # Display results
        for check_name, success, message in health_result['details']:
            if success:
                self.print_success(message)
            else:
                self.print_error(message)

        # Display database info
        db_info = health_result['database_info']
        self.console.print(f'[dim]  Database: {db_info["database"]}[/dim]')
        self.console.print(
            f'[dim]  Host: {db_info["host"]}:{db_info["port"]}[/dim]'
        )

        # Summary
        passed = health_result['passed']
        total = health_result['total']

        if health_result['success']:
            self.console.print(
                f'\n[bold green]🎉 All {total} health checks passed![/bold green]'
            )
            return 0
        else:
            self.console.print(
                f'\n[bold yellow]⚠ {passed}/{total} health checks passed[/bold yellow]'
            )
            return 1


# Create the health app
health_app = cyclopts.App(
    name='health',
    help='System health check commands',
)


@health_app.default
def health_default(db_host: str = 'localhost') -> int:
    """Check system health status.

    Args:
        db_host: Database hostname (default: localhost)

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    command = HealthCommand(db_host=db_host)
    return command.execute()
