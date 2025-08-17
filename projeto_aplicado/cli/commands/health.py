"""Health command implementation following SOLID principles."""

from typing import Any

import cyclopts

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.health import HealthService


class HealthCommand(BaseCommand):
    """Check system health and status.

    Performs comprehensive health checks including database connectivity,
    admin user availability, and configuration validation.
    """

    def __init__(self, **kwargs):
        """Initialize the health command."""
        super().__init__(**kwargs)
        self.health_service = self.get_service(HealthService)

    def execute(self, **kwargs: Any) -> int:
        """Run system health checks.

        Checks database connection, admin users, and system configuration.
        Displays detailed status for each component.

        Returns:
            0 if all checks pass, 1 if any checks fail
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
            f'  Database: {db_info.database}',
            f'  Host: {db_info.host}:{db_info.port}',
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
    """Check system health and display status.

    Runs comprehensive health checks and shows results.
    """
    command = HealthCommand()
    return command.execute()
