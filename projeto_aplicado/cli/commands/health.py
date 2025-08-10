"""Health command implementation following SOLID principles."""

from typing import Any

import cyclopts

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.health import HealthService


class HealthCommand(BaseCommand):
    """Health check command.

    Follows Single Responsibility Principle: only handles health check display.
    Follows Dependency Inversion Principle: depends on service abstractions.
    """

    def __init__(self, **kwargs):
        """Initialize the health command.

        Args:
            **kwargs: Additional arguments for base class
        """
        super().__init__(**kwargs)
        self.health_service = self.get_service(HealthService)

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

        msg_parts = []

        # Add check results
        for detail in health_result.details:
            status = '[green]✓[/green]' if detail.passed else '[red]✗[/red]'
            msg_parts.append(f'{status} {detail.message}')

        # Add database info
        db_info = health_result.database_info
        msg_parts.extend([
            '',
            '[dim]Database details:[/dim]',
            f'  Database: {db_info["database"]}',
            f'  Host: {db_info["host"]}:{db_info["port"]}',
        ])

        # Add summary
        passed = health_result.passed
        total = health_result.total

        if health_result.success:
            msg_parts.append(
                f'\n[bold green]🎉 All {total} health checks passed![/bold green]'
            )
        else:
            msg_parts.append(
                f'\n[bold yellow]⚠ {passed}/{total} health checks passed[/bold yellow]'  # noqa: E501
            )

        msg = '\n'.join(msg_parts)
        self.console.print(msg)
        return 0 if health_result.success else 1


# Create the health app
health_app = cyclopts.App(
    name='health',
    help='System health check commands',
)


@health_app.default
def health_default() -> int:
    """Check system health status.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    command = HealthCommand()
    return command.execute()
