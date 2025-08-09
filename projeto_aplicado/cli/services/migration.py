"""Migration service for database operations following clean architecture."""

import os
import subprocess
from contextlib import contextmanager
from importlib import reload
from typing import Any, Dict, List, Tuple

from projeto_aplicado.cli.base.service import BaseService


class MigrationService(BaseService):
    """Service for handling database migrations and setup operations.

    Implements Alembic operations following SOLID principles:
    - Single Responsibility: Only handles migration operations
    - Open/Closed: Easy to extend with new migration operations
    - Dependency Inversion: Depends on abstractions, not concretions
    """

    def __init__(self, db_host: str = 'localhost'):
        """Initialize migration service with database configuration.

        Args:
            db_host: Database hostname (default: localhost for development)
        """
        super().__init__()
        self.db_host = db_host

    def validate_input(self, **kwargs) -> bool:
        """Validate migration service inputs.

        Returns:
            bool: Always True as migration service has no specific validation
        """
        return True

    @contextmanager
    def _database_environment(self):
        """Context manager to set database environment variables."""
        original_hostname = os.environ.get('POSTGRES_HOSTNAME')
        try:
            os.environ['POSTGRES_HOSTNAME'] = self.db_host
            # Force reload of settings to pick up new environment
            from projeto_aplicado import settings

            reload(settings)
            yield
        finally:
            if original_hostname:
                os.environ['POSTGRES_HOSTNAME'] = original_hostname
            else:
                os.environ.pop('POSTGRES_HOSTNAME', None)
            # Reload settings back to original state
            from projeto_aplicado import settings

            reload(settings)

    def execute_operation(self, operation: str, **kwargs) -> Any:
        """Execute migration operation.

        Args:
            operation: Type of operation ('init', 'upgrade', 'downgrade', etc.)
            **kwargs: Additional parameters for the operation

        Returns:
            Any: Result of the operation

        Raises:
            ValueError: For unknown operations
        """
        with self._database_environment():
            if operation == 'init':
                return self._init_database(**kwargs)
            elif operation == 'upgrade':
                return self._upgrade_migrations(**kwargs)
            elif operation == 'downgrade':
                return self._downgrade_migrations(**kwargs)
            elif operation == 'current':
                return self._current_migration()
            elif operation == 'history':
                return self._migration_history(**kwargs)
            elif operation == 'create':
                return self._create_migration(**kwargs)
            elif operation == 'reset':
                return self._reset_database(**kwargs)
            elif operation == 'status':
                return self._database_status()
            else:
                raise ValueError(f'Unknown operation: {operation}')

    def _run_alembic_command(self, command: List[str]) -> Tuple[int, str, str]:
        """Run an Alembic command and return result.

        Args:
            command: Alembic command as list of strings

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                check=False,
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, '', str(e)

    def _init_database(self, **kwargs) -> Dict[str, Any]:
        """Initialize database with migrations.

        Returns:
            Dict containing operation result
        """
        # Check if alembic is already initialized
        if os.path.exists('alembic.ini') and os.path.exists('migrations'):
            # Run upgrade to head
            return_code, stdout, stderr = self._run_alembic_command([
                'alembic',
                'upgrade',
                'head',
            ])

            if return_code == 0:
                return {
                    'success': True,
                    'message': 'Database initialized successfully',
                    'details': stdout.strip()
                    if stdout.strip()
                    else 'No pending migrations',
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to initialize database',
                    'error': stderr.strip() or stdout.strip(),
                }
        else:
            return {
                'success': False,
                'message': 'Alembic not configured. Run alembic init first.',
                'error': 'Missing alembic.ini or migrations directory',
            }

    def _upgrade_migrations(
        self, revision: str = 'head', **kwargs
    ) -> Dict[str, Any]:
        """Upgrade database to specified revision.

        Args:
            revision: Target revision (default: head)

        Returns:
            Dict containing operation result
        """
        return_code, stdout, stderr = self._run_alembic_command([
            'alembic',
            'upgrade',
            revision,
        ])

        if return_code == 0:
            return {
                'success': True,
                'message': f'Database upgraded to {revision}',
                'details': stdout.strip()
                if stdout.strip()
                else f'Upgraded to {revision}',
            }
        else:
            return {
                'success': False,
                'message': f'Failed to upgrade to {revision}',
                'error': stderr.strip() or stdout.strip(),
            }

    def _downgrade_migrations(
        self, revision: str = '-1', **kwargs
    ) -> Dict[str, Any]:
        """Downgrade database to specified revision.

        Args:
            revision: Target revision (default: -1 for one step back)

        Returns:
            Dict containing operation result
        """
        return_code, stdout, stderr = self._run_alembic_command([
            'alembic',
            'downgrade',
            revision,
        ])

        if return_code == 0:
            return {
                'success': True,
                'message': f'Database downgraded to {revision}',
                'details': stdout.strip()
                if stdout.strip()
                else f'Downgraded to {revision}',
            }
        else:
            return {
                'success': False,
                'message': f'Failed to downgrade to {revision}',
                'error': stderr.strip() or stdout.strip(),
            }

    def _current_migration(self) -> Dict[str, Any]:
        """Get current migration revision.

        Returns:
            Dict containing current revision info
        """
        return_code, stdout, stderr = self._run_alembic_command([
            'alembic',
            'current',
        ])

        if return_code == 0:
            current = stdout.strip()
            return {
                'success': True,
                'message': 'Current migration retrieved',
                'current': current if current else 'No migrations applied',
                'details': current,
            }
        else:
            return {
                'success': False,
                'message': 'Failed to get current migration',
                'error': stderr.strip() or stdout.strip(),
            }

    def _migration_history(
        self, verbose: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """Get migration history.

        Args:
            verbose: Include verbose output

        Returns:
            Dict containing migration history
        """
        command = ['alembic', 'history']
        if verbose:
            command.append('--verbose')

        return_code, stdout, stderr = self._run_alembic_command(command)

        if return_code == 0:
            return {
                'success': True,
                'message': 'Migration history retrieved',
                'history': stdout.strip()
                if stdout.strip()
                else 'No migration history',
                'details': stdout.strip(),
            }
        else:
            return {
                'success': False,
                'message': 'Failed to get migration history',
                'error': stderr.strip() or stdout.strip(),
            }

    def _create_migration(self, message: str, **kwargs) -> Dict[str, Any]:
        """Create a new migration.

        Args:
            message: Migration message/description

        Returns:
            Dict containing operation result
        """
        if not message:
            return {
                'success': False,
                'message': 'Migration message is required',
                'error': 'Please provide a message for the migration',
            }

        return_code, stdout, stderr = self._run_alembic_command([
            'alembic',
            'revision',
            '--autogenerate',
            '-m',
            message,
        ])

        if return_code == 0:
            return {
                'success': True,
                'message': f'Migration "{message}" created successfully',
                'details': stdout.strip()
                if stdout.strip()
                else 'Migration created',
            }
        else:
            return {
                'success': False,
                'message': f'Failed to create migration "{message}"',
                'error': stderr.strip() or stdout.strip(),
            }

    def _reset_database(self, force: bool = False, **kwargs) -> Dict[str, Any]:
        """Reset database (dangerous operation).

        Args:
            force: Force reset without confirmation

        Returns:
            Dict containing operation result
        """
        if not force:
            return {
                'success': False,
                'message': 'Database reset requires --force flag',
                'error': 'This is a destructive operation. Use --force to confirm.',
            }

        # First downgrade to base
        downgrade_result = self._downgrade_migrations('base')
        if not downgrade_result['success']:
            return downgrade_result

        # Then upgrade to head
        upgrade_result = self._upgrade_migrations('head')
        if upgrade_result['success']:
            return {
                'success': True,
                'message': 'Database reset successfully',
                'details': 'Database downgraded to base and upgraded to head',
            }
        else:
            return upgrade_result

    def _database_status(self) -> Dict[str, Any]:
        """Get database status and migration info.

        Returns:
            Dict containing database status
        """
        # Get current migration
        current_result = self._current_migration()

        # Check if database is accessible
        try:
            from projeto_aplicado.cli.services.database import DatabaseService

            db_service = DatabaseService(self.db_host)
            connection_ok = db_service.test_connection()
        except Exception:
            connection_ok = False

        status = {
            'success': True,
            'message': 'Database status retrieved',
            'connection': 'OK' if connection_ok else 'FAILED',
            'current_migration': current_result.get('current', 'Unknown'),
            'alembic_configured': os.path.exists('alembic.ini'),
            'migrations_dir': os.path.exists('migrations'),
        }

        return status
