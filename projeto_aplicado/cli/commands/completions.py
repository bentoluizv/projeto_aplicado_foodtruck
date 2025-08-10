"""Shell completions commands for foodtruck-cli."""

from typing import Optional

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.completions import CompletionsService


class CompletionsCommand(BaseCommand):
    """Manage shell completions for foodtruck-cli.

    Generate, install, and manage tab completion scripts
    for bash, zsh, and fish shells.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize completions command with dependency injection.

        Args:
            console: Rich console for output (injected dependency)
        """
        super().__init__(console)
        self.completions_service = self.get_service(CompletionsService)

    def execute(self) -> int:
        """Execute completions command (shows help).

        Returns:
            int: Exit code (0 for success)
        """
        msg = (
            '[bold blue]🔧 Shell Completions Commands[/bold blue]\n'
            '[blue]Available commands:[/blue]\n'
            '  • [cyan]generate[/cyan] - Generate completion script\n'
            '  • [cyan]install[/cyan]  - Install completions for current shell\n'  # noqa: E501
            '  • [cyan]status[/cyan]   - Check completion installation status\n'  # noqa: E501
            '  • [cyan]uninstall[/cyan] - Remove installed completions\n'
            '\n[yellow]Use --help with any command for details[/yellow]'
        )
        self.console.print(msg)
        return 0


class GenerateCompletionsCommand(BaseCommand):
    """Generate shell completion scripts.

    Creates tab completion scripts for supported shells.
    Can output to stdout or save to a file.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = self.get_service(CompletionsService)

    def execute(
        self, shell: str = 'bash', output: Optional[str] = None
    ) -> int:
        """Generate completion script.

        Args:
            shell: Shell type (bash, zsh, fish)
            output: Output file path (stdout if not provided)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        try:
            result = self.completions_service.execute_operation(
                'generate', shell=shell, output=output
            )

            if result.success:
                if output:
                    msg_parts = [
                        f'[green]✅ Completion script generated: {output}[/green]',  # noqa: E501
                        f'[blue]🐚 Shell: {shell}[/blue]',
                        '',
                        '[bold blue]Installation Instructions:[/bold blue]',
                    ]

                    # Add instructions
                    if result.install_instructions:
                        for instruction in result.install_instructions:
                            msg_parts.append(f'  {instruction}')

                    msg_parts.extend([
                        '',
                        '[blue]💡 Or use [cyan]completions install[/cyan] '
                        'for automatic installation[/blue]',
                    ])

                    msg = '\n'.join(msg_parts)
                    self.console.print(msg)
                else:
                    # Output to stdout
                    print(result.script)

                return 0
            else:
                msg_parts = [
                    '[red]❌ Failed to generate completion script[/red]'
                ]
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

                msg = '\n'.join(msg_parts)
                self.console.print(msg)
                return 1

        except Exception as e:
            self.print_error(f'Failed to generate completions: {str(e)}')
            return 1


class InstallCompletionsCommand(BaseCommand):
    """Install completions command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = self.get_service(CompletionsService)

    def execute(self, shell: str = 'auto', force: bool = False) -> int:
        """Install completion script.

        Args:
            shell: Shell type (bash, zsh, fish, auto)
            force: Force reinstall if already installed

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Install Shell Completions', '📦')

        try:
            result = self.completions_service.execute_operation(
                'install', shell=shell, force=force
            )

            msg_parts = []
            if result.success:
                msg_parts.extend([
                    f'[green]✅ Completions installed for {result.shell}![/green]',  # noqa: E501
                    f'[blue]📁 Location: {result.install_path}[/blue]',
                ])

                if result.backup_created:
                    msg_parts.append(
                        f'[blue]💾 Backup: {result.backup_path}[/blue]'
                    )

                msg_parts.extend([
                    '',
                    '[bold blue]Next steps:[/bold blue]',
                    '1. Restart your shell or run:',
                    f'   [cyan]{result.reload_command}[/cyan]',
                    '2. Test completion:',
                    '   [cyan]foodtruck-cli <TAB><TAB>[/cyan]',
                ])
            else:
                msg_parts.append('[red]❌ Failed to install completions[/red]')
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )  # noqa: E501

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to install completions: {str(e)}')
            return 1


class StatusCompletionsCommand(BaseCommand):
    """Check completions status command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = self.get_service(CompletionsService)

    def execute(self) -> int:
        """Check completion installation status.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Completions Status', '📊')

        try:
            result = self.completions_service.execute_operation('status')

            msg_parts = [
                '[bold blue]Shell Information:[/bold blue]',
                f'  Current shell: {result.current_shell}',
                f'  Completion support: {result.completion_support}',
                '',
                '[bold blue]Installation Status:[/bold blue]',
            ]

            # Add installation status for each shell
            for shell, status in result.shells.items():
                if status.installed:
                    msg_parts.append(
                        f'[green]✅ {shell}: Installed at {status.path}[/green]'
                    )
                else:
                    msg_parts.append(
                        f'[yellow]⚠️ {shell}: Not installed[/yellow]'
                    )

            # Add test status
            msg_parts.append('')
            if result.can_test:
                msg_parts.extend([
                    '[bold blue]Testing:[/bold blue]',
                    '[blue]💡 Test completions: [cyan]foodtruck-cli <TAB><TAB>[/cyan][/blue]',
                ])
            else:
                msg_parts.append(
                    '[yellow]⚠️ Cannot test completions - shell not supported '
                    'or not installed[/yellow]'
                )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)

            return 0

        except Exception as e:
            self.print_error(f'Failed to check completions status: {str(e)}')
            return 1


class UninstallCompletionsCommand(BaseCommand):
    """Uninstall completions command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = self.get_service(CompletionsService)

    def execute(self, shell: str = 'auto') -> int:
        """Uninstall completion script.

        Args:
            shell: Shell type (bash, zsh, fish, auto, all)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Uninstall Shell Completions', '🗑️')

        try:
            result = self.completions_service.execute_operation(
                'uninstall', shell=shell
            )

            msg_parts = []
            if result.success:
                if result.removed:
                    msg_parts.append(
                        f'[green]✅ Completions removed for: {", ".join(result.removed)}[/green]'
                    )
                    if result.paths:
                        for shell_name in result.removed:
                            path = result.paths.get(shell_name)
                            if path:
                                msg_parts.append(
                                    f'[blue]📁 Removed: {path}[/blue]'
                                )
                else:
                    msg_parts.append(
                        '[blue]ℹ️ No completions were installed[/blue]'
                    )

                msg_parts.extend([
                    '',
                    '[blue]💡 Restart your shell to apply changes[/blue]',
                ])
            else:
                msg_parts.append(
                    '[red]❌ Failed to uninstall completions[/red]'
                )
                if result.error:
                    msg_parts.append(
                        f'[yellow]Details: {result.error}[/yellow]'
                    )

            msg = '\n'.join(msg_parts)
            self.console.print(msg)
            return 0 if result.success else 1

        except Exception as e:
            self.print_error(f'Failed to uninstall completions: {str(e)}')
            return 1


# Create the completions app with sub-commands
completions_app = cyclopts.App(
    name='completions',
    help='Shell completion management commands',
)


# Register completions commands
@completions_app.default
def completions_default() -> int:
    """Manage shell tab completions - generate, install, and maintain.

    Use subcommands to work with completion scripts for your shell.
    """
    command = CompletionsCommand()
    return command.execute()


@completions_app.command
def generate(shell: str = 'bash', output: Optional[str] = None) -> int:
    """Generate completion script.

    Args:
        shell: Shell type (bash, zsh, fish)
        output: Output file path (stdout if not provided)
    """
    command = GenerateCompletionsCommand()
    return command.execute(shell, output)


@completions_app.command
def install(shell: str = 'auto', force: bool = False) -> int:
    """Install completion script.

    Args:
        shell: Shell type (bash, zsh, fish, auto)
        force: Force reinstall if already installed
    """
    command = InstallCompletionsCommand()
    return command.execute(shell, force)


@completions_app.command
def status() -> int:
    """Check completion installation status."""
    command = StatusCompletionsCommand()
    return command.execute()


@completions_app.command
def uninstall(shell: str = 'auto') -> int:
    """Uninstall completion script.

    Args:
        shell: Shell type (bash, zsh, fish, auto, all)
    """
    command = UninstallCompletionsCommand()
    return command.execute(shell)
