"""Installer service for development environment setup following clean architecture."""

import os
import platform
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Tuple

from projeto_aplicado.cli.base.service import BaseService


class InstallerService(BaseService):
    """Service for installing and setting up development environment.

    Implements development environment setup following SOLID principles:
    - Single Responsibility: Only handles installation and setup
    - Open/Closed: Easy to extend with new installation steps
    - Dependency Inversion: Depends on abstractions, not concretions
    """

    def __init__(self):
        """Initialize installer service."""
        super().__init__()
        self.system = platform.system().lower()

    def validate_input(self, **kwargs) -> bool:
        """Validate installer service inputs.

        Returns:
            bool: Always True as installer has no specific validation
        """
        return True

    def execute_operation(self, operation: str, **kwargs) -> Any:
        """Execute installer operation.

        Args:
            operation: Type of operation ('check', 'install', 'setup', etc.)
            **kwargs: Additional parameters for the operation

        Returns:
            Any: Result of the operation

        Raises:
            ValueError: For unknown operations
        """
        if operation == 'check':
            return self._check_dependencies()
        elif operation == 'install':
            return self._install_dependencies(**kwargs)
        elif operation == 'setup':
            return self._setup_project(**kwargs)
        elif operation == 'status':
            return self._get_system_status()
        else:
            raise ValueError(f'Unknown operation: {operation}')

    def _run_command(
        self, command: List[str], shell: bool = False
    ) -> Tuple[int, str, str]:
        """Run a system command and return result.

        Args:
            command: Command as list of strings
            shell: Whether to run in shell mode

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        try:
            if shell and self.system == 'windows':
                result = subprocess.run(
                    ' '.join(command),
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False,
                )
            else:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    shell=shell,
                    check=False,
                )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, '', str(e)

    def _check_tool_installed(
        self, tool: str, version_command: List[str]
    ) -> Dict[str, Any]:
        """Check if a tool is installed and get its version.

        Args:
            tool: Name of the tool
            version_command: Command to check version

        Returns:
            Dict with installation status and version info
        """
        # First check if tool is in PATH
        if not shutil.which(tool):
            return {
                'installed': False,
                'tool': tool,
                'error': f'{tool} not found in PATH',
            }

        # Check version
        return_code, stdout, stderr = self._run_command(version_command)

        if return_code == 0:
            version = stdout.strip() or stderr.strip()
            return {
                'installed': True,
                'tool': tool,
                'version': version,
                'command_output': version,
            }
        else:
            return {
                'installed': False,
                'tool': tool,
                'error': f'Failed to get {tool} version: {stderr or stdout}',
            }

    def _check_dependencies(self) -> Dict[str, Any]:
        """Check if all required dependencies are installed.

        Returns:
            Dict containing status of all dependencies
        """
        dependencies = {
            'python': ['python', '--version'],
            'uv': ['uv', '--version'],
            'git': ['git', '--version'],
            'docker': ['docker', '--version'],
        }

        results = {}
        all_installed = True

        for tool, version_cmd in dependencies.items():
            result = self._check_tool_installed(tool, version_cmd)
            results[tool] = result
            if not result['installed']:
                all_installed = False

        # Check for Docker Compose separately
        docker_compose_result = self._check_tool_installed(
            'docker-compose', ['docker-compose', '--version']
        )
        if not docker_compose_result['installed']:
            # Try docker compose (newer syntax)
            docker_compose_result = self._check_tool_installed(
                'docker', ['docker', 'compose', 'version']
            )
            docker_compose_result['tool'] = 'docker-compose'

        results['docker-compose'] = docker_compose_result
        if not docker_compose_result['installed']:
            all_installed = False

        return {
            'success': True,
            'all_installed': all_installed,
            'dependencies': results,
            'system': self.system,
            'message': 'All dependencies installed'
            if all_installed
            else 'Missing dependencies',
        }

    def _install_uv(self) -> Dict[str, Any]:
        """Install uv package manager.

        Returns:
            Dict containing installation result
        """
        if self.system == 'windows':
            command = [
                'powershell',
                '-c',
                'irm https://astral.sh/uv/install.ps1 | iex',
            ]
        else:
            command = [
                'curl',
                '-LsSf',
                'https://astral.sh/uv/install.sh',
                '|',
                'sh',
            ]

        return_code, stdout, stderr = self._run_command(command, shell=True)

        if return_code == 0:
            return {
                'success': True,
                'tool': 'uv',
                'message': 'uv installed successfully',
                'details': stdout.strip()
                if stdout.strip()
                else 'Installation completed',
            }
        else:
            return {
                'success': False,
                'tool': 'uv',
                'message': 'Failed to install uv',
                'error': stderr.strip() or stdout.strip(),
            }

    def _install_python(self, version: str = '3.13') -> Dict[str, Any]:
        """Install Python using uv.

        Args:
            version: Python version to install

        Returns:
            Dict containing installation result
        """
        # Check if uv is available
        if not shutil.which('uv'):
            return {
                'success': False,
                'tool': 'python',
                'message': 'uv is required to install Python',
                'error': 'Install uv first before installing Python',
            }

        return_code, stdout, stderr = self._run_command([
            'uv',
            'python',
            'install',
            version,
        ])

        if return_code == 0:
            return {
                'success': True,
                'tool': 'python',
                'message': f'Python {version} installed successfully',
                'details': stdout.strip()
                if stdout.strip()
                else f'Python {version} installed',
            }
        else:
            return {
                'success': False,
                'tool': 'python',
                'message': f'Failed to install Python {version}',
                'error': stderr.strip() or stdout.strip(),
            }

    def _install_dependencies(
        self, auto: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """Install missing dependencies.

        Args:
            auto: Whether to install automatically without prompts

        Returns:
            Dict containing installation results
        """
        check_result = self._check_dependencies()
        dependencies = check_result['dependencies']

        installation_results = {}
        all_success = True

        # Install uv if missing
        if not dependencies['uv']['installed']:
            if auto:
                result = self._install_uv()
                installation_results['uv'] = result
                if not result['success']:
                    all_success = False
            else:
                installation_results['uv'] = {
                    'success': False,
                    'tool': 'uv',
                    'message': 'uv installation skipped (use --auto to install)',
                    'error': 'Manual confirmation required',
                }
                all_success = False

        # Install Python if missing (requires uv)
        if (
            not dependencies['python']['installed']
            and dependencies['uv']['installed']
        ):
            if auto:
                result = self._install_python()
                installation_results['python'] = result
                if not result['success']:
                    all_success = False
            else:
                installation_results['python'] = {
                    'success': False,
                    'tool': 'python',
                    'message': 'Python installation skipped (use --auto to install)',
                    'error': 'Manual confirmation required',
                }
                all_success = False

        # For Git and Docker, provide installation instructions
        missing_tools = []
        for tool in ['git', 'docker', 'docker-compose']:
            if not dependencies[tool]['installed']:
                missing_tools.append(tool)

        if missing_tools:
            installation_results['manual_install_required'] = {
                'success': False,
                'tools': missing_tools,
                'message': f'Manual installation required for: {", ".join(missing_tools)}',
                'instructions': self._get_installation_instructions(
                    missing_tools
                ),
            }
            all_success = False

        return {
            'success': all_success,
            'message': 'All installations completed'
            if all_success
            else 'Some installations failed or require manual setup',
            'results': installation_results,
            'manual_steps_required': len(missing_tools) > 0,
        }

    def _get_installation_instructions(
        self, tools: List[str]
    ) -> Dict[str, str]:
        """Get installation instructions for missing tools.

        Args:
            tools: List of missing tools

        Returns:
            Dict with installation instructions per tool
        """
        instructions = {}

        for tool in tools:
            if tool == 'git':
                if self.system == 'windows':
                    instructions[tool] = (
                        'Download from https://git-scm.com/download/win'
                    )
                elif self.system == 'darwin':
                    instructions[tool] = (
                        'Install via Homebrew: brew install git'
                    )
                else:
                    instructions[tool] = (
                        'Install via package manager: sudo apt-get install git (Ubuntu/Debian) or sudo yum install git (RHEL/CentOS)'
                    )

            elif tool == 'docker':
                if self.system == 'windows':
                    instructions[tool] = (
                        'Download Docker Desktop from https://www.docker.com/products/docker-desktop'
                    )
                elif self.system == 'darwin':
                    instructions[tool] = (
                        'Download Docker Desktop from https://www.docker.com/products/docker-desktop'
                    )
                else:
                    instructions[tool] = (
                        'Follow instructions at https://docs.docker.com/engine/install/'
                    )

            elif tool == 'docker-compose':
                instructions[tool] = (
                    'Usually included with Docker Desktop. For Linux, see: https://docs.docker.com/compose/install/'
                )

        return instructions

    def _setup_project(self, **kwargs) -> Dict[str, Any]:
        """Set up the project environment.

        Returns:
            Dict containing setup result
        """
        setup_steps = []
        all_success = True

        # Check if we're in the right directory
        if not os.path.exists('pyproject.toml'):
            return {
                'success': False,
                'message': 'Not in project root directory',
                'error': 'pyproject.toml not found. Run this command from the project root.',
            }

        # Create virtual environment
        return_code, stdout, stderr = self._run_command(['uv', 'venv'])
        if return_code == 0:
            setup_steps.append({
                'step': 'create_venv',
                'success': True,
                'message': 'Virtual environment created',
            })
        else:
            setup_steps.append({
                'step': 'create_venv',
                'success': False,
                'message': 'Failed to create virtual environment',
                'error': stderr.strip() or stdout.strip(),
            })
            all_success = False

        # Install dependencies
        return_code, stdout, stderr = self._run_command([
            'uv',
            'pip',
            'install',
            '-e',
            '.[dev]',
        ])
        if return_code == 0:
            setup_steps.append({
                'step': 'install_deps',
                'success': True,
                'message': 'Dependencies installed',
            })
        else:
            setup_steps.append({
                'step': 'install_deps',
                'success': False,
                'message': 'Failed to install dependencies',
                'error': stderr.strip() or stdout.strip(),
            })
            all_success = False

        return {
            'success': all_success,
            'message': 'Project setup completed'
            if all_success
            else 'Project setup failed',
            'steps': setup_steps,
        }

    def _get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status.

        Returns:
            Dict containing system status information
        """
        dependencies = self._check_dependencies()

        # Check project status
        project_status = {
            'in_project_dir': os.path.exists('pyproject.toml'),
            'venv_exists': os.path.exists('.venv'),
            'dependencies_installed': False,
        }

        # Check if dependencies are installed by trying to import
        try:
            import fastapi
            import sqlmodel

            project_status['dependencies_installed'] = True
        except ImportError:
            pass

        return {
            'success': True,
            'message': 'System status retrieved',
            'system': {
                'platform': platform.platform(),
                'python_version': sys.version,
                'architecture': platform.architecture()[0],
            },
            'dependencies': dependencies['dependencies'],
            'project': project_status,
            'ready_for_development': (
                dependencies['all_installed']
                and project_status['in_project_dir']
                and project_status['venv_exists']
                and project_status['dependencies_installed']
            ),
        }
