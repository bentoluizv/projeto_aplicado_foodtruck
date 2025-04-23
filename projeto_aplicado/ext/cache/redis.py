import json

from redis import Redis
from sqlmodel import SQLModel

from projeto_aplicado.settings import get_settings

settings = get_settings()

redis = Redis(
    host=settings.REDIS_HOSTNAME,
    port=settings.REDIS_PORT,
    decode_responses=True,
)


def set(key: str, value: SQLModel):
    """
    Set a value in Redis with an expiration time.
    """
    redis.hset(key, mapping=value.model_dump())


def get(key: str):
    """
    Get a value from Redis.
    """
    value = redis.hgetall(key)
    sql_model = SQLModel.model_validate(value)

    return sql_model


def set_many(key: str, value: SQLModel):
    """
    Set multiple values in Redis with an expiration time.
    """
    redis.set(
        key, value.model_dump_json(), ex=settings.REDIS_EXPIRE_IN_SECONDS
    )


def get_many(key: str):
    """
    Get multiple values from Redis.
    """
    value = redis.get(key)

    if not value:
        return None

    if not isinstance(value, str):
        raise TypeError('Value must be a string')

    value = json.loads(value)

    if not isinstance(value, list):
        raise TypeError('Value must be a list')

    sql_model = [SQLModel.model_validate(item) for item in value]

    return sql_model


def delete(key: str):
    """
    Delete a value from Redis.
    """
    redis.delete(key)
