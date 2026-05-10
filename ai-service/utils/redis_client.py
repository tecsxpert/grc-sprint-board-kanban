import os

from utils.logging_config import get_logger

try:
    import redis
except ImportError:
    redis = None

logger = get_logger(__name__)


def create_redis_client():
    if redis is None:
        logger.warning("redis_package_missing")
        return None
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    try:
        client = redis.Redis(host=host, port=port, socket_connect_timeout=1, decode_responses=True)
        client.ping()
        return client
    except redis.RedisError as exc:
        logger.warning("redis_unavailable", error=str(exc), host=host, port=port)
        return None
