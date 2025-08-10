"""Integration tests for setup commands."""

from unittest.mock import Mock, patch

import pytest

from projeto_aplicado.cli.commands.setup import (
    AutoInstallCommand,
    CheckSetupCommand,
    GenerateAliasCommand,
    SetupCommand,
    ShowPathCommand,
)
from projeto_aplicado.cli.schemas import (
    ShellAliasConfig,
    ShellInstallResult,
    ShellPathInfo,
    ShellSetupStatus,
)


class TestSetupCommand:
    """Integration tests for SetupCommand."""

    def test_setup_help(self):
        """Test setup command shows help."""
        command = SetupCommand()

        result = command.execute()

        assert result == 0


class TestShowPathCommand:
    """Integration tests for ShowPathCommand."""

    def test_show_path_success(self):
        """Test showing path configuration."""
        command = ShowPathCommand()

        mock_path_info = ShellPathInfo(
            project_root='/home/user/foodtruck',
            venv_path='/home/user/foodtruck/.venv',
            venv_bin_path='/home/user/foodtruck/.venv/bin',
            cli_path='/home/user/foodtruck/.venv/bin/foodtruck-cli',
            activation_script='/home/user/foodtruck/.venv/bin/activate',
            cli_exists=True,
            current_shell='bash',
            shell_config_file='/home/user/.bashrc',
            cli_in_path=True,
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_path_info,
        ) as mock_execute:
            result = command.execute()

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with('show_path')

    def test_show_path_cli_not_in_path(self):
        """Test showing path when CLI not in PATH."""
        command = ShowPathCommand()

        mock_path_info = ShellPathInfo(
            project_root='/home/user/foodtruck',
            venv_path='/home/user/foodtruck/.venv',
            venv_bin_path='/home/user/foodtruck/.venv/bin',
            cli_path='/home/user/foodtruck/.venv/bin/foodtruck-cli',
            activation_script='/home/user/foodtruck/.venv/bin/activate',
            cli_exists=True,
            current_shell='bash',
            shell_config_file='/home/user/.bashrc',
            cli_in_path=False,
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_path_info,
        ):
            result = command.execute()

            assert result == 0

    def test_show_path_exception(self):
        """Test show path with exception."""
        command = ShowPathCommand()

        with patch.object(
            command.shell_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute()

            assert result == 1

    def test_show_path_prints_header(self):
        """Test that show path prints header."""
        command = ShowPathCommand()

        mock_path_info = ShellPathInfo(
            project_root='/home/user/foodtruck',
            venv_path='/home/user/foodtruck/.venv',
            venv_bin_path='/home/user/foodtruck/.venv/bin',
            cli_path='/home/user/foodtruck/.venv/bin/foodtruck-cli',
            activation_script='/home/user/foodtruck/.venv/bin/activate',
            cli_exists=True,
            current_shell='bash',
            shell_config_file='/home/user/.bashrc',
            cli_in_path=True,
        )

        with (
            patch.object(
                command.shell_service,
                'execute_operation',
                return_value=mock_path_info,
            ),
            patch.object(command, 'print_header') as mock_print_header,
        ):
            command.execute()

            mock_print_header.assert_called_once_with(
                'PATH Configuration', '🛤️'
            )


class TestGenerateAliasCommand:
    """Integration tests for GenerateAliasCommand."""

    def test_generate_aliases_bash(self):
        """Test generating aliases for bash."""
        command = GenerateAliasCommand()

        mock_alias_config = ShellAliasConfig(
            shell='bash',
            config_file='/home/user/.bashrc',
            aliases={
                'ftcli': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app',
                'ft-health': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app health',
                'ft-admin': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app admin',
            },
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_alias_config,
        ) as mock_execute:
            result = command.execute(shell='bash')

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with(
                'generate_aliases', shell='bash'
            )

    def test_generate_aliases_auto_shell(self):
        """Test generating aliases with auto shell detection."""
        command = GenerateAliasCommand()

        mock_alias_config = ShellAliasConfig(
            shell='zsh',
            config_file='/home/user/.zshrc',
            aliases={
                'ftcli': 'cd /home/user/foodtruck && uv run python -m projeto_aplicado.cli.app',
            },
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_alias_config,
        ) as mock_execute:
            result = command.execute(shell='auto')

            assert result == 0

            mock_execute.assert_called_once_with(
                'generate_aliases', shell='auto'
            )

    def test_generate_aliases_exception(self):
        """Test generate aliases with exception."""
        command = GenerateAliasCommand()

        with patch.object(
            command.shell_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute(shell='bash')

            assert result == 1

    def test_generate_aliases_prints_header(self):
        """Test that generate alias prints header."""
        command = GenerateAliasCommand()

        mock_alias_config = ShellAliasConfig(
            shell='bash',
            config_file='/home/user/.bashrc',
            aliases={'ftcli': 'test'},
        )

        with (
            patch.object(
                command.shell_service,
                'execute_operation',
                return_value=mock_alias_config,
            ),
            patch.object(command, 'print_header') as mock_print_header,
        ):
            command.execute(shell='bash')

            mock_print_header.assert_called_once_with(
                'Shell Aliases', '🔗'
            )


class TestAutoInstallCommand:
    """Integration tests for AutoInstallCommand."""

    def test_auto_install_success(self):
        """Test successful auto installation."""
        command = AutoInstallCommand()

        mock_install_result = ShellInstallResult(
            success=True,
            shell='bash',
            config_file='/home/user/.bashrc',
            backup_file='/home/user/.bashrc.backup',
            backup_created=True,
            error=None,
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_install_result,
        ) as mock_execute:
            result = command.execute(shell='bash', force=False)

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with(
                'auto_install', shell='bash', force=False
            )

    def test_auto_install_failure(self):
        """Test failed auto installation."""
        command = AutoInstallCommand()

        mock_install_result = ShellInstallResult(
            success=False,
            shell=None,
            config_file=None,
            backup_file=None,
            backup_created=False,
            error='Permission denied: /home/user/.bashrc',
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_install_result,
        ):
            result = command.execute(shell='bash', force=False)

            assert result == 1

    def test_auto_install_with_force(self):
        """Test auto installation with force flag."""
        command = AutoInstallCommand()

        mock_install_result = ShellInstallResult(
            success=True,
            shell='zsh',
            config_file='/home/user/.zshrc',
            backup_file=None,
            backup_created=False,
            error=None,
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_install_result,
        ) as mock_execute:
            result = command.execute(shell='zsh', force=True)

            assert result == 0

            mock_execute.assert_called_once_with(
                'auto_install', shell='zsh', force=True
            )

    def test_auto_install_exception(self):
        """Test auto install with exception."""
        command = AutoInstallCommand()

        with patch.object(
            command.shell_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute(shell='bash', force=False)

            assert result == 1


class TestCheckSetupCommand:
    """Integration tests for CheckSetupCommand."""

    def test_check_setup_all_good(self):
        """Test check setup when everything is configured."""
        command = CheckSetupCommand()

        mock_setup_status = ShellSetupStatus(
            current_shell='bash',
            config_file='/home/user/.bashrc',
            cli_in_path=True,
            venv_active=True,
            aliases_found=['ftcli', 'ft-health', 'ft-admin'],
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_setup_status,
        ) as mock_execute:
            result = command.execute()

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with('check_setup')

    def test_check_setup_partial(self):
        """Test check setup with partial configuration."""
        command = CheckSetupCommand()

        mock_setup_status = ShellSetupStatus(
            current_shell='zsh',
            config_file='/home/user/.zshrc',
            cli_in_path=True,
            venv_active=False,
            aliases_found=[],
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_setup_status,
        ):
            result = command.execute()

            assert result == 0

    def test_check_setup_minimal(self):
        """Test check setup with minimal configuration."""
        command = CheckSetupCommand()

        mock_setup_status = ShellSetupStatus(
            current_shell='fish',
            config_file='/home/user/.config/fish/config.fish',
            cli_in_path=False,
            venv_active=False,
            aliases_found=[],
        )

        with patch.object(
            command.shell_service,
            'execute_operation',
            return_value=mock_setup_status,
        ):
            result = command.execute()

            assert result == 0

    def test_check_setup_exception(self):
        """Test check setup with exception."""
        command = CheckSetupCommand()

        with patch.object(
            command.shell_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute()

            assert result == 1

    def test_check_setup_prints_header(self):
        """Test that check setup prints header."""
        command = CheckSetupCommand()

        mock_setup_status = ShellSetupStatus(
            current_shell='bash',
            config_file='/home/user/.bashrc',
            cli_in_path=True,
            venv_active=True,
            aliases_found=[],
        )

        with (
            patch.object(
                command.shell_service,
                'execute_operation',
                return_value=mock_setup_status,
            ),
            patch.object(command, 'print_header') as mock_print_header,
        ):
            command.execute()

            mock_print_header.assert_called_once_with(
                'Shell Configuration Check', '🔍'
            )
