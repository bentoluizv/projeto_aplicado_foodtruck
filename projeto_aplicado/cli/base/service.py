# noqa: E501
"""Abstract base service class for CLI operations."""

from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Abstract base class for CLI services.

    Provides a common interface for service operations with input validation
    and execution logic. All CLI services should inherit from this class
    and implement the validate_input and execute_operation methods.
    """

    @abstractmethod
    def validate_input(self, **kwargs: Any) -> bool:
        """Validate input parameters before executing the operation.

        This method should perform all necessary validation checks on the
        provided parameters to ensure they meet the service requirements.

        Args:
            **kwargs: Parameters to validate for the service operation

        Returns:
            True if all parameters are valid, False if validation fails
        """
        pass

    @abstractmethod
    def execute_operation(self, **kwargs: Any) -> Any:
        """Execute the main service operation logic.

        This method contains the core business logic for the service.
        It should only be called after successful validation.

        Args:
            **kwargs: Operation parameters that have been validated

        Returns:
            The result of the service operation (type depends on the service)
        """
        pass
