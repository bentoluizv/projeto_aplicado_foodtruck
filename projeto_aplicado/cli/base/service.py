"""Abstract base service class for CLI operations."""

from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Abstract base class for CLI services.

    Follows the Single Responsibility Principle by focusing on specific service operations.
    Follows the Interface Segregation Principle by providing focused interfaces.
    """

    @abstractmethod
    def validate_input(self, **kwargs: Any) -> bool:
        """Validate input parameters.

        Args:
            **kwargs: Parameters to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    @abstractmethod
    def execute_operation(self, **kwargs: Any) -> Any:
        """Execute the main service operation.

        Args:
            **kwargs: Operation parameters

        Returns:
            Operation result
        """
        pass
