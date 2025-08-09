"""Main CLI application using clean architecture and SOLID principles."""

import os

from cyclopts import App
from rich.console import Console

from projeto_aplicado.cli.commands.admin import admin_app
from projeto_aplicado.cli.commands.database import database_app
from projeto_aplicado.cli.commands.health import health_app
from projeto_aplicado.cli.commands.install import install_app


def create_cli_app() -> App:
    """Create and configure the main CLI application.

    Factory function that follows the Dependency Inversion Principle
    by creating all dependencies and injecting them appropriately.

    Returns:
        Configured Cyclopts App instance
    """
    # Set default localhost for CLI usage
    os.environ.setdefault('POSTGRES_HOSTNAME', 'localhost')

    # Main application
    app = App(
        name='foodtruck-cli',
        help='Food Truck Management System CLI Tools',
        version='1.0.0',
    )
    app.console = Console()

    # Register sub-applications
    app.command(health_app, name='health')
    app.command(admin_app, name='admin')
    app.command(database_app, name='database')
    app.command(install_app, name='install')

    @app.command
    def version() -> None:
        """Show version information.

        Examples
        --------
        Show version:
            foodtruck-cli version
        """
        app.console.print(
            '[bold blue]🚚 Food Truck Management System[/bold blue]'
        )
        app.console.print(f'Version: {app.version}')
        app.console.print('Python CLI Framework: Cyclopts')
        app.console.print('Database: PostgreSQL with SQLModel')
        app.console.print('Web Framework: FastAPI')

    @app.default
    def default() -> None:
        """Default command that shows help information.

        Examples
        --------
        Show help:
            foodtruck-cli
        """
        app.console.print(
            '[bold blue]🚚 Food Truck Management System CLI[/bold blue]'
        )
        app.console.print(f'Version: {app.version}')
        app.console.print()
        app.console.print('[blue]Available commands:[/blue]')
        app.console.print(
            '  • [cyan]health[/cyan]    - Check system health status'
        )
        app.console.print(
            '  • [cyan]admin[/cyan]     - Admin user management commands'
        )
        app.console.print(
            '  • [cyan]database[/cyan]  - Database and migration management'
        )
        app.console.print(
            '  • [cyan]install[/cyan]   - Installation and environment setup'
        )
        app.console.print(
            '  • [cyan]version[/cyan]   - Show version information'
        )
        app.console.print()
        app.console.print(
            '[yellow]Use --help with any command for details[/yellow]'
        )
        app.console.print(
            '[yellow]Example: foodtruck-cli database --help[/yellow]'
        )

    return app


# Create the app instance
app = create_cli_app()

if __name__ == '__main__':
    app()
