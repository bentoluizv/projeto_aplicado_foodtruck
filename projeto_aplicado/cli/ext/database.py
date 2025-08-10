"""Database service for CLI operations providing connection status and information."""

from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, create_engine, text

from projeto_aplicado.cli.schemas import DatabaseInfo
from projeto_aplicado.settings import get_settings
from projeto_aplicado.utils import get_db_url


class DatabaseService:
    """Database service that provides connection status and information."""

    def __init__(self):
        """Initialize database service with CLI-specific connection."""
        self.settings = get_settings()
        config = {
            'url': get_db_url(self.settings, cli=True),
            'echo': self.settings.DB_ECHO,
        }
        self.engine = create_engine(**config)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a CLI-specific database session.

        Yields:
            Session: Database session configured for CLI use
        """
        session = Session(self.engine)
        try:
            yield session
        finally:
            session.close()

    def test_connection(self) -> bool:
        """Test database connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_session() as session:
                result = session.exec(text('SELECT 1')).first()
                return result is not None
        except Exception:
            return False

    def get_database_info(self) -> DatabaseInfo:
        """Get database information for display.

        Returns:
            DatabaseInfo with connection details
        """
        try:
            status = 'connected' if self.test_connection() else 'disconnected'
            return DatabaseInfo(
                database=self.settings.POSTGRES_DB,
                host=self.settings.POSTGRES_HOSTNAME_CLI,
                container=self.settings.POSTGRES_HOSTNAME_CLI,
                port=self.settings.POSTGRES_PORT,
                status=status,
            )
        except Exception as e:
            return DatabaseInfo(
                database='unknown',
                host=self.settings.POSTGRES_HOSTNAME_CLI,
                container=self.settings.POSTGRES_HOSTNAME_CLI,
                port='unknown',
                status=f'error: {str(e)}',
            )
