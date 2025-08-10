"""Abstract base command class for CLI command implementation."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from rich.console import Console

from projeto_aplicado.cli.base.service_factory import ServiceFactory


class BaseCommand(ABC):
    """Abstract base class for all CLI commands.

    Provides a common interface and utilities for command execution, including
    console output formatting and standardized exit codes. All CLI commands
    should inherit from this class and implement the execute method.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize the command with a console for output.

        Args:
            console: Optional Rich console instance for styled output.
            If not provided, a new Console instance will be created.
        """
        self.console = console or Console()
        self.service_factory = ServiceFactory()

    def get_service(self, service_type: Type) -> Any:
        """Get a service instance from the factory.

        Args:
            service_type: The type of service to get

        Returns:
            Service instance
        """
        method_name = f'get_{service_type.__name__.lower()}'
        factory_method = getattr(self.service_factory, method_name)
        return factory_method()

    @abstractmethod
    def execute(self, **kwargs: Any) -> int:
        """Execute the command logic.

        This method must be implemented by all subclasses to define the specific
        command behavior.

        Args:
            **kwargs: Command-specific arguments passed from the CLI

        Returns:
            Exit code indicating command success (0) or failure (non-zero)
        """  # noqa: E501
        pass

    def print_success(self, message: str) -> None:
        """Print a success message with green checkmark styling.

        Args:
            message: The success message to display
        """
        self.console.print(f'[green]✓ {message}[/green]')

    def print_error(self, message: str) -> None:
        """Print an error message with red X styling.

        Args:
            message: The error message to display
        """
        self.console.print(f'[red]✗ {message}[/red]')

    def print_warning(self, message: str) -> None:
        """Print a warning message with yellow warning symbol styling.

        Args:
            message: The warning message to display
        """
        self.console.print(f'[yellow]⚠ {message}[/yellow]')

    def print_info(self, message: str) -> None:
        """Print an informational message with blue info symbol styling.

        Args:
            message: The informational message to display
        """
        self.console.print(f'[blue]ℹ {message}[/blue]')

    def print_header(self, title: str, emoji: str = '🚚') -> None:
        """Print a styled header with emoji and bold blue text.

        Args:
            title: The header title to display
            emoji: Optional emoji to prefix the title (defaults to truck emoji)
        """
        self.console.print(f'[bold blue]{emoji} {title}[/bold blue]')
