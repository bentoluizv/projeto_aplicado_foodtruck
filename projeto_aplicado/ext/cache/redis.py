from redis import Redis

from projeto_aplicado.settings import get_settings

settings = get_settings()

redis = Redis(
    host=settings.REDIS_HOSTNAME,
    port=settings.REDIS_PORT,
    decode_responses=True,
)


def set(key: str, value: dict):
    """
    Set a value in Redis with an expiration time.
    """
    redis.hset(key, mapping=value)


def get(key: str):
    """
    Get a value from Redis.
    """
    return redis.hgetall(key)


def delete(key: str):
    """
    Delete a value from Redis.
    """
    redis.delete(key)
