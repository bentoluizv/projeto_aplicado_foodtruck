"""Integration tests for completions commands."""

from unittest.mock import Mock, patch

import pytest

from projeto_aplicado.cli.commands.completions import (
    CompletionsCommand,
    GenerateCompletionsCommand,
    InstallCompletionsCommand,
    StatusCompletionsCommand,
    UninstallCompletionsCommand,
)
from projeto_aplicado.cli.schemas import (
    CompletionGenerateResult,
    CompletionInstallResult,
    CompletionShellStatus,
    CompletionStatusResult,
    CompletionUninstallResult,
)


class TestCompletionsCommand:
    """Integration tests for CompletionsCommand."""

    def test_completions_help(self):
        """Test completions command shows help."""
        command = CompletionsCommand()

        result = command.execute()

        assert result == 0


class TestGenerateCompletionsCommand:
    """Integration tests for GenerateCompletionsCommand."""

    def test_generate_bash_to_stdout(self):
        """Test generating bash completion script to stdout."""
        command = GenerateCompletionsCommand()

        mock_result = CompletionGenerateResult(
            success=True,
            script='# bash completion script content',
            shell='bash',
            output_file=None,
            install_instructions=None,
            error=None,
        )

        with (
            patch.object(
                command.completions_service,
                'execute_operation',
                return_value=mock_result,
            ) as mock_execute,
            patch('builtins.print') as mock_print,
        ):
            result = command.execute(shell='bash', output=None)

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with(
                'generate', shell='bash', output=None
            )

            # Verify script was printed to stdout
            mock_print.assert_called_once_with(
                '# bash completion script content'
            )

    def test_generate_zsh_to_file(self):
        """Test generating zsh completion script to file."""
        command = GenerateCompletionsCommand()

        mock_result = CompletionGenerateResult(
            success=True,
            script='# zsh completion script content',
            shell='zsh',
            output_file='/tmp/completion.zsh',
            install_instructions=[
                '1. Copy to appropriate location:',
                '   cp /tmp/completion.zsh ~/.local/share/zsh/completions/',
                '2. Reload shell:',
                '   source ~/.zshrc',
            ],
            error=None,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ) as mock_execute:
            result = command.execute(shell='zsh', output='/tmp/completion.zsh')

            assert result == 0

            mock_execute.assert_called_once_with(
                'generate', shell='zsh', output='/tmp/completion.zsh'
            )

    def test_generate_unsupported_shell(self):
        """Test generating completion for unsupported shell."""
        command = GenerateCompletionsCommand()

        mock_result = CompletionGenerateResult(
            success=False,
            script=None,
            shell=None,
            output_file=None,
            install_instructions=None,
            error="Unsupported shell: powershell. Supported: ['bash', 'zsh', 'fish']",
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute(shell='powershell', output=None)

            assert result == 1

    def test_generate_exception(self):
        """Test generate completion with exception."""
        command = GenerateCompletionsCommand()

        with patch.object(
            command.completions_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute(shell='bash', output=None)

            assert result == 1


class TestInstallCompletionsCommand:
    """Integration tests for InstallCompletionsCommand."""

    def test_install_bash_success(self):
        """Test successful bash completion installation."""
        command = InstallCompletionsCommand()

        mock_result = CompletionInstallResult(
            success=True,
            shell='bash',
            install_path='/home/user/.local/share/bash-completion/completions/foodtruck-cli',
            backup_path=None,
            backup_created=False,
            reload_command='source ~/.bashrc',
            error=None,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ) as mock_execute:
            result = command.execute(shell='bash', force=False)

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with(
                'install', shell='bash', force=False
            )

    def test_install_already_exists(self):
        """Test installation when completions already exist."""
        command = InstallCompletionsCommand()

        mock_result = CompletionInstallResult(
            success=False,
            shell=None,
            install_path=None,
            backup_path=None,
            backup_created=False,
            reload_command=None,
            error='Completions already installed at /home/user/.local/share/bash-completion/completions/foodtruck-cli. Use --force to overwrite.',
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute(shell='bash', force=False)

            assert result == 1

    def test_install_with_force(self):
        """Test installation with force flag."""
        command = InstallCompletionsCommand()

        mock_result = CompletionInstallResult(
            success=True,
            shell='zsh',
            install_path='/home/user/.local/share/zsh/site-functions/_foodtruck-cli',
            backup_path='/home/user/.local/share/zsh/site-functions/_foodtruck-cli.backup',
            backup_created=True,
            reload_command='source ~/.zshrc',
            error=None,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ) as mock_execute:
            result = command.execute(shell='zsh', force=True)

            assert result == 0

            mock_execute.assert_called_once_with(
                'install', shell='zsh', force=True
            )

    def test_install_exception(self):
        """Test install completion with exception."""
        command = InstallCompletionsCommand()

        with patch.object(
            command.completions_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute(shell='bash', force=False)

            assert result == 1


class TestStatusCompletionsCommand:
    """Integration tests for StatusCompletionsCommand."""

    def test_status_completions_installed(self):
        """Test status when completions are installed."""
        command = StatusCompletionsCommand()

        mock_shells = {
            'bash': CompletionShellStatus(
                installed=True,
                path='/home/user/.local/share/bash-completion/completions/foodtruck-cli',
            ),
            'zsh': CompletionShellStatus(
                installed=True,
                path='/home/user/.local/share/zsh/site-functions/_foodtruck-cli',
            ),
            'fish': CompletionShellStatus(installed=False, path=None),
        }

        mock_result = CompletionStatusResult(
            current_shell='bash',
            completion_support='supported',
            can_test=True,
            shells=mock_shells,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ) as mock_execute:
            result = command.execute()

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with('status')

    def test_status_completions_not_installed(self):
        """Test status when no completions are installed."""
        command = StatusCompletionsCommand()

        mock_shells = {
            'bash': CompletionShellStatus(installed=False, path=None),
            'zsh': CompletionShellStatus(installed=False, path=None),
            'fish': CompletionShellStatus(installed=False, path=None),
        }

        mock_result = CompletionStatusResult(
            current_shell='bash',
            completion_support='supported',
            can_test=False,
            shells=mock_shells,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 0

    def test_status_unsupported_shell(self):
        """Test status with unsupported shell."""
        command = StatusCompletionsCommand()

        mock_shells = {
            'bash': CompletionShellStatus(installed=False, path=None),
            'zsh': CompletionShellStatus(installed=False, path=None),
            'fish': CompletionShellStatus(installed=False, path=None),
        }

        mock_result = CompletionStatusResult(
            current_shell='powershell',
            completion_support='not supported',
            can_test=False,
            shells=mock_shells,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute()

            assert result == 0

    def test_status_exception(self):
        """Test status completion with exception."""
        command = StatusCompletionsCommand()

        with patch.object(
            command.completions_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute()

            assert result == 1


class TestUninstallCompletionsCommand:
    """Integration tests for UninstallCompletionsCommand."""

    def test_uninstall_bash_success(self):
        """Test successful bash completion uninstallation."""
        command = UninstallCompletionsCommand()

        mock_result = CompletionUninstallResult(
            success=True,
            removed=['bash'],
            paths={
                'bash': '/home/user/.local/share/bash-completion/completions/foodtruck-cli'
            },
            error=None,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ) as mock_execute:
            result = command.execute(shell='bash')

            assert result == 0

            # Verify service was called correctly
            mock_execute.assert_called_once_with('uninstall', shell='bash')

    def test_uninstall_all_shells(self):
        """Test uninstalling completions for all shells."""
        command = UninstallCompletionsCommand()

        mock_result = CompletionUninstallResult(
            success=True,
            removed=['bash', 'zsh'],
            paths={
                'bash': '/home/user/.local/share/bash-completion/completions/foodtruck-cli',
                'zsh': '/home/user/.local/share/zsh/site-functions/_foodtruck-cli',
            },
            error=None,
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ) as mock_execute:
            result = command.execute(shell='all')

            assert result == 0

            mock_execute.assert_called_once_with('uninstall', shell='all')

    def test_uninstall_not_installed(self):
        """Test uninstalling when not installed."""
        command = UninstallCompletionsCommand()

        mock_result = CompletionUninstallResult(
            success=True, removed=[], paths={}, error=None
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute(shell='bash')

            assert result == 0

    def test_uninstall_unsupported_shell(self):
        """Test uninstalling for unsupported shell."""
        command = UninstallCompletionsCommand()

        mock_result = CompletionUninstallResult(
            success=False,
            removed=None,
            paths=None,
            error='Unsupported shell: powershell',
        )

        with patch.object(
            command.completions_service,
            'execute_operation',
            return_value=mock_result,
        ):
            result = command.execute(shell='powershell')

            assert result == 1

    def test_uninstall_exception(self):
        """Test uninstall completion with exception."""
        command = UninstallCompletionsCommand()

        with patch.object(
            command.completions_service,
            'execute_operation',
            side_effect=Exception('Service error'),
        ):
            result = command.execute(shell='bash')

            assert result == 1
