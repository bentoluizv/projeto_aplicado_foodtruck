"""Abstract base command class following SOLID principles."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from rich.console import Console


class BaseCommand(ABC):
    """Abstract base class for all CLI commands.

    Follows the Single Responsibility Principle by focusing only on command execution.
    Follows the Open/Closed Principle by allowing extension without modification.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize the command with a console for output.

        Args:
            console: Optional Rich console for styled output
        """
        self.console = console or Console()

    @abstractmethod
    def execute(self, **kwargs: Any) -> int:
        """Execute the command.

        Args:
            **kwargs: Command-specific arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        pass

    def print_success(self, message: str) -> None:
        """Print a success message."""
        self.console.print(f'[green]✓ {message}[/green]')

    def print_error(self, message: str) -> None:
        """Print an error message."""
        self.console.print(f'[red]✗ {message}[/red]')

    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        self.console.print(f'[yellow]⚠ {message}[/yellow]')

    def print_info(self, message: str) -> None:
        """Print an info message."""
        self.console.print(f'[blue]ℹ {message}[/blue]')

    def print_header(self, title: str, emoji: str = '🚚') -> None:
        """Print a styled header."""
        self.console.print(f'[bold blue]{emoji} {title}[/bold blue]')
