"""Shell setup commands for foodtruck-cli."""

from typing import Optional

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.shell import ShellService


class SetupCommand(BaseCommand):
    """Shell setup command.

    Helps users configure their shell to use foodtruck-cli directly.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize setup command with dependency injection.

        Args:
            console: Rich console for output (injected dependency)
        """
        super().__init__(console)
        self.shell_service = ShellService()

    def execute(self) -> int:
        """Execute setup command (shows help).

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Shell Setup Commands', '⚙️')
        self.console.print('[blue]Available commands:[/blue]')
        self.console.print(
            '  • [cyan]path[/cyan]    - Show PATH configuration for foodtruck-cli'
        )
        self.console.print('  • [cyan]alias[/cyan]   - Generate shell aliases')
        self.console.print(
            '  • [cyan]install[/cyan] - Auto-configure shell (bash/zsh)'
        )
        self.console.print(
            '  • [cyan]check[/cyan]   - Check current shell configuration'
        )
        self.console.print(
            '\n[yellow]Use --help with any command for details[/yellow]'
        )
        return 0


class ShowPathCommand(BaseCommand):
    """Show PATH configuration command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.shell_service = ShellService()

    def execute(self) -> int:
        """Show PATH configuration instructions.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('PATH Configuration', '🛤️')

        try:
            result = self.shell_service.execute_operation('show_path')

            # Project info
            self.console.print('[bold blue]Project Information:[/bold blue]')
            self.print_info(f'Project root: {result["project_root"]}')
            self.print_info(f'Virtual env: {result["venv_path"]}')
            self.print_info(f'CLI script: {result["cli_path"]}')
            self.console.print()

            # Current status
            if result['cli_in_path']:
                self.print_success('✅ foodtruck-cli is accessible in PATH')
            else:
                self.print_warning('⚠️ foodtruck-cli not found in PATH')

            self.console.print()

            # Instructions
            self.console.print(
                '[bold blue]Manual Setup Instructions:[/bold blue]'
            )
            self.console.print(
                '[yellow]Option 1: Activate virtual environment[/yellow]'
            )
            self.console.print(f'  source {result["activation_script"]}')
            self.console.print('  foodtruck-cli --help')
            self.console.print()

            self.console.print('[yellow]Option 2: Use full path[/yellow]')
            self.console.print(f'  {result["cli_path"]} --help')
            self.console.print()

            self.console.print(
                '[yellow]Option 3: Add to PATH permanently[/yellow]'
            )
            shell_config = result['shell_config_file']
            self.console.print(
                f'  echo \'export PATH="{result["venv_bin_path"]}:$PATH"\' >> {shell_config}'
            )
            self.console.print(f'  source {shell_config}')
            self.console.print()

            return 0

        except Exception as e:
            self.print_error(f'Failed to show PATH configuration: {str(e)}')
            return 1


class GenerateAliasCommand(BaseCommand):
    """Generate shell aliases command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.shell_service = ShellService()

    def execute(self, shell: str = 'auto') -> int:
        """Generate shell aliases.

        Args:
            shell: Shell type (bash, zsh, or auto)

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Shell Aliases', '🔗')

        try:
            result = self.shell_service.execute_operation(
                'generate_aliases', shell=shell
            )

            self.console.print(
                f'[bold blue]Generated aliases for {result["shell"]}:[/bold blue]'
            )
            self.console.print()

            # Show aliases
            for alias, command in result['aliases'].items():
                self.console.print(
                    f'[cyan]{alias}[/cyan] = [yellow]{command}[/yellow]'
                )

            self.console.print()

            # Show how to apply
            self.console.print(
                '[bold blue]To apply these aliases:[/bold blue]'
            )
            config_file = result['config_file']

            self.console.print('[yellow]1. Add to your shell config:[/yellow]')
            self.console.print(
                f'   echo "# Food Truck CLI aliases" >> {config_file}'
            )
            for alias, command in result['aliases'].items():
                self.console.print(
                    f'   echo "alias {alias}=\\"{command}\\"" >> {config_file}'
                )

            self.console.print()
            self.console.print('[yellow]2. Reload your shell:[/yellow]')
            self.console.print(f'   source {config_file}')
            self.console.print()

            return 0

        except Exception as e:
            self.print_error(f'Failed to generate aliases: {str(e)}')
            return 1


class AutoInstallCommand(BaseCommand):
    """Auto-install shell configuration command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.shell_service = ShellService()

    def execute(self, shell: str = 'auto', force: bool = False) -> int:
        """Auto-configure shell.

        Args:
            shell: Shell type (bash, zsh, or auto)
            force: Force overwrite existing configuration

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Auto Shell Configuration', '🚀')

        try:
            result = self.shell_service.execute_operation(
                'auto_install', shell=shell, force=force
            )

            if result['success']:
                self.print_success(
                    f'✅ Configured {result["shell"]} successfully!'
                )
                self.print_info(f'📁 Modified: {result["config_file"]}')

                if result.get('backup_created'):
                    self.print_info(f'💾 Backup: {result["backup_file"]}')

                self.console.print()
                self.console.print('[bold blue]Next steps:[/bold blue]')
                self.console.print(
                    f'1. Reload shell: [cyan]source {result["config_file"]}[/cyan]'
                )
                self.console.print(
                    '2. Test command: [cyan]foodtruck-cli --help[/cyan]'
                )

                return 0
            else:
                self.print_error('❌ Failed to configure shell')
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(
                f'Failed to auto-install shell configuration: {str(e)}'
            )
            return 1


class CheckSetupCommand(BaseCommand):
    """Check shell setup command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.shell_service = ShellService()

    def execute(self) -> int:
        """Check current shell configuration.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Shell Configuration Check', '🔍')

        try:
            result = self.shell_service.execute_operation('check_setup')

            # Shell info
            self.console.print('[bold blue]Shell Information:[/bold blue]')
            self.print_info(f'Current shell: {result["current_shell"]}')
            self.print_info(f'Config file: {result["config_file"]}')
            self.console.print()

            # CLI accessibility
            self.console.print('[bold blue]CLI Accessibility:[/bold blue]')
            if result['cli_in_path']:
                self.print_success('✅ foodtruck-cli accessible via PATH')
            else:
                self.print_warning('⚠️ foodtruck-cli not in PATH')

            if result['venv_active']:
                self.print_success('✅ Virtual environment is active')
            else:
                self.print_warning('⚠️ Virtual environment not active')

            # Aliases
            aliases = result.get('aliases_found', [])
            if aliases:
                self.console.print()
                self.console.print('[bold blue]Found Aliases:[/bold blue]')
                for alias in aliases:
                    self.print_success(f'✅ {alias}')
            else:
                self.console.print()
                self.print_warning('⚠️ No food truck aliases found')

            self.console.print()

            # Recommendations
            if not result['cli_in_path'] and not result['venv_active']:
                self.print_info(
                    '💡 Run [cyan]setup install[/cyan] to auto-configure your shell'
                )
            elif not aliases:
                self.print_info(
                    '💡 Run [cyan]setup alias[/cyan] to create convenient aliases'
                )

            return 0

        except Exception as e:
            self.print_error(f'Failed to check setup: {str(e)}')
            return 1


# Create the setup app with sub-commands
setup_app = cyclopts.App(
    name='setup',
    help='Shell setup and configuration commands',
)


# Register setup commands
@setup_app.default
def setup_default() -> int:
    """Shell setup and configuration commands."""
    command = SetupCommand()
    return command.execute()


@setup_app.command
def path() -> int:
    """Show PATH configuration for foodtruck-cli."""
    command = ShowPathCommand()
    return command.execute()


@setup_app.command
def alias(shell: str = 'auto') -> int:
    """Generate shell aliases.

    Args:
        shell: Shell type (bash, zsh, or auto)
    """
    command = GenerateAliasCommand()
    return command.execute(shell)


@setup_app.command
def install(shell: str = 'auto', force: bool = False) -> int:
    """Auto-configure shell for foodtruck-cli access.

    Args:
        shell: Shell type (bash, zsh, or auto)
        force: Force overwrite existing configuration
    """
    command = AutoInstallCommand()
    return command.execute(shell, force)


@setup_app.command
def check() -> int:
    """Check current shell configuration."""
    command = CheckSetupCommand()
    return command.execute()
