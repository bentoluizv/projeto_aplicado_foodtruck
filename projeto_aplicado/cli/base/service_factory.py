"""Service factory for CLI commands."""

from typing import Dict, Type

from projeto_aplicado.cli.ext.database import DatabaseService
from projeto_aplicado.cli.services.completions import CompletionsService
from projeto_aplicado.cli.services.health import HealthService
from projeto_aplicado.cli.services.migration import MigrationService
from projeto_aplicado.cli.services.shell import ShellService
from projeto_aplicado.cli.services.user import UserService


class ServiceFactory:
    """Factory for creating and caching service instances."""

    _instances: Dict[Type, object] = {}

    @classmethod
    def get_databaseservice(cls) -> DatabaseService:
        """Get or create DatabaseService instance."""
        if DatabaseService not in cls._instances:
            cls._instances[DatabaseService] = DatabaseService()
        return cls._instances[DatabaseService]

    @classmethod
    def get_userservice(cls) -> UserService:
        """Get or create UserService instance."""
        if UserService not in cls._instances:
            db_service = cls.get_databaseservice()
            cls._instances[UserService] = UserService(db_service)
        return cls._instances[UserService]

    @classmethod
    def get_healthservice(cls) -> HealthService:
        """Get or create HealthService instance."""
        if HealthService not in cls._instances:
            db_service = cls.get_databaseservice()
            user_service = cls.get_userservice()
            cls._instances[HealthService] = HealthService(
                db_service, user_service
            )
        return cls._instances[HealthService]

    @classmethod
    def get_migrationservice(cls) -> MigrationService:
        """Get or create MigrationService instance."""
        if MigrationService not in cls._instances:
            cls._instances[MigrationService] = MigrationService()
        return cls._instances[MigrationService]

    @classmethod
    def get_shellservice(cls) -> ShellService:
        """Get or create ShellService instance."""
        if ShellService not in cls._instances:
            cls._instances[ShellService] = ShellService()
        return cls._instances[ShellService]

    @classmethod
    def get_completionsservice(cls) -> CompletionsService:
        """Get or create CompletionsService instance."""
        if CompletionsService not in cls._instances:
            cls._instances[CompletionsService] = CompletionsService()
        return cls._instances[CompletionsService]
