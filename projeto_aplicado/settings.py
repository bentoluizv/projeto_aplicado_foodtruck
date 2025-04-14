from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
    # Database
    DB_ECHO: bool
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str
    POSTGRES_PORT: str
    # Redis
    REDIS_HOSTNAME: str
    REDIS_PORT: int
    REDIS_EXPIRE_IN_SECONDS: int
    # Fastapi
    API_DEBUG: bool
    API_VERSION: str
    API_PREFIX: str
    # S3
    S3_ACCESS_KEY_ID: str
    S3_ACCESS_KEY_SECRET: str
    S3_ENDPOINT: str
    S3_REGION: str


def get_settings() -> Settings:
    """
    Retorna as configurações do projeto.

    :return: Configurações do projeto.
    """
    return Settings()  # type: ignore
