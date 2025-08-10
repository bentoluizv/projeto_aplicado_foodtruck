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
        self.shell_service = self.get_service(ShellService)

    def execute(self) -> int:
        """Execute setup command (shows help).

        Returns:
            int: Exit code (0 for success)
        """
        msg = (
            '[bold blue]⚙️ Shell Setup Commands[/bold blue]\n'
            '[blue]Available commands:[/blue]\n'
            '  • [cyan]path[/cyan]    - Show PATH configuration for foodtruck-cli\n'  # noqa: E501
            '  • [cyan]alias[/cyan]   - Generate shell aliases\n'
            '  • [cyan]install[/cyan] - Auto-configure shell (bash/zsh)\n'
            '  • [cyan]check[/cyan]   - Check current shell configuration\n'
            '\n[yellow]Use --help with any command for details[/yellow]'
        )
        self.console.print(msg)
        return 0


class ShowPathCommand(BaseCommand):
    """Show PATH configuration command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.shell_service = self.get_service(ShellService)

    def execute(self) -> int:
        """Show PATH configuration instructions.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('PATH Configuration', '🛤️')

        try:
            result = self.shell_service.execute_operation('show_path')

            msg_parts = [
                '[bold blue]Project Information:[/bold blue]',
                f'  Project root: {result.project_root}',
                f'  Virtual env: {result.venv_path}',
                f'  CLI script: {result.cli_path}',
                '',
                # Current status
                '[green]✅ foodtruck-cli is accessible in PATH[/green]'
                if result.cli_in_path
                else '[yellow]⚠️ foodtruck-cli not found in PATH[/yellow]',
                '',
                '[bold blue]Manual Setup Instructions:[/bold blue]',
                '[yellow]Option 1: Activate virtual environment[/yellow]',
                f'  source {result.activation_script}',
                '  foodtruck-cli --help',
                '',
                '[yellow]Option 2: Use full path[/yellow]',
                f'  {result.cli_path} --help',
                '',
                '[yellow]Option 3: Add to PATH permanently[/yellow]',
                f'  echo \'export PATH="{result.venv_bin_path}:$PATH"\' >> {result.shell_config_file}',  # noqa: E501
                f'  source {result.shell_config_file}',
            ]

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
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
        self.shell_service = self.get_service(ShellService)

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

            msg_parts = [
                f'[bold blue]Generated aliases for {result.shell}:[/bold blue]',
                '',
            ]

            # Show aliases
            for alias, command in result.aliases.items():
                msg_parts.append(
                    f'[cyan]{alias}[/cyan] = [yellow]{command}[/yellow]'
                )

            msg_parts.extend([
                '',
                '[bold blue]To apply these aliases:[/bold blue]',
                '[yellow]1. Add to your shell config:[/yellow]',
                f'   echo "# Food Truck CLI aliases" >> {result.config_file}',
            ])

            # Add alias commands
            for alias, command in result.aliases.items():
                msg_parts.append(
                    f'   echo "alias {alias}=\\"{command}\\"" >> {result.config_file}'  # noqa: E501
                )

            msg_parts.extend([
                '',
                '[yellow]2. Reload your shell:[/yellow]',
                f'   source {result.config_file}',
            ])

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
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
        self.shell_service = self.get_service(ShellService)

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

            msg_parts = []
            if result.success:
                msg_parts.extend([
                    f'[green]✅ Configured {result.shell} successfully![/green]',  # noqa: E501
                    f'[blue]📁 Modified: {result.config_file}[/blue]',
                ])

                if result.backup_created:
                    msg_parts.append(
                        f'[blue]💾 Backup: {result.backup_file}[/blue]'
                    )

                msg_parts.extend([
                    '',
                    '[bold blue]Next steps:[/bold blue]',
                    f'1. Reload shell: [cyan]source {result.config_file}[/cyan]',  # noqa: E501
                    '2. Test command: [cyan]foodtruck-cli --help[/cyan]',
                ])
            else:
                msg_parts.append('[red]❌ Failed to configure shell[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

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
        self.shell_service = self.get_service(ShellService)

    def execute(self) -> int:
        """Check current shell configuration.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Shell Configuration Check', '🔍')

        try:
            result = self.shell_service.execute_operation('check_setup')

            msg_parts = [
                '[bold blue]Shell Information:[/bold blue]',
                f'  Current shell: {result.current_shell}',
                f'  Config file: {result.config_file}',
                '',
                '[bold blue]CLI Accessibility:[/bold blue]',
                '[green]✅ foodtruck-cli accessible via PATH[/green]'
                if result.cli_in_path
                else '[yellow]⚠️ foodtruck-cli not in PATH[/yellow]',
                '[green]✅ Virtual environment is active[/green]'
                if result.venv_active
                else '[yellow]⚠️ Virtual environment not active[/yellow]',
            ]

            # Aliases
            aliases = result.aliases_found
            if aliases:
                msg_parts.extend(['', '[bold blue]Found Aliases:[/bold blue]'])
                for alias in aliases:
                    msg_parts.append(f'[green]✅ {alias}[/green]')
            else:
                msg_parts.extend([
                    '',
                    '[yellow]⚠️ No food truck aliases found[/yellow]',
                ])

            # Recommendations
            if not result.cli_in_path and not result.venv_active:
                msg_parts.extend([
                    '',
                    '[blue]💡 Run [cyan]setup install[/cyan] to auto-configure your shell[/blue]',  # noqa: E501
                ])
            elif not aliases:
                msg_parts.extend([
                    '',
                    '[blue]💡 Run [cyan]setup alias[/cyan] to create convenient aliases[/blue]',  # noqa: E501
                ])

            msg = '\n'.join(msg_parts)
            self.console.print(msg)

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
