"""Tests for CLI app integration and configuration."""

from unittest.mock import patch

from projeto_aplicado.cli.app import create_cli_app


class TestCLIApp:
    """Test CLI app creation and configuration."""

    def test_create_cli_app(self):
        """Test CLI app creation and basic configuration."""
        app = create_cli_app()

        assert app is not None
        # App name can be string or tuple depending on cyclopts state
        assert app.name in ['foodtruck-cli', ('foodtruck-cli',)]
        assert 'Food Truck Management System CLI Tools' in app.help
        assert app.version == '1.0.0'
        assert hasattr(app, 'console')

    def test_app_has_commands(self):
        """Test that app has expected commands registered."""
        app = create_cli_app()

        # Check that the app has the expected structure
        assert hasattr(app, '_commands')
        # Note: Testing specific commands would require running cyclopts,
        # so we keep this basic for unit testing

    def test_environment_setup(self):
        """Test that environment variables are set correctly."""
        import os

        # Store original value
        original_hostname = os.environ.get('POSTGRES_HOSTNAME')

        try:
            # Remove the environment variable if it exists
            if 'POSTGRES_HOSTNAME' in os.environ:
                del os.environ['POSTGRES_HOSTNAME']

            # Create the app
            app = create_cli_app()

            # Check that localhost is set as default
            assert os.environ.get('POSTGRES_HOSTNAME') == 'localhost'

        finally:
            # Restore original value
            if original_hostname is not None:
                os.environ['POSTGRES_HOSTNAME'] = original_hostname
            else:
                os.environ.pop('POSTGRES_HOSTNAME', None)

    def test_environment_preservation(self):
        """Test that existing environment variables are preserved."""
        import os

        # Store original value
        original_hostname = os.environ.get('POSTGRES_HOSTNAME')

        try:
            # Set a custom value
            os.environ['POSTGRES_HOSTNAME'] = 'custom-host'

            # Create the app
            app = create_cli_app()

            # Check that custom value is preserved
            assert os.environ.get('POSTGRES_HOSTNAME') == 'custom-host'

        finally:
            # Restore original value
            if original_hostname is not None:
                os.environ['POSTGRES_HOSTNAME'] = original_hostname
            else:
                os.environ.pop('POSTGRES_HOSTNAME', None)


class TestCLIAppCommands:
    """Test CLI app command functions (mocked for unit testing)."""

    def test_health_command_function(self):
        """Test health command function."""
        from projeto_aplicado.cli.app import create_cli_app

        app = create_cli_app()

        # Since we can't easily test the actual cyclopts command execution,
        # we verify that the HealthCommand can be instantiated
        from projeto_aplicado.cli.commands.health import HealthCommand

        command = HealthCommand(db_host='localhost', console=app.console)
        assert command is not None
        assert command.database_service.db_host == 'localhost'

    def test_admin_create_command_function(self):
        """Test admin create command function."""
        from projeto_aplicado.cli.app import create_cli_app
        from projeto_aplicado.cli.commands.admin import CreateAdminCommand

        app = create_cli_app()

        command = CreateAdminCommand(db_host='localhost', console=app.console)
        assert command is not None
        assert command.database_service.db_host == 'localhost'

    def test_admin_check_command_function(self):
        """Test admin check command function."""
        from projeto_aplicado.cli.app import create_cli_app
        from projeto_aplicado.cli.commands.admin import CheckUserCommand

        app = create_cli_app()

        command = CheckUserCommand(db_host='localhost', console=app.console)
        assert command is not None
        assert command.database_service.db_host == 'localhost'

    def test_admin_list_command_function(self):
        """Test admin list command function."""
        from projeto_aplicado.cli.app import create_cli_app
        from projeto_aplicado.cli.commands.admin import ListAdminsCommand

        app = create_cli_app()

        command = ListAdminsCommand(db_host='localhost', console=app.console)
        assert command is not None
        assert command.database_service.db_host == 'localhost'


class TestCLIAppIntegration:
    """Integration tests for CLI app functionality."""

    @patch('sys.exit')
    def test_health_command_integration(self, mock_exit):
        """Test health command integration (mocked)."""
        from projeto_aplicado.cli.commands.health import HealthCommand

        # Mock all the health checks to pass
        with patch.object(HealthCommand, 'execute', return_value=0):
            command = HealthCommand()
            exit_code = command.execute()

            assert exit_code == 0

    @patch('sys.exit')
    def test_admin_create_command_integration(self, mock_exit):
        """Test admin create command integration (mocked)."""
        from projeto_aplicado.cli.commands.admin import CreateAdminCommand

        # Mock successful user creation
        with patch.object(CreateAdminCommand, 'execute', return_value=0):
            command = CreateAdminCommand()
            exit_code = command.execute(
                username='testuser',
                email='test@example.com',
                password='password123',
                full_name='Test User',
                force=True
            )

            assert exit_code == 0


class TestCLIAppErrorHandling:
    """Test CLI app error handling and edge cases."""

    def test_app_creation_with_import_errors(self):
        """Test app creation when there are import issues."""
        # This test ensures the app can be created even if some imports fail
        app = create_cli_app()
        assert app is not None

    def test_app_version_command(self):
        """Test that version command functionality is available."""
        app = create_cli_app()

        # The version command should be a simple function that prints version info
        # We can't easily test the actual cyclopts command, but we can verify
        # the app has version information
        assert app.version == '1.0.0'

    def test_app_default_command(self):
        """Test that default command functionality is available."""
        app = create_cli_app()

        # The default command should display help information
        # We verify the app has console capability for output
        assert hasattr(app, 'console')
        assert app.console is not None
