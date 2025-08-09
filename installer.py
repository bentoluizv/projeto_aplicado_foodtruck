#!/usr/bin/env python3
"""
Development Environment Installer Script

This script automatically checks for and installs the following tools:
- uv (Python package manager)
- Python 3.13 (via uv)
- Docker
- Git

Supports Linux, macOS, and Windows platforms.
"""

import os
import platform
import shutil
import subprocess
import sys
from typing import Optional, Tuple


class Colors:
    """ANSI color codes for terminal output"""

    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def log_info(message: str) -> None:
    """Log informational message"""
    print(f'{Colors.BLUE}ℹ{Colors.END} {message}')


def log_success(message: str) -> None:
    """Log success message"""
    print(f'{Colors.GREEN}✓{Colors.END} {message}')


def log_warning(message: str) -> None:
    """Log warning message"""
    print(f'{Colors.YELLOW}⚠{Colors.END} {message}')


def log_error(message: str) -> None:
    """Log error message"""
    print(f'{Colors.RED}✗{Colors.END} {message}')


def run_command(
    command, capture_output: bool = True, check: bool = False
) -> Tuple[bool, str]:
    """
    Run a shell command and return success status and output

    Args:
        command: List of command parts or string for shell commands
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on failure

    Returns:
        Tuple of (success, output)
    """
    try:
        # Determine if we need shell=True for string commands
        use_shell = isinstance(command, str)

        if capture_output:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check,
                shell=use_shell,
            )
            return True, result.stdout.strip()

        else:
            result = subprocess.run(command, check=check, shell=use_shell)
            return True, ''

    except subprocess.CalledProcessError as e:
        if capture_output:
            return False, e.stderr.strip() if e.stderr else str(e)
        return False, str(e)

    except FileNotFoundError:
        cmd_str = command if isinstance(command, str) else ' '.join(command)
        return False, f'Command not found: {cmd_str}'


def is_command_available(command: str) -> bool:
    """Check if a command is available in PATH"""
    return shutil.which(command) is not None


def get_platform_info() -> Tuple[str, str]:
    """Get platform information"""
    system = platform.system().lower()
    arch = platform.machine().lower()

    # Normalize architecture names
    if arch in {'x86_64', 'amd64'}:
        arch = 'x86_64'

    elif arch in {'aarch64', 'arm64'}:
        arch = 'aarch64'

    return system, arch


class UvInstaller:
    """Handles uv installation"""

    @staticmethod
    def is_installed() -> bool:
        """Check if uv is installed"""
        return is_command_available('uv')

    @staticmethod
    def get_version() -> Optional[str]:
        """Get installed uv version"""
        if not UvInstaller.is_installed():
            return None

        success, output = run_command(['uv', '--version'])

        if success:
            # Output format: "uv 0.x.x"
            return output.split()[1] if len(output.split()) > 1 else output
        return None

    @staticmethod
    def install() -> bool:
        """Install uv using the official installer"""
        log_info('Installing uv...')

        system, _ = get_platform_info()

        try:
            if system == 'windows':
                # Use PowerShell on Windows
                command = [
                    'powershell',
                    '-c',
                    'irm https://astral.sh/uv/install.ps1 | iex',
                ]
            else:
                # Use curl on Unix-like systems
                command = 'curl -LsSf https://astral.sh/uv/install.sh | sh'

            success, output = run_command(command, capture_output=False)

            if success:
                log_success('uv installed successfully')
                return True
            else:
                log_error(f'Failed to install uv: {output}')
                return False

        except Exception as e:
            log_error(f'Error installing uv: {e}')
            return False


class PythonInstaller:
    """Handles Python 3.13 installation via uv"""

    @staticmethod
    def is_python_313_available() -> bool:
        """Check if Python 3.13 is available via uv or system"""
        # First check if uv can find Python 3.13 (only installed versions)
        if UvInstaller.is_installed():
            success, output = run_command([
                'uv',
                'python',
                'list',
                '--only-installed',
            ])
            if success and '3.13' in output:
                return True

        # Check system Python
        for python_cmd in ['python3.13', 'python3', 'python']:
            if is_command_available(python_cmd):
                success, output = run_command([python_cmd, '--version'])
                if success and 'Python 3.13' in output:
                    return True

        return False

    @staticmethod
    def install() -> bool:
        """Install Python 3.13 using uv"""
        if not UvInstaller.is_installed():
            log_error('uv is required to install Python 3.13')
            return False

        log_info('Installing Python 3.13 via uv...')

        success, output = run_command(['uv', 'python', 'install', '3.13'])
        if success:
            log_success('Python 3.13 installed successfully')
            return True
        else:
            log_error(f'Failed to install Python 3.13: {output}')
            return False


class DockerInstaller:
    """Handles Docker installation"""

    @staticmethod
    def is_installed() -> bool:
        """Check if Docker is installed"""
        return is_command_available('docker')

    @staticmethod
    def get_version() -> Optional[str]:
        """Get installed Docker version"""
        if not DockerInstaller.is_installed():
            return None

        success, output = run_command(['docker', '--version'])
        if success:
            # Output format: "Docker version 20.10.x, build ..."
            parts = output.split()
            return parts[2].rstrip(',') if len(parts) > 2 else output
        return None

    @staticmethod
    def install() -> bool:
        """Install Docker based on the platform"""
        system, _ = get_platform_info()

        log_info('Installing Docker...')

        if system == 'linux':
            return DockerInstaller._install_linux()
        elif system == 'darwin':
            return DockerInstaller._install_macos()
        elif system == 'windows':
            return DockerInstaller._install_windows()
        else:
            log_error(
                f'Unsupported platform for Docker installation: {system}'
            )
            return False

    @staticmethod
    def _install_linux() -> bool:
        """Install Docker on Linux"""
        try:
            # Update package index
            log_info('Updating package index...')
            success, _ = run_command(
                ['sudo', 'apt-get', 'update'], capture_output=False
            )
            if not success:
                log_error('Failed to update package index')
                return False

            # Install prerequisites
            log_info('Installing prerequisites...')
            prereqs = [
                'sudo',
                'apt-get',
                'install',
                '-y',
                'ca-certificates',
                'curl',
                'gnupg',
                'lsb-release',
            ]
            success, _ = run_command(prereqs, capture_output=False)
            if not success:
                log_error('Failed to install prerequisites')
                return False

            # Add Docker's official GPG key
            log_info('Adding Docker GPG key...')
            success, _ = run_command(
                'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg'
            )

            # Add Docker repository
            log_info('Adding Docker repository...')
            success, _ = run_command(
                'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
            )

            # Update and install Docker
            run_command(['sudo', 'apt-get', 'update'], capture_output=False)
            success, _ = run_command(
                [
                    'sudo',
                    'apt-get',
                    'install',
                    '-y',
                    'docker-ce',
                    'docker-ce-cli',
                    'containerd.io',
                    'docker-compose-plugin',
                ],
                capture_output=False,
            )

            if success:
                # Add user to docker group
                username = os.getenv('USER', 'user')
                run_command(['sudo', 'usermod', '-aG', 'docker', username])
                log_success('Docker installed successfully')
                log_warning(
                    'Please log out and back in for Docker group permissions to take effect'
                )
                return True
            else:
                log_error('Failed to install Docker')
                return False

        except Exception as e:
            log_error(f'Error installing Docker on Linux: {e}')
            return False

    @staticmethod
    def _install_macos() -> bool:
        """Install Docker on macOS"""
        log_warning('For macOS, please download Docker Desktop from:')
        log_warning('https://www.docker.com/products/docker-desktop')
        log_warning('Or install via Homebrew: brew install --cask docker')
        return False

    @staticmethod
    def _install_windows() -> bool:
        """Install Docker on Windows"""
        log_warning('For Windows, please download Docker Desktop from:')
        log_warning('https://www.docker.com/products/docker-desktop')
        return False


class GitInstaller:
    """Handles Git installation"""

    @staticmethod
    def is_installed() -> bool:
        """Check if Git is installed"""
        return is_command_available('git')

    @staticmethod
    def get_version() -> Optional[str]:
        """Get installed Git version"""
        if not GitInstaller.is_installed():
            return None

        success, output = run_command(['git', '--version'])
        if success:
            # Output format: "git version 2.x.x"
            parts = output.split()
            return parts[2] if len(parts) > 2 else output
        return None

    @staticmethod
    def install() -> bool:
        """Install Git based on the platform"""
        system, _ = get_platform_info()

        log_info('Installing Git...')

        if system == 'linux':
            return GitInstaller._install_linux()
        elif system == 'darwin':
            return GitInstaller._install_macos()
        elif system == 'windows':
            return GitInstaller._install_windows()
        else:
            log_error(f'Unsupported platform for Git installation: {system}')
            return False

    @staticmethod
    def _install_linux() -> bool:
        """Install Git on Linux"""
        try:
            success, _ = run_command(
                ['sudo', 'apt-get', 'update'], capture_output=False
            )
            if not success:
                log_error('Failed to update package index')
                return False

            success, _ = run_command(
                ['sudo', 'apt-get', 'install', '-y', 'git'],
                capture_output=False,
            )
            if success:
                log_success('Git installed successfully')
                return True
            else:
                log_error('Failed to install Git')
                return False
        except Exception as e:
            log_error(f'Error installing Git on Linux: {e}')
            return False

    @staticmethod
    def _install_macos() -> bool:
        """Install Git on macOS"""
        # Git usually comes with Xcode Command Line Tools
        log_info('Installing Xcode Command Line Tools (includes Git)...')
        success, _ = run_command(
            ['xcode-select', '--install'], capture_output=False
        )
        if success:
            log_success(
                'Git installed successfully via Xcode Command Line Tools'
            )
            return True
        else:
            log_warning(
                'If Xcode Command Line Tools are already installed, Git should be available'
            )
            log_warning(
                'Alternatively, install via Homebrew: brew install git'
            )
            return False

    @staticmethod
    def _install_windows() -> bool:
        """Install Git on Windows"""
        log_warning('For Windows, please download Git from:')
        log_warning('https://git-scm.com/download/windows')
        return False


def main():
    """Main installer function"""
    print(f'{Colors.BOLD}Development Environment Installer{Colors.END}')
    print('=' * 40)

    system, arch = get_platform_info()
    log_info(f'Detected platform: {system} ({arch})')
    print()

    # Track installation results
    results = {}

    # Check and install uv
    print(f'{Colors.BOLD}Checking uv...{Colors.END}')
    if UvInstaller.is_installed():
        version = UvInstaller.get_version()
        log_success(f'uv is already installed (version: {version})')
        results['uv'] = True
    else:
        log_warning('uv is not installed')
        if UvInstaller.install():
            results['uv'] = True
        else:
            results['uv'] = False
            log_error('Failed to install uv')
    print()

    # Check and install Python 3.13
    print(f'{Colors.BOLD}Checking Python 3.13...{Colors.END}')
    if PythonInstaller.is_python_313_available():
        log_success('Python 3.13 is available')
        results['python'] = True
    else:
        log_warning('Python 3.13 is not available')
        if results.get('uv', False):
            if PythonInstaller.install():
                results['python'] = True
            else:
                results['python'] = False
                log_error('Failed to install Python 3.13')
        else:
            log_error('Cannot install Python 3.13 without uv')
            results['python'] = False
    print()

    # Check and install Docker
    print(f'{Colors.BOLD}Checking Docker...{Colors.END}')
    if DockerInstaller.is_installed():
        version = DockerInstaller.get_version()
        log_success(f'Docker is already installed (version: {version})')
        results['docker'] = True
    else:
        log_warning('Docker is not installed')
        if DockerInstaller.install():
            results['docker'] = True
        else:
            results['docker'] = False
            log_error('Failed to install Docker')
    print()

    # Check and install Git
    print(f'{Colors.BOLD}Checking Git...{Colors.END}')
    if GitInstaller.is_installed():
        version = GitInstaller.get_version()
        log_success(f'Git is already installed (version: {version})')
        results['git'] = True
    else:
        log_warning('Git is not installed')
        if GitInstaller.install():
            results['git'] = True
        else:
            results['git'] = False
            log_error('Failed to install Git')
    print()

    # Summary
    print(f'{Colors.BOLD}Installation Summary{Colors.END}')
    print('=' * 20)

    all_success = True
    for tool, success in results.items():
        status = (
            f'{Colors.GREEN}✓{Colors.END}'
            if success
            else f'{Colors.RED}✗{Colors.END}'
        )
        print(f'{status} {tool}')
        if not success:
            all_success = False

    print()
    if all_success:
        log_success('All tools are installed and ready!')
    else:
        log_warning(
            'Some tools failed to install. Please check the output above.'
        )

    # Additional notes
    if system == 'linux' and results.get('docker', False):
        print()
        log_info('Note: If Docker was just installed, you may need to:')
        log_info('1. Log out and back in for group permissions')
        log_info('2. Or run: newgrp docker')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Colors.YELLOW}Installation interrupted by user{Colors.END}')
        sys.exit(1)
    except Exception as e:
        log_error(f'Unexpected error: {e}')
        sys.exit(1)
