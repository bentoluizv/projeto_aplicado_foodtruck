"""Integration tests for database commands."""

from unittest.mock import Mock, patch

import pytest

from projeto_aplicado.cli.commands.database import (
    DatabaseCommand,
    DatabaseStatusCommand,
    InitDatabaseCommand,
)
from projeto_aplicado.cli.schemas import (
    DatabaseInfo,
    MigrationResult,
    MigrationStatus,
)


class TestDatabaseCommand:
    """Integration tests for DatabaseCommand."""

    def test_database_help(self):
        """Test database command shows help."""
        command = DatabaseCommand()

        result = command.execute()

        assert result == 0


class TestDatabaseStatusCommand:
    """Integration tests for DatabaseStatusCommand."""

    def test_database_status_connected(self):
        """Test database status when connected."""
        command = DatabaseStatusCommand()

        mock_status = MigrationStatus(
            success=True,
            message='Database status retrieved',
            connection='OK',
            current_migration='abc123def456',
            alembic_configured=True,
            migrations_dir=True,
        )

        mock_db_info = DatabaseInfo(
            database='foodtruck',
            host='localhost',
            container='localhost',
            port='5432',
            status='connected',
        )

        with (
            patch.object(
                command.migration_service,
                'execute_operation',
                return_value=mock_status,
            ),
            patch.object(
                command.database_service,
                'get_database_info',
                return_value=mock_db_info,
            ),
        ):
            result = command.execute()

            assert result == 0

            # Verify services were called correctly
            command.migration_service.execute_operation.assert_called_once_with(
                'status'
            )
            command.database_service.get_database_info.assert_called_once()

    def test_database_status_disconnected(self):
        """Test database status when disconnected."""
        command = DatabaseStatusCommand()

        mock_status = MigrationStatus(
            success=True,
            message='Database connection failed',
            connection='FAILED',
            current_migration='Unknown',
            alembic_configured=False,
            migrations_dir=False,
        )

        with patch.object(
            command.migration_service,
            'execute_operation',
            return_value=mock_status,
        ):
            result = command.execute()

            assert (
                result == 0
            )  # Status command shows info even if connection fails

    def test_database_status_exception(self):
        """Test database status with exception."""
        command = DatabaseStatusCommand()

        with patch.object(
            command.migration_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute()

            assert result == 1

    def test_database_status_prints_header(self):
        """Test that status command prints header."""
        command = DatabaseStatusCommand()

        mock_status = MigrationStatus(
            success=True,
            message='Status OK',
            connection='OK',
            current_migration='abc123',
            alembic_configured=True,
            migrations_dir=True,
        )

        with (
            patch.object(
                command.migration_service,
                'execute_operation',
                return_value=mock_status,
            ),
            patch.object(command, 'print_header') as mock_print_header,
        ):
            command.execute()

            mock_print_header.assert_called_once_with('Database Status', '📊')


class TestInitDatabaseCommand:
    """Integration tests for InitDatabaseCommand."""

    def test_database_init_success(self):
        """Test successful database initialization."""
        command = InitDatabaseCommand()

        mock_result = MigrationResult(
            success=True,
            message='Database initialized successfully',
            error=None,
            details='Created tables and applied initial migrations',
        )

        with patch.object(
            command.migration_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 0

            # Verify service was called correctly
            command.migration_service.execute_operation.assert_called_once_with(
                'init'
            )

    def test_database_init_failure(self):
        """Test failed database initialization."""
        command = InitDatabaseCommand()

        mock_result = MigrationResult(
            success=False,
            message='Database initialization failed',
            error='Connection refused',
            details=None,
        )

        with patch.object(
            command.migration_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 1

    def test_database_init_already_initialized(self):
        """Test database init when already initialized."""
        command = InitDatabaseCommand()

        mock_result = MigrationResult(
            success=True,
            message='Database already initialized',
            error=None,
            details='Current migration: abc123',
        )

        with patch.object(
            command.migration_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 0

    def test_database_init_exception(self):
        """Test database init with exception."""
        command = InitDatabaseCommand()

        with patch.object(
            command.migration_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute()

            assert result == 1

    def test_database_init_prints_header(self):
        """Test that init command prints header."""
        command = InitDatabaseCommand()

        mock_result = MigrationResult(
            success=True, message='Success', error=None, details=None
        )

        with (
            patch.object(
                command.migration_service,
                'execute_operation',
                return_value=mock_result,
            ),
            patch.object(command, 'print_header') as mock_print_header,
        ):
            command.execute()

            mock_print_header.assert_called_once_with(
                'Database Initialization', '🚀'
            )
