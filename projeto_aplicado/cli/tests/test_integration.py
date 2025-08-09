"""Integration tests for CLI clean architecture."""

from unittest.mock import Mock, patch

import pytest

from projeto_aplicado.cli.commands.admin import (
    CreateAdminCommand,
    ListAdminsCommand,
)
from projeto_aplicado.cli.commands.health import HealthCommand
from projeto_aplicado.cli.services.database import DatabaseService
from projeto_aplicado.cli.services.health import HealthService
from projeto_aplicado.cli.services.user import UserService
from projeto_aplicado.resources.user.model import UserRole


class TestCLIWorkflow:
    """Test complete CLI workflows end-to-end."""

    def test_admin_creation_workflow(self, session):
        """Test complete admin creation workflow."""
        # Step 1: Create database service
        db_service = DatabaseService()

        # Step 2: Create user service with dependency injection
        user_service = UserService(db_service)

        # Step 3: Mock database operations to use test session
        with patch.object(db_service, 'execute_operation') as mock_execute:
            mock_execute.side_effect = lambda func, **kwargs: func(session, **kwargs)

            # Step 4: Create admin command
            command = CreateAdminCommand()
            command.database_service = db_service
            command.user_service = user_service

            # Step 5: Execute admin creation
            exit_code = command.execute(
                username='workflow_admin',
                email='workflow@example.com',
                password='password123',
                full_name='Workflow Admin',
                force=True
            )

            # Step 6: Verify success
            assert exit_code == 0

            # Step 7: Verify user was created in database
            from sqlmodel import select

            from projeto_aplicado.resources.user.model import User
            user = session.exec(select(User).where(User.email == 'workflow@example.com')).first()
            assert user is not None
            assert user.username == 'workflow_admin'
            assert user.role == UserRole.ADMIN

    def test_health_check_workflow(self):
        """Test complete health check workflow."""
        # Step 1: Create all services with dependency injection
        db_service = DatabaseService()
        user_service = UserService(db_service)
        health_service = HealthService(db_service, user_service)

        # Step 2: Create health command
        command = HealthCommand()
        command.database_service = db_service
        command.user_service = user_service
        command.health_service = health_service

        # Step 3: Mock all dependencies for successful health check
        with patch.object(db_service, 'test_connection', return_value=True), \
             patch.object(user_service, 'execute_operation', return_value=2), \
             patch.object(db_service, 'get_database_info', return_value={
                 'database': 'test_db',
                 'host': 'localhost',
                 'port': '5432',
                 'status': 'connected'
             }):

            # Step 4: Execute health check
            exit_code = command.execute()

            # Step 5: Verify success
            assert exit_code == 0

    def test_list_admins_workflow(self, session):
        """Test complete list admins workflow."""
        # Step 1: Create services
        db_service = DatabaseService()
        user_service = UserService(db_service)

        # Step 2: Create some test admin users first
        with patch.object(db_service, 'execute_operation') as mock_execute:
            mock_execute.side_effect = lambda func, **kwargs: func(session, **kwargs)

            # Create first admin
            user_service.execute_operation(
                'create',
                username='admin1',
                email='admin1@example.com',
                password='password123',
                full_name='Admin One'
            )

            # Create second admin
            user_service.execute_operation(
                'create',
                username='admin2',
                email='admin2@example.com',
                password='password123',
                full_name='Admin Two'
            )

            # Step 3: Create list command
            command = ListAdminsCommand()
            command.database_service = db_service
            command.user_service = user_service

            # Step 4: Execute list command
            exit_code = command.execute()

            # Step 5: Verify success
            assert exit_code == 0


class TestServiceIntegration:
    """Test service integration following dependency injection."""

    def test_database_service_integration(self):
        """Test DatabaseService integration with real-like scenarios."""
        service = DatabaseService(db_host='localhost')

        # Test validation
        assert service.validate_input() is True

        # Test environment management (mocked)
        with patch('projeto_aplicado.cli.services.database.Session'), \
             patch('importlib.reload'):

            # Test operation execution pattern
            def mock_operation(session, **kwargs):
                return f"Operation executed with {kwargs}"

            with patch.object(service, 'get_session') as mock_get_session:
                mock_session = Mock()
                mock_get_session.return_value.__enter__.return_value = mock_session
                mock_get_session.return_value.__exit__.return_value = None

                result = service.execute_operation(mock_operation, test_param='test_value')
                assert 'test_value' in result

    def test_user_service_integration(self):
        """Test UserService integration with DatabaseService."""
        # Create database service
        db_service = DatabaseService()

        # Create user service with dependency injection
        user_service = UserService(db_service)

        # Test validation
        assert user_service.validate_input(
            username='test',
            email='test@example.com',
            password='password123',
            full_name='Test User'
        ) is True

        # Test operation delegation
        with patch.object(db_service, 'execute_operation') as mock_execute:
            mock_execute.return_value = Mock()

            result = user_service.execute_operation('create', test_param='test_value')

            # Verify that database service was called
            mock_execute.assert_called_once()
            assert result is not None

    def test_health_service_integration(self):
        """Test HealthService integration with multiple dependencies."""
        # Create all dependencies
        db_service = DatabaseService()
        user_service = UserService(db_service)
        health_service = HealthService(db_service, user_service)

        # Test validation
        assert health_service.validate_input() is True

        # Test with mocked dependencies
        with patch.object(db_service, 'test_connection', return_value=True), \
             patch.object(user_service, 'execute_operation', return_value=1), \
             patch.object(db_service, 'get_database_info', return_value={}):

            result = health_service.execute_operation()

            assert result['passed'] == 3
            assert result['total'] == 3
            assert result['success'] is True


class TestErrorHandlingIntegration:
    """Test error handling across the CLI architecture."""

    def test_database_service_error_handling(self):
        """Test DatabaseService error handling."""
        service = DatabaseService()

        # Test connection failure
        with patch('projeto_aplicado.cli.services.database.Session', side_effect=Exception("Connection failed")):
            result = service.test_connection()
            assert result is False

    def test_user_service_error_handling(self):
        """Test UserService error handling."""
        db_service = Mock()
        db_service.execute_operation.side_effect = Exception("Database error")

        user_service = UserService(db_service)

        # Test that exceptions are propagated appropriately
        with pytest.raises(Exception):
            user_service.execute_operation('create', username='test')

    def test_command_error_handling(self):
        """Test command-level error handling."""
        command = CreateAdminCommand()

        # Mock service to raise exception
        with patch.object(command.user_service, 'validate_input', return_value=True), \
             patch.object(command.user_service, 'execute_operation', side_effect=Exception("Service error")):

            exit_code = command.execute(
                username='test',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=True
            )

            # Should return error exit code
            assert exit_code == 1

    def test_health_service_partial_failure_handling(self):
        """Test HealthService handling of partial failures."""
        db_service = Mock()
        user_service = Mock()
        health_service = HealthService(db_service, user_service)

        # Mock mixed results
        db_service.test_connection.return_value = True  # Success
        user_service.execute_operation.side_effect = Exception("User service error")  # Failure
        db_service.get_database_info.return_value = {}  # Success

        result = health_service.execute_operation()

        # Should handle partial failures gracefully
        assert result['passed'] == 2  # DB and settings pass, admin users fail
        assert result['total'] == 3
        assert result['success'] is False

        # Check that exception was caught and handled
        details = {detail[0]: (detail[1], detail[2]) for detail in result['details']}
        assert details['Admin Users'][0] is False
        assert 'FAILED' in details['Admin Users'][1]


class TestDependencyInjection:
    """Test dependency injection patterns in the CLI architecture."""

    def test_service_dependency_injection(self):
        """Test that services correctly use dependency injection."""
        # Create dependencies
        db_service = DatabaseService()
        user_service = UserService(db_service)
        health_service = HealthService(db_service, user_service)

        # Verify dependency injection
        assert user_service.database_service is db_service
        assert health_service.database_service is db_service
        assert health_service.user_service is user_service

    def test_command_dependency_injection(self):
        """Test that commands correctly create and inject dependencies."""
        command = HealthCommand(db_host='test-host')

        # Verify that dependencies are created and configured
        assert command.database_service.db_host == 'test-host'
        assert command.user_service.database_service is command.database_service
        assert command.health_service.database_service is command.database_service
        assert command.health_service.user_service is command.user_service

    def test_dependency_isolation(self):
        """Test that different command instances have isolated dependencies."""
        command1 = HealthCommand(db_host='host1')
        command2 = HealthCommand(db_host='host2')

        # Verify isolation
        assert command1.database_service is not command2.database_service
        assert command1.database_service.db_host == 'host1'
        assert command2.database_service.db_host == 'host2'
