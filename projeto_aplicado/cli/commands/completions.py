"""Shell completions commands for foodtruck-cli."""

from typing import Optional

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.completions import CompletionsService


class CompletionsCommand(BaseCommand):
    """Shell completions command.

    Generates and manages shell completion scripts for foodtruck-cli.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize completions command with dependency injection.

        Args:
            console: Rich console for output (injected dependency)
        """
        super().__init__(console)
        self.completions_service = CompletionsService()

    def execute(self) -> int:
        """Execute completions command (shows help).

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Shell Completions Commands', '🔧')
        self.console.print('[blue]Available commands:[/blue]')
        self.console.print(
            '  • [cyan]generate[/cyan] - Generate completion script'
        )
        self.console.print(
            '  • [cyan]install[/cyan]  - Install completions for current shell'
        )
        self.console.print(
            '  • [cyan]status[/cyan]   - Check completion installation status'
        )
        self.console.print(
            '  • [cyan]uninstall[/cyan] - Remove installed completions'
        )
        self.console.print(
            '\n[yellow]Use --help with any command for details[/yellow]'
        )
        return 0


class GenerateCompletionsCommand(BaseCommand):
    """Generate completions command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = CompletionsService()

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

            if result['success']:
                if output:
                    self.print_success(
                        f'✅ Completion script generated: {output}'
                    )
                    self.print_info(f'🐚 Shell: {shell}')

                    # Show installation instructions
                    self.console.print()
                    self.console.print(
                        '[bold blue]Installation Instructions:[/bold blue]'
                    )
                    instructions = result.get('install_instructions', [])
                    for instruction in instructions:
                        self.console.print(f'  {instruction}')

                    self.console.print()
                    self.print_info(
                        '💡 Or use [cyan]completions install[/cyan] '
                        'for automatic installation'
                    )
                else:
                    # Output to stdout
                    print(result['script'])

                return 0
            else:
                self.print_error('❌ Failed to generate completion script')
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to generate completions: {str(e)}')
            return 1


class InstallCompletionsCommand(BaseCommand):
    """Install completions command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = CompletionsService()

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

            if result['success']:
                self.print_success(
                    f'✅ Completions installed for {result["shell"]}!'
                )
                self.print_info(f'📁 Location: {result["install_path"]}')

                if result.get('backup_created'):
                    self.print_info(f'💾 Backup: {result["backup_path"]}')

                self.console.print()
                self.console.print('[bold blue]Next steps:[/bold blue]')
                self.console.print('1. Restart your shell or run:')
                self.console.print(
                    f'   [cyan]{result["reload_command"]}[/cyan]'
                )
                self.console.print('2. Test completion:')
                self.console.print('   [cyan]foodtruck-cli <TAB><TAB>[/cyan]')

                return 0
            else:
                self.print_error('❌ Failed to install completions')
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

        except Exception as e:
            self.print_error(f'Failed to install completions: {str(e)}')
            return 1


class StatusCompletionsCommand(BaseCommand):
    """Check completions status command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = CompletionsService()

    def execute(self) -> int:
        """Check completion installation status.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Completions Status', '📊')

        try:
            result = self.completions_service.execute_operation('status')

            # Shell info
            self.console.print('[bold blue]Shell Information:[/bold blue]')
            self.print_info(f'Current shell: {result["current_shell"]}')
            self.print_info(
                f'Completion support: {result["completion_support"]}'
            )
            self.console.print()

            # Installation status
            self.console.print('[bold blue]Installation Status:[/bold blue]')
            for shell, status in result['shells'].items():
                if status['installed']:
                    self.print_success(
                        f'✅ {shell}: Installed at {status["path"]}'
                    )
                else:
                    self.print_warning(f'⚠️ {shell}: Not installed')

            self.console.print()

            # Test status
            if result['can_test']:
                self.console.print('[bold blue]Testing:[/bold blue]')
                self.print_info(
                    '💡 Test completions: '
                    '[cyan]foodtruck-cli <TAB><TAB>[/cyan]'
                )
            else:
                self.print_warning(
                    '⚠️ Cannot test completions - shell not supported '
                    'or not installed'
                )

            return 0

        except Exception as e:
            self.print_error(f'Failed to check completions status: {str(e)}')
            return 1


class UninstallCompletionsCommand(BaseCommand):
    """Uninstall completions command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.completions_service = CompletionsService()

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

            if result['success']:
                removed = result.get('removed', [])
                if removed:
                    self.print_success(
                        f'✅ Completions removed for: {", ".join(removed)}'
                    )
                    for shell_name in removed:
                        path = result.get('paths', {}).get(shell_name)
                        if path:
                            self.print_info(f'📁 Removed: {path}')
                else:
                    self.print_info('ℹ️ No completions were installed')

                self.console.print()
                self.print_info('💡 Restart your shell to apply changes')

                return 0
            else:
                self.print_error('❌ Failed to uninstall completions')
                if result.get('error'):
                    self.print_warning(f'Details: {result["error"]}')
                return 1

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
    """Shell completion management commands."""
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
