"""Database service for CLI operations following SOLID principles."""

import os
from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session

from projeto_aplicado.cli.base.service import BaseService


class DatabaseService(BaseService):
    """Database service that manages connections and operations.

    Follows Single Responsibility Principle: only handles database connections.
    Follows Dependency Inversion Principle: depends on abstractions, not concretions.
    """

    def __init__(self, db_host: str = 'localhost'):
        """Initialize the database service.

        Args:
            db_host: Database hostname, defaults to 'localhost'
        """
        self.db_host = db_host

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with proper environment setup.

        This method handles the complexity of environment variable management
        and module reloading internally, keeping the interface clean.

        Yields:
            Database session
        """
        # Store original hostname to restore later
        original_hostname = os.environ.get('POSTGRES_HOSTNAME')

        try:
            # Set the hostname for this operation
            os.environ['POSTGRES_HOSTNAME'] = self.db_host

            # Force reload of settings and database modules to pick up changes
            from importlib import reload

            from projeto_aplicado import settings
            from projeto_aplicado.ext.database import db

            reload(settings)
            reload(db)

            # Create and yield the session
            with Session(db.get_engine()) as session:
                yield session

        finally:
            # Restore original hostname
            if original_hostname is not None:
                os.environ['POSTGRES_HOSTNAME'] = original_hostname
            else:
                os.environ.pop('POSTGRES_HOSTNAME', None)

    def validate_input(self, **kwargs) -> bool:
        """Validate database connection parameters.

        Args:
            **kwargs: Parameters to validate

        Returns:
            True if valid
        """
        # Basic validation - can be extended
        return isinstance(self.db_host, str) and len(self.db_host.strip()) > 0

    def execute_operation(self, operation_func, **kwargs):
        """Execute a database operation with proper session management.

        Args:
            operation_func: Function to execute with the session
            **kwargs: Additional parameters for the operation

        Returns:
            Operation result
        """
        with self.get_session() as session:
            return operation_func(session, **kwargs)

    def test_connection(self) -> bool:
        """Test database connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_session() as session:
                # Simple query to test connection using SQLModel approach
                from sqlmodel import text

                result = session.exec(text('SELECT 1')).first()
                return result is not None
        except Exception:
            return False

    def get_database_info(self) -> dict:
        """Get database information for display.

        Returns:
            Dictionary with database info
        """
        try:
            # Force reload to get current settings
            from importlib import reload

            from projeto_aplicado import settings

            reload(settings)
            from projeto_aplicado.settings import get_settings

            settings_obj = get_settings()
            return {
                'database': settings_obj.POSTGRES_DB,
                'host': settings_obj.POSTGRES_HOSTNAME,
                'port': settings_obj.POSTGRES_PORT,
                'status': 'connected'
                if self.test_connection()
                else 'disconnected',
            }
        except Exception as e:
            return {
                'database': 'unknown',
                'host': self.db_host,
                'port': 'unknown',
                'status': f'error: {str(e)}',
            }
