from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """Base settings that are not sensitive and can be version controlled."""

    # FastAPI settings
    API_DEBUG: bool = False
    API_VERSION: str = '1.0.0'
    API_PREFIX: str = '/api/v1'

    # Database settings
    DB_ECHO: bool = False
    POSTGRES_HOSTNAME: str = 'postgres'
    POSTGRES_PORT: str = '5432'
    POSTGRES_DB: str = 'foodtruck'

    # Redis settings
    REDIS_HOSTNAME: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_EXPIRE_IN_SECONDS: int = 3600

    # JWT settings
    JWT_SECRET_KEY: str = (
        '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    )
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Default admin user settings
    DEFAULT_ADMIN_EMAIL: str = 'admin@foodtruck.com'
    DEFAULT_ADMIN_NAME: str = 'Admin'
    DEFAULT_ADMIN_PASSWORD: str = 'admin123'  # Should be changed in production


class SensitiveSettings(BaseSettings):
    """Settings that contain sensitive data and should be in .env file."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    # Database credentials
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str


class Settings(BaseAppSettings, SensitiveSettings):
    """Combined settings class that inherits from both base and sensitive settings."""  # noqa: E501

    pass


def get_settings() -> Settings:
    """
    Returns the project settings.

    :return: Project settings.
    """
    return Settings()  # type: ignore
