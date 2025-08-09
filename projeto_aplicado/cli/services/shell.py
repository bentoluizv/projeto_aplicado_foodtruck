"""Shell configuration service for foodtruck-cli setup."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict

from projeto_aplicado.cli.base.service import BaseService


class ShellService(BaseService):
    """Service for shell configuration and setup.

    Handles shell detection, PATH configuration, and alias generation
    for foodtruck-cli accessibility.
    """

    def __init__(self):
        """Initialize shell service."""
        super().__init__()

    def validate_input(self, **kwargs) -> bool:
        """Validate shell service inputs.

        Returns:
            bool: Always True as shell service has no specific validation
        """
        return True

    def execute_operation(self, operation: str, **kwargs) -> Any:
        """Execute shell operation.

        Args:
            operation: Type of operation
            **kwargs: Additional parameters for the operation

        Returns:
            Any: Result of the operation

        Raises:
            ValueError: For unknown operations
        """
        operations = {
            'show_path': self._show_path_info,
            'generate_aliases': self._generate_aliases,
            'auto_install': self._auto_install_shell,
            'check_setup': self._check_shell_setup,
        }

        if operation not in operations:
            raise ValueError(f'Unknown operation: {operation}')

        return operations[operation](**kwargs)

    def _get_current_shell(self) -> str:
        """Get current shell name.

        Returns:
            str: Shell name (bash, zsh, fish, etc.)
        """
        shell_env = os.environ.get('SHELL', '')
        if shell_env:
            return Path(shell_env).name
        return 'unknown'

    def _get_shell_config_file(self, shell: str = 'auto') -> Path:
        """Get shell configuration file path.

        Args:
            shell: Shell type or 'auto' for detection

        Returns:
            Path: Configuration file path
        """
        if shell == 'auto':
            shell = self._get_current_shell()

        home = Path.home()
        
        config_files = {
            'bash': home / '.bashrc',
            'zsh': home / '.zshrc',
            'fish': home / '.config' / 'fish' / 'config.fish',
        }

        # Fallback order for common shells
        if shell not in config_files:
            for fallback in ['bash', 'zsh']:
                config_file = config_files[fallback]
                if config_file.exists():
                    return config_file

        return config_files.get(shell, home / '.profile')

    def _get_project_paths(self) -> Dict[str, Any]:
        """Get project-related paths.

        Returns:
            Dict containing project paths
        """
        # Find project root by looking for pyproject.toml
        current = Path.cwd()
        project_root = None
        
        for path in [current] + list(current.parents):
            if (path / 'pyproject.toml').exists():
                project_root = path
                break
        
        if not project_root:
            project_root = current

        venv_path = project_root / '.venv'
        venv_bin = venv_path / 'bin'
        cli_path = venv_bin / 'foodtruck-cli'

        # Shell activation script
        activation_script = venv_bin / 'activate'

        return {
            'project_root': str(project_root),
            'venv_path': str(venv_path),
            'venv_bin_path': str(venv_bin),
            'cli_path': str(cli_path),
            'activation_script': str(activation_script),
            'cli_exists': cli_path.exists(),
        }

    def _show_path_info(self, **kwargs) -> Dict[str, Any]:
        """Show PATH configuration information.

        Returns:
            Dict containing PATH information
        """
        paths = self._get_project_paths()
        current_shell = self._get_current_shell()
        config_file = self._get_shell_config_file()

        # Check if CLI is in PATH
        cli_in_path = shutil.which('foodtruck-cli') is not None

        return {
            **paths,
            'current_shell': current_shell,
            'shell_config_file': str(config_file),
            'cli_in_path': cli_in_path,
        }

    def _generate_aliases(self, shell: str = 'auto', **kwargs) -> Dict[str, Any]:
        """Generate shell aliases.

        Args:
            shell: Shell type

        Returns:
            Dict containing aliases and configuration
        """
        if shell == 'auto':
            shell = self._get_current_shell()

        paths = self._get_project_paths()
        project_root = paths['project_root']
        config_file = self._get_shell_config_file(shell)

        # Generate uv run based aliases (simpler approach)
        base_cmd = f'cd {project_root} && uv run python -m projeto_aplicado.cli.app'
        aliases = {
            'ftcli': base_cmd,
            'ft-health': f'{base_cmd} health',
            'ft-admin': f'{base_cmd} admin',
            'ft-db': f'{base_cmd} database',
            'ft-setup': f'{base_cmd} setup',
            'ft-completions': f'{base_cmd} completions',
        }

        return {
            'shell': shell,
            'config_file': str(config_file),
            'aliases': aliases,
        }

    def _auto_install_shell(
        self, shell: str = 'auto', force: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """Auto-install shell configuration.

        Args:
            shell: Shell type
            force: Force overwrite existing configuration

        Returns:
            Dict containing installation result
        """
        if shell == 'auto':
            shell = self._get_current_shell()

        paths = self._get_project_paths()
        config_file = self._get_shell_config_file(shell)

        # With uv run approach, we don't need to check for CLI binary existence
        # Just check if we're in a valid project directory
        if not paths['project_root'] or not Path(paths['project_root']).exists():
            return {
                'success': False,
                'error': f'Project root not found at {paths["project_root"]}',
            }

        # Create backup if file exists
        backup_file = None
        if config_file.exists() and not force:
            backup_file = config_file.with_suffix(f'{config_file.suffix}.backup')
            try:
                shutil.copy2(config_file, backup_file)
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to create backup: {str(e)}',
                }

        # Generate aliases using uv run approach
        aliases_result = self._generate_aliases(shell)
        aliases = aliases_result['aliases']
        
        config_lines = [
            '\n# Food Truck CLI aliases (auto-generated)',
        ]
        
        for alias_name, alias_command in aliases.items():
            config_lines.append(f'alias {alias_name}="{alias_command}"')
        
        config_lines.append('# End Food Truck CLI aliases\n')

        try:
            # Append to config file
            with open(config_file, 'a') as f:
                f.write('\n'.join(config_lines))

            return {
                'success': True,
                'shell': shell,
                'config_file': str(config_file),
                'backup_file': str(backup_file) if backup_file else None,
                'backup_created': backup_file is not None,
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to write configuration: {str(e)}',
            }

    def _check_shell_setup(self, **kwargs) -> Dict[str, Any]:
        """Check current shell setup.

        Returns:
            Dict containing setup status
        """
        current_shell = self._get_current_shell()
        config_file = self._get_shell_config_file()
        
        # Check if CLI is accessible
        cli_in_path = shutil.which('foodtruck-cli') is not None
        
        # Check if virtual environment is active
        venv_active = os.environ.get('VIRTUAL_ENV') is not None

        # Look for existing aliases
        aliases_found = []
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                    
                # Look for food truck related aliases
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('alias ft') or 'foodtruck-cli' in line:
                        aliases_found.append(line)
            except Exception:
                pass

        return {
            'current_shell': current_shell,
            'config_file': str(config_file),
            'cli_in_path': cli_in_path,
            'venv_active': venv_active,
            'aliases_found': aliases_found,
        }
