"""Completions service for generating shell completion scripts."""

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from projeto_aplicado.cli.base.service import BaseService


class CompletionsService(BaseService):
    """Service for generating and managing shell completions.

    Handles generation, installation, and management of shell completion
    scripts for bash, zsh, and fish shells.
    """

    def __init__(self):
        """Initialize completions service."""
        super().__init__()

    def validate_input(self, **kwargs) -> bool:
        """Validate completions service inputs.

        Returns:
            bool: Always True as completions service has no specific validation
        """
        return True

    def execute_operation(self, operation: str, **kwargs) -> Any:
        """Execute completions operation.

        Args:
            operation: Type of operation
            **kwargs: Additional parameters for the operation

        Returns:
            Any: Result of the operation

        Raises:
            ValueError: For unknown operations
        """
        operations = {
            'generate': self._generate_completion_script,
            'install': self._install_completions,
            'status': self._check_completions_status,
            'uninstall': self._uninstall_completions,
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

    def _get_completion_script_bash(self) -> str:
        """Generate bash completion script.

        Returns:
            str: Bash completion script content
        """
        return '''#!/bin/bash

# foodtruck-cli bash completion script
# Generated automatically - do not edit manually

_foodtruck_cli_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Main commands
    if [[ ${COMP_CWORD} == 1 ]]; then
        opts="health admin database setup completions version --help --version"
        COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
        return 0
    fi

    # Subcommands based on main command
    case "${COMP_WORDS[1]}" in
        health)
            if [[ ${COMP_CWORD} == 2 ]]; then
                opts="--help"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            fi
            ;;
        admin)
            if [[ ${COMP_CWORD} == 2 ]]; then
                opts="create check list-admins --help"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            fi
            ;;
        database)
            if [[ ${COMP_CWORD} == 2 ]]; then
                opts="init status upgrade downgrade current history create --help"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            fi
            ;;
        setup)
            if [[ ${COMP_CWORD} == 2 ]]; then
                opts="path alias install check --help"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            elif [[ ${COMP_CWORD} == 3 && "${COMP_WORDS[2]}" == "alias" ]]; then
                opts="bash zsh fish auto"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            elif [[ ${COMP_CWORD} == 3 && "${COMP_WORDS[2]}" == "install" ]]; then
                opts="bash zsh fish auto --force"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            fi
            ;;
        completions)
            if [[ ${COMP_CWORD} == 2 ]]; then
                opts="generate install status uninstall --help"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            elif [[ ${COMP_CWORD} == 3 && ("${COMP_WORDS[2]}" == "generate" || "${COMP_WORDS[2]}" == "install") ]]; then
                opts="bash zsh fish auto"
                COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            fi
            ;;
    esac

    # Handle flags
    case "${prev}" in
        --shell)
            opts="bash zsh fish auto"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        --output)
            COMPREPLY=($(compgen -f -- ${cur}))
            ;;
    esac
}

complete -F _foodtruck_cli_completion foodtruck-cli
'''

    def _get_completion_script_zsh(self) -> str:
        """Generate zsh completion script.

        Returns:
            str: Zsh completion script content
        """
        return '''#compdef foodtruck-cli

# foodtruck-cli zsh completion script
# Generated automatically - do not edit manually

_foodtruck_cli() {
    local context state line
    typeset -A opt_args

    _arguments -C \\
        '1: :_foodtruck_cli_commands' \\
        '*::arg:->args' \\
        '--help[Show help]' \\
        '--version[Show version]'

    case $state in
        args)
            case ${words[1]} in
                health)
                    _arguments '--help[Show help]'
                    ;;
                admin)
                    _arguments \\
                        '1: :(create check list-admins)' \\
                        '--help[Show help]'
                    ;;
                database)
                    _arguments \\
                        '1: :(init status upgrade downgrade current history create)' \\
                        '--help[Show help]'
                    ;;
                setup)
                    _arguments \\
                        '1: :(path alias install check)' \\
                        '--help[Show help]'
                    case ${words[2]} in
                        alias|install)
                            _arguments \\
                                '2: :(bash zsh fish auto)' \\
                                '--force[Force overwrite]'
                            ;;
                    esac
                    ;;
                completions)
                    _arguments \\
                        '1: :(generate install status uninstall)' \\
                        '--help[Show help]'
                    case ${words[2]} in
                        generate|install)
                            _arguments \\
                                '2: :(bash zsh fish auto)' \\
                                '--output[Output file]:file:_files' \\
                                '--force[Force overwrite]'
                            ;;
                        uninstall)
                            _arguments \\
                                '2: :(bash zsh fish auto all)'
                            ;;
                    esac
                    ;;
            esac
            ;;
    esac
}

_foodtruck_cli_commands() {
    local commands=(
        'health:Check system health status'
        'admin:Admin user management commands'
        'database:Database management commands'
        'setup:Shell setup and configuration'
        'completions:Shell completion management'
        'version:Show version information'
    )
    _describe 'commands' commands
}

_foodtruck_cli "$@"
'''

    def _get_completion_script_fish(self) -> str:
        """Generate fish completion script.

        Returns:
            str: Fish completion script content
        """
        return '''# foodtruck-cli fish completion script
# Generated automatically - do not edit manually

# Main commands
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -a "health" -d "Check system health status"
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -a "admin" -d "Admin user management commands"
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -a "database" -d "Database management commands"
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -a "setup" -d "Shell setup and configuration"
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -a "completions" -d "Shell completion management"
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -a "version" -d "Show version information"
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -l "help" -d "Show help"
complete -c foodtruck-cli -f -n "__fish_use_subcommand" -l "version" -d "Show version"

# Admin subcommands
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from admin" -a "create" -d "Create admin user"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from admin" -a "check" -d "Check if admin exists"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from admin" -a "list-admins" -d "List all admin users"

# Database subcommands
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from database" -a "init" -d "Initialize database"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from database" -a "status" -d "Show database status"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from database" -a "upgrade" -d "Upgrade database"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from database" -a "downgrade" -d "Downgrade database"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from database" -a "current" -d "Show current migration"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from database" -a "history" -d "Show migration history"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from database" -a "create" -d "Create new migration"

# Setup subcommands
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from setup" -a "path" -d "Show PATH configuration"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from setup" -a "alias" -d "Generate shell aliases"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from setup" -a "install" -d "Auto-configure shell"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from setup" -a "check" -d "Check shell configuration"

# Setup shell options
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from setup; and __fish_seen_subcommand_from alias install" -a "bash zsh fish auto"

# Completions subcommands
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from completions" -a "generate" -d "Generate completion script"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from completions" -a "install" -d "Install completions"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from completions" -a "status" -d "Check completion status"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from completions" -a "uninstall" -d "Uninstall completions"

# Completions shell options
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from completions; and __fish_seen_subcommand_from generate install" -a "bash zsh fish auto"
complete -c foodtruck-cli -f -n "__fish_seen_subcommand_from completions; and __fish_seen_subcommand_from uninstall" -a "bash zsh fish auto all"

# Common options
complete -c foodtruck-cli -f -l "help" -d "Show help"
complete -c foodtruck-cli -f -l "force" -d "Force overwrite"
'''

    def _get_shell_completion_paths(self, shell: str) -> Dict[str, str]:
        """Get completion installation paths for shell.

        Args:
            shell: Shell name

        Returns:
            Dict containing installation paths
        """
        home = Path.home()
        
        paths = {
            'bash': {
                'user': home / '.bash_completion',
                'system': Path('/etc/bash_completion.d/foodtruck-cli'),
                'reload': 'source ~/.bashrc',
            },
            'zsh': {
                'user': home / '.zsh' / 'completion' / '_foodtruck-cli',
                'system': Path('/usr/local/share/zsh/site-functions/_foodtruck-cli'),
                'reload': 'source ~/.zshrc',
            },
            'fish': {
                'user': home / '.config' / 'fish' / 'completions' / 'foodtruck-cli.fish',
                'system': Path('/usr/share/fish/completions/foodtruck-cli.fish'),
                'reload': 'source ~/.config/fish/config.fish',
            },
        }
        
        return paths.get(shell, {})

    def _generate_completion_script(
        self, shell: str = 'bash', output: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """Generate completion script for shell.

        Args:
            shell: Shell type
            output: Output file path

        Returns:
            Dict containing generation result
        """
        generators = {
            'bash': self._get_completion_script_bash,
            'zsh': self._get_completion_script_zsh,
            'fish': self._get_completion_script_fish,
        }

        if shell not in generators:
            return {
                'success': False,
                'error': f'Unsupported shell: {shell}. Supported: {list(generators.keys())}',
            }

        script = generators[shell]()
        
        if output:
            try:
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(script)
                
                # Make executable
                os.chmod(output_path, 0o755)
                
                # Generate installation instructions
                paths = self._get_shell_completion_paths(shell)
                instructions = [
                    f'1. Copy to appropriate location:',
                    f'   cp {output} {paths.get("user", "~/.completion/")}',
                    f'2. Reload shell:',
                    f'   {paths.get("reload", "source ~/.bashrc")}',
                ]
                
                return {
                    'success': True,
                    'script': script,
                    'output_path': str(output_path),
                    'shell': shell,
                    'install_instructions': instructions,
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to write output file: {str(e)}',
                }
        else:
            return {
                'success': True,
                'script': script,
                'shell': shell,
            }

    def _install_completions(
        self, shell: str = 'auto', force: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """Install completion script.

        Args:
            shell: Shell type
            force: Force reinstall

        Returns:
            Dict containing installation result
        """
        if shell == 'auto':
            shell = self._get_current_shell()

        if shell not in ['bash', 'zsh', 'fish']:
            return {
                'success': False,
                'error': f'Unsupported shell: {shell}',
            }

        paths = self._get_shell_completion_paths(shell)
        if not paths:
            return {
                'success': False,
                'error': f'No completion paths configured for {shell}',
            }

        # Try user path first, fallback to system if needed
        install_path = paths['user']
        install_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if already installed
        if install_path.exists() and not force:
            return {
                'success': False,
                'error': f'Completions already installed at {install_path}. Use --force to overwrite.',
            }

        # Create backup if exists
        backup_path = None
        if install_path.exists():
            backup_path = install_path.with_suffix(f'{install_path.suffix}.backup')
            shutil.copy2(install_path, backup_path)

        try:
            # Generate and install script
            result = self._generate_completion_script(shell)
            if not result['success']:
                return result

            install_path.write_text(result['script'])
            os.chmod(install_path, 0o644)

            # Special handling for zsh - update fpath if needed
            if shell == 'zsh':
                self._setup_zsh_fpath(install_path.parent)

            return {
                'success': True,
                'shell': shell,
                'install_path': str(install_path),
                'backup_path': str(backup_path) if backup_path else None,
                'backup_created': backup_path is not None,
                'reload_command': paths['reload'],
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to install completions: {str(e)}',
            }

    def _setup_zsh_fpath(self, completion_dir: Path) -> None:
        """Setup zsh fpath for completion directory.

        Args:
            completion_dir: Directory containing completions
        """
        zshrc = Path.home() / '.zshrc'
        fpath_line = f'fpath=({completion_dir} $fpath)'
        compinit_line = 'autoload -U compinit && compinit'

        if zshrc.exists():
            content = zshrc.read_text()
            
            # Add fpath if not present
            if str(completion_dir) not in content:
                with open(zshrc, 'a') as f:
                    f.write(f'\n# foodtruck-cli completions\n')
                    f.write(f'{fpath_line}\n')
                    
            # Add compinit if not present
            if 'compinit' not in content:
                with open(zshrc, 'a') as f:
                    f.write(f'{compinit_line}\n')

    def _check_completions_status(self, **kwargs) -> Dict[str, Any]:
        """Check completion installation status.

        Returns:
            Dict containing status information
        """
        current_shell = self._get_current_shell()
        shells_status = {}

        for shell in ['bash', 'zsh', 'fish']:
            paths = self._get_shell_completion_paths(shell)
            if not paths:
                continue

            user_path = paths['user']
            system_path = paths.get('system')
            
            installed = user_path.exists()
            install_path = None
            
            if installed:
                install_path = str(user_path)
            elif system_path and system_path.exists():
                installed = True
                install_path = str(system_path)

            shells_status[shell] = {
                'installed': installed,
                'path': install_path,
            }

        return {
            'current_shell': current_shell,
            'completion_support': current_shell in ['bash', 'zsh', 'fish'],
            'shells': shells_status,
            'can_test': current_shell in shells_status and shells_status[current_shell]['installed'],
        }

    def _uninstall_completions(
        self, shell: str = 'auto', **kwargs
    ) -> Dict[str, Any]:
        """Uninstall completion scripts.

        Args:
            shell: Shell type or 'all'

        Returns:
            Dict containing uninstall result
        """
        if shell == 'auto':
            shell = self._get_current_shell()

        shells_to_remove = []
        if shell == 'all':
            shells_to_remove = ['bash', 'zsh', 'fish']
        elif shell in ['bash', 'zsh', 'fish']:
            shells_to_remove = [shell]
        else:
            return {
                'success': False,
                'error': f'Unsupported shell: {shell}',
            }

        removed = []
        paths = {}

        for shell_name in shells_to_remove:
            shell_paths = self._get_shell_completion_paths(shell_name)
            if not shell_paths:
                continue

            user_path = shell_paths['user']
            if user_path.exists():
                try:
                    user_path.unlink()
                    removed.append(shell_name)
                    paths[shell_name] = str(user_path)
                except Exception:
                    pass

        return {
            'success': True,
            'removed': removed,
            'paths': paths,
        }
