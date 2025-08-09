"""Main CLI application using clean architecture and SOLID principles."""

import os
from pathlib import Path

from cyclopts import App
from rich.console import Console

from projeto_aplicado.cli.commands.admin import admin_app
from projeto_aplicado.cli.commands.completions import completions_app
from projeto_aplicado.cli.commands.database import database_app
from projeto_aplicado.cli.commands.health import health_app
from projeto_aplicado.cli.commands.setup import setup_app


def _auto_setup_aliases_if_needed(console: Console) -> None:
    """Auto-setup aliases if this is the first time using the CLI.

    Args:
        console: Rich console for output
    """
    # Check if aliases are already configured
    shell_config_files = {
        'bash': Path.home() / '.bashrc',
        'zsh': Path.home() / '.zshrc',
        'fish': Path.home() / '.config' / 'fish' / 'config.fish',
    }

    # Check current shell
    shell_env = os.environ.get('SHELL', '')
    if shell_env:
        current_shell = Path(shell_env).name
    else:
        current_shell = 'unknown'

    # Get the appropriate config file
    config_file = None
    if current_shell in shell_config_files:
        config_file = shell_config_files[current_shell]
    else:
        # Fallback to existing configs
        for shell, path in shell_config_files.items():
            if path.exists():
                config_file = path
                current_shell = shell
                break

    if not config_file or not config_file.exists():
        return

    # Check if aliases are already installed
    try:
        content = config_file.read_text()
        if 'Food Truck CLI aliases' in content:
            return  # Already configured
    except Exception:
        return  # Can't read file, skip auto-setup

    # First time use - offer to setup aliases
    console.print()
    console.print('[bold yellow]🎉 Welcome to Food Truck CLI![/bold yellow]')
    console.print('[yellow]Setting up convenient aliases for you...[/yellow]')

    try:
        from projeto_aplicado.cli.services.shell import ShellService

        shell_service = ShellService()
        result = shell_service.execute_operation(
            'auto_install', shell=current_shell
        )

        if result.get('success'):
            console.print('[green]✅ Aliases configured successfully![/green]')
            console.print(
                f'[green]📁 Modified: {result.get("config_file", "shell config")}[/green]'
            )
            console.print()
            console.print(
                '[bold cyan]💡 Quick commands now available:[/bold cyan]'
            )
            console.print('  • [cyan]ftcli[/cyan] - Main CLI')
            console.print('  • [cyan]ft-health[/cyan] - Quick health check')
            console.print('  • [cyan]ft-admin[/cyan] - Admin commands')
            console.print('  • [cyan]ft-db[/cyan] - Database commands')
            console.print()
            console.print(
                '[yellow]💡 Reload your shell: [bold]source ~/.{}rc[/bold][/yellow]'.format(
                    current_shell
                )
            )
            console.print()
        else:
            console.print(
                '[yellow]⚠️ Could not auto-configure aliases[/yellow]'
            )
            console.print(
                '[yellow]💡 Run manually: [bold]uv run python -m projeto_aplicado.cli.app setup install[/bold][/yellow]'
            )
            console.print()
    except Exception:
        console.print('[yellow]⚠️ Could not auto-configure aliases[/yellow]')
        console.print(
            '[yellow]💡 Run manually: [bold]uv run python -m projeto_aplicado.cli.app setup install[/bold][/yellow]'
        )
        console.print()


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
    app.command(setup_app, name='setup')
    app.command(completions_app, name='completions')

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
        # Auto-setup aliases on first use
        _auto_setup_aliases_if_needed(app.console)

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
            '  • [cyan]setup[/cyan]     - Shell setup and configuration'
        )
        app.console.print(
            '  • [cyan]completions[/cyan] - Shell completion management'
        )
        app.console.print(
            '  • [cyan]version[/cyan]   - Show version information'
        )
        app.console.print()
        app.console.print(
            '[yellow]Use --help with any command for details[/yellow]'
        )
        app.console.print(
            '[yellow]Example: uv run python -m projeto_aplicado.cli.app database --help[/yellow]'
        )

    return app


# Create the app instance
app = create_cli_app()

if __name__ == '__main__':
    app()
