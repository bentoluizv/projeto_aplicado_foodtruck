"""Pydantic models for CLI operations."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from projeto_aplicado.resources.user.model import User


class MigrationResult(BaseModel):
    """Base model for migration operation results."""

    success: bool = Field(description='Whether the operation was successful')
    message: str = Field(description='Operation result message')
    error: Optional[str] = Field(
        None, description='Error message if operation failed'
    )
    details: Optional[str] = Field(
        None, description='Additional operation details'
    )


class MigrationStatus(BaseModel):
    """Model for database migration status."""

    success: bool = Field(description='Whether status check was successful')
    message: str = Field(description='Status message')
    connection: str = Field(
        description='Database connection status (OK/FAILED)'
    )
    current_migration: str = Field(description='Current migration revision')
    alembic_configured: bool = Field(
        description='Whether Alembic is configured'
    )
    migrations_dir: bool = Field(
        description='Whether migrations directory exists'
    )


class MigrationHistoryResult(MigrationResult):
    """Model for migration history results."""

    history: Optional[str] = Field(
        None, description='Migration history output'
    )


class CurrentMigrationResult(MigrationResult):
    """Model for current migration results."""

    current: Optional[str] = Field(
        None, description='Current migration revision'
    )


class HealthCheckDetail(BaseModel):
    """Model for individual health check results."""

    name: str = Field(description='Name of the health check')
    passed: bool = Field(description='Whether the check passed')
    message: str = Field(description='Check result message')


class HealthCheckResult(BaseModel):
    """Model for health check results."""

    passed: int = Field(description='Number of passed checks')
    total: int = Field(description='Total number of checks')
    success: bool = Field(description='Whether all checks passed')
    details: List[HealthCheckDetail] = Field(
        description='Individual check results'
    )
    database_info: dict = Field(description='Database connection information')


class DatabaseInfo(BaseModel):
    """Model for database information."""

    database: str = Field(description='Database name')
    host: str = Field(description='Database host')
    container: str = Field(description='Container name')
    port: str = Field(description='Database port')
    status: str = Field(description='Connection status')


class UserOperationResult(BaseModel):
    """Model for user operation results."""

    success: bool = Field(description='Whether the operation was successful')
    data: Optional[User] = Field(
        None, description='User data if operation successful'
    )
    error: Optional[str] = Field(
        None, description='Error message if operation failed'
    )


class UserListResult(BaseModel):
    """Model for user list operation results."""

    success: bool = Field(description='Whether the operation was successful')
    data: Optional[List[User]] = Field(
        None, description='List of users if operation successful'
    )
    error: Optional[str] = Field(
        None, description='Error message if operation failed'
    )


class ShellPathInfo(BaseModel):
    """Model for shell path information."""

    project_root: str = Field(description='Project root directory')
    venv_path: str = Field(description='Virtual environment path')
    venv_bin_path: str = Field(description='Virtual environment bin directory')
    cli_path: str = Field(description='CLI binary path')
    activation_script: str = Field(description='Shell activation script path')
    cli_exists: bool = Field(description='Whether CLI binary exists')
    current_shell: str = Field(description='Current shell type')
    shell_config_file: str = Field(description='Shell configuration file path')
    cli_in_path: bool = Field(description='Whether CLI is in PATH')


class ShellAliasConfig(BaseModel):
    """Model for shell alias configuration."""

    shell: str = Field(description='Shell type')
    config_file: str = Field(description='Configuration file path')
    aliases: Dict[str, str] = Field(description='Shell aliases')


class ShellInstallResult(BaseModel):
    """Model for shell installation results."""

    success: bool = Field(description='Whether installation was successful')
    shell: Optional[str] = Field(None, description='Shell type')
    config_file: Optional[str] = Field(
        None, description='Configuration file path'
    )
    backup_file: Optional[str] = Field(
        None, description='Backup file path if created'
    )
    backup_created: Optional[bool] = Field(
        None, description='Whether backup was created'
    )
    error: Optional[str] = Field(
        None, description='Error message if installation failed'
    )


class ShellSetupStatus(BaseModel):
    """Model for shell setup status."""

    current_shell: str = Field(description='Current shell type')
    config_file: str = Field(description='Configuration file path')
    cli_in_path: bool = Field(description='Whether CLI is in PATH')
    venv_active: bool = Field(
        description='Whether virtual environment is active'
    )
    aliases_found: List[str] = Field(description='Found CLI aliases')


class CompletionGenerateResult(BaseModel):
    """Model for completion script generation results."""

    success: bool = Field(description='Whether generation was successful')
    script: Optional[str] = Field(None, description='Generated script content')
    shell: Optional[str] = Field(None, description='Shell type')
    output_file: Optional[str] = Field(None, description='Output file path')
    install_instructions: Optional[List[str]] = Field(
        None, description='Installation instructions'
    )
    error: Optional[str] = Field(
        None, description='Error message if generation failed'
    )


class CompletionInstallResult(BaseModel):
    """Model for completion installation results."""

    success: bool = Field(description='Whether installation was successful')
    shell: Optional[str] = Field(None, description='Shell type')
    install_path: Optional[str] = Field(None, description='Installation path')
    backup_path: Optional[str] = Field(None, description='Backup file path')
    backup_created: Optional[bool] = Field(
        None, description='Whether backup was created'
    )
    reload_command: Optional[str] = Field(
        None, description='Command to reload shell'
    )
    error: Optional[str] = Field(
        None, description='Error message if installation failed'
    )


class CompletionShellStatus(BaseModel):
    """Model for individual shell completion status."""

    installed: bool = Field(description='Whether completions are installed')
    path: Optional[str] = Field(None, description='Installation path')


class CompletionStatusResult(BaseModel):
    """Model for completion status results."""

    current_shell: str = Field(description='Current shell type')
    completion_support: str = Field(description='Completion support status')
    can_test: bool = Field(description='Whether completions can be tested')
    shells: Dict[str, CompletionShellStatus] = Field(
        description='Status for each shell'
    )


class CompletionUninstallResult(BaseModel):
    """Model for completion uninstallation results."""

    success: bool = Field(description='Whether uninstallation was successful')
    removed: Optional[List[str]] = Field(
        None, description='List of removed shells'
    )
    paths: Optional[Dict[str, str]] = Field(
        None, description='Paths that were removed'
    )
    error: Optional[str] = Field(
        None, description='Error message if uninstallation failed'
    )
