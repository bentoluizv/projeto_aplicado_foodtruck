"""Installation and setup commands following clean architecture principles."""

from typing import Optional

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.installer import InstallerService


class InstallCommand(BaseCommand):
    """Installation operations command with clean architecture.

    Implements installation management following SOLID principles:
    - Single Responsibility: Only handles install command coordination
    - Open/Closed: Easy to extend with new install operations
    - Dependency Inversion: Depends on service abstractions
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize install command with dependency injection.

        Args:
            console: Rich console for output (injected dependency)
        """
        super().__init__(console)
        self.installer_service = InstallerService()

    def execute(self) -> int:
        """Execute install command (shows help).

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('Installation & Setup Commands', '🚀')
        self.console.print('[blue]Available commands:[/blue]')
        self.console.print(
            '  • [cyan]check[/cyan]   - Check system dependencies'
        )
        self.console.print(
            '  • [cyan]install[/cyan] - Install missing dependencies'
        )
        self.console.print(
            '  • [cyan]setup[/cyan]   - Set up project environment'
        )
        self.console.print(
            '  • [cyan]status[/cyan]  - Show comprehensive system status'
        )
        self.console.print(
            '\n[yellow]Use --help with any command for details[/yellow]'
        )
        return 0


class CheckDependenciesCommand(BaseCommand):
    """Check dependencies command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.installer_service = InstallerService()

    def execute(self) -> int:
        """Check system dependencies.

        Returns:
            int: Exit code (0 for success, 1 if missing dependencies)
        """
        self.print_header('Dependency Check', '🔍')

        try:
            result = self.installer_service.execute_operation('check')
            dependencies = result['dependencies']

            self.print_info(f'System: {result["system"]}')
            self.console.print()

            for tool, info in dependencies.items():
                if info['installed']:
                    version = info.get('version', 'Unknown version')
                    self.print_success(f'{tool}: {version}')
                else:
                    error = info.get('error', 'Not found')
                    self.print_error(f'{tool}: {error}')

            self.console.print()
            if result['all_installed']:
                self.print_success('✨ All dependencies are installed!')
                return 0
            else:
                self.print_warning('⚠️ Some dependencies are missing')
                self.print_info(
                    "Run 'install dependencies --auto' to install missing tools"
                )
                return 1

        except Exception as e:
            self.print_error(f'Failed to check dependencies: {str(e)}')
            return 1


class InstallDependenciesCommand(BaseCommand):
    """Install dependencies command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.installer_service = InstallerService()

    def execute(self, auto: bool = False) -> int:
        """Install missing dependencies.

        Args:
            auto: Install automatically without prompts

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Install Dependencies', '📦')

        if not auto:
            self.print_warning(
                'This will attempt to install missing dependencies'
            )
            self.print_info('Use --auto flag for automatic installation')

        try:
            result = self.installer_service.execute_operation(
                'install', auto=auto
            )

            # Display installation results
            for tool, install_result in result.get('results', {}).items():
                if tool == 'manual_install_required':
                    tools = install_result['tools']
                    self.print_warning(
                        f'Manual installation required for: {", ".join(tools)}'
                    )

                    instructions = install_result.get('instructions', {})
                    for manual_tool, instruction in instructions.items():
                        self.console.print(
                            f'  [yellow]{manual_tool}:[/yellow] {instruction}'
                        )
                elif install_result['success']:
                    self.print_success(install_result['message'])
                else:
                    self.print_error(install_result['message'])
                    if install_result.get('error'):
                        self.print_warning(
                            f'  Details: {install_result["error"]}'
                        )

            if result['success']:
                self.print_success('✨ Installation completed successfully!')
                if result.get('manual_steps_required'):
                    self.print_info(
                        '📋 Some tools require manual installation (see above)'
                    )
                return 0
            else:
                self.print_error('❌ Installation failed or incomplete')
                return 1

        except Exception as e:
            self.print_error(f'Failed to install dependencies: {str(e)}')
            return 1


class SetupProjectCommand(BaseCommand):
    """Setup project command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.installer_service = InstallerService()

    def execute(self) -> int:
        """Set up the project environment.

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self.print_header('Project Setup', '🎯')

        try:
            result = self.installer_service.execute_operation('setup')

            # Display setup steps
            for step in result.get('steps', []):
                if step['success']:
                    self.print_success(f'{step["step"]}: {step["message"]}')
                else:
                    self.print_error(f'{step["step"]}: {step["message"]}')
                    if step.get('error'):
                        self.print_warning(f'  Details: {step["error"]}')

            if result['success']:
                self.print_success('✨ Project setup completed!')
                self.print_info(
                    '🚀 You can now run the development server with: uv run task dev'
                )
                return 0
            else:
                self.print_error('❌ Project setup failed')
                return 1

        except Exception as e:
            self.print_error(f'Failed to set up project: {str(e)}')
            return 1


class SystemStatusCommand(BaseCommand):
    """System status command."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize with dependency injection."""
        super().__init__(console)
        self.installer_service = InstallerService()

    def execute(self) -> int:
        """Show comprehensive system status.

        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('System Status', '📊')

        try:
            result = self.installer_service.execute_operation('status')

            # System information
            system = result['system']
            self.console.print('[bold blue]System Information:[/bold blue]')
            self.console.print(f'  Platform: {system["platform"]}')
            self.console.print(
                f'  Python: {system["python_version"].split()[0]}'
            )
            self.console.print(f'  Architecture: {system["architecture"]}')
            self.console.print()

            # Dependencies status
            self.console.print('[bold blue]Dependencies:[/bold blue]')
            dependencies = result['dependencies']
            for tool, info in dependencies.items():
                if info['installed']:
                    version = info.get('version', 'Unknown').split('\n')[
                        0
                    ]  # First line only
                    self.print_success(f'{tool}: {version}')
                else:
                    self.print_error(f'{tool}: Not installed')
            self.console.print()

            # Project status
            project = result['project']
            self.console.print('[bold blue]Project Status:[/bold blue]')

            if project['in_project_dir']:
                self.print_success('In project directory: Yes')
            else:
                self.print_error('In project directory: No')

            if project['venv_exists']:
                self.print_success('Virtual environment: Created')
            else:
                self.print_warning('Virtual environment: Not found')

            if project['dependencies_installed']:
                self.print_success('Dependencies: Installed')
            else:
                self.print_warning('Dependencies: Not installed')

            self.console.print()

            # Overall readiness
            if result['ready_for_development']:
                self.print_success('🎉 Ready for development!')
            else:
                self.print_warning('⚠️ Setup incomplete')
                self.print_info(
                    "Run 'install setup' to complete project setup"
                )

            return 0

        except Exception as e:
            self.print_error(f'Failed to get system status: {str(e)}')
            return 1


# Create the install app with sub-commands
install_app = cyclopts.App(
    name='install',
    help='Installation and setup commands',
)


# Register install commands
@install_app.default
def install_default() -> int:
    """Installation and setup commands."""
    command = InstallCommand()
    return command.execute()


@install_app.command
def check() -> int:
    """Check system dependencies."""
    command = CheckDependenciesCommand()
    return command.execute()


@install_app.command
def dependencies(auto: bool = False) -> int:
    """Install missing dependencies.

    Args:
        auto: Install automatically without prompts
    """
    command = InstallDependenciesCommand()
    return command.execute(auto)


@install_app.command
def setup() -> int:
    """Set up project environment."""
    command = SetupProjectCommand()
    return command.execute()


@install_app.command
def status() -> int:
    """Show comprehensive system status."""
    command = SystemStatusCommand()
    return command.execute()
