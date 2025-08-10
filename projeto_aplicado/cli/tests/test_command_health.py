"""Integration tests for health command."""

from unittest.mock import Mock, patch

import pytest

from projeto_aplicado.cli.commands.health import HealthCommand
from projeto_aplicado.cli.schemas import HealthCheckDetail, HealthCheckResult


class TestHealthCommand:
    """Integration tests for HealthCommand."""

    def test_health_check_all_pass(self):
        """Test health check when all checks pass."""
        command = HealthCommand()

        # Mock successful health check details
        mock_details = [
            HealthCheckDetail(
                name='Database Connection',
                passed=True,
                message='Database connection OK',
            ),
            HealthCheckDetail(
                name='Admin Users', passed=True, message='Admin users found: 2'
            ),
            HealthCheckDetail(
                name='Configuration',
                passed=True,
                message='All settings configured',
            ),
        ]

        # Mock database info (as dict, as used in health command)
        mock_db_info = {
            'database': 'foodtruck',
            'host': 'localhost',
            'port': '5432',
        }

        mock_result = HealthCheckResult(
            passed=3,
            total=3,
            success=True,
            details=mock_details,
            database_info=mock_db_info,
        )

        with patch.object(
            command.health_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 0

            # Verify service was called
            command.health_service.execute_operation.assert_called_once()

    def test_health_check_some_fail(self):
        """Test health check when some checks fail."""
        command = HealthCommand()

        # Mock mixed health check results
        mock_details = [
            HealthCheckDetail(
                name='Database Connection',
                passed=False,
                message='Database connection failed',
            ),
            HealthCheckDetail(
                name='Admin Users',
                passed=True,
                message='Admin users found: 1',
            ),
            HealthCheckDetail(
                name='Configuration',
                passed=True,
                message='All settings configured',
            ),
        ]

        mock_db_info = {
            'database': 'foodtruck',
            'host': 'localhost',
            'port': '5432',
        }

        mock_result = HealthCheckResult(
            passed=2,
            total=3,
            success=False,
            details=mock_details,
            database_info=mock_db_info,
        )

        with patch.object(
            command.health_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 1

    def test_health_check_all_fail(self):
        """Test health check when all checks fail."""
        command = HealthCommand()

        # Mock all failed health checks
        mock_details = [
            HealthCheckDetail(
                name='Database Connection',
                passed=False,
                message='Database connection failed',
            ),
            HealthCheckDetail(
                name='Admin Users',
                passed=False,
                message='No admin users found',
            ),
            HealthCheckDetail(
                name='Configuration',
                passed=False,
                message='Missing configuration',
            ),
        ]

        mock_db_info = {
            'database': 'unknown',
            'host': 'localhost',
            'port': 'unknown',
        }

        mock_result = HealthCheckResult(
            passed=0,
            total=3,
            success=False,
            details=mock_details,
            database_info=mock_db_info,
        )

        with patch.object(
            command.health_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 1

    def test_health_check_with_exception(self):
        """Test health check handling unexpected exceptions."""
        command = HealthCommand()

        with patch.object(
            command.health_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            # Should raise exception since health command doesn't handle them
            with pytest.raises(Exception, match='Service error'):
                command.execute()

    def test_health_check_prints_header(self):
        """Test that health command prints header."""
        command = HealthCommand()

        mock_result = HealthCheckResult(
            passed=1,
            total=1,
            success=True,
            details=[],
            database_info={
                'database': 'test',
                'host': 'localhost',
                'port': '5432',
            },
        )

        with (
            patch.object(
                command.health_service,
                'execute_operation',
                return_value=mock_result,
            ),
            patch.object(command, 'print_header') as mock_print_header,
        ):
            command.execute()

            # Verify header was printed
            mock_print_header.assert_called_once_with(
                'System Health Check', '🏥'
            )
