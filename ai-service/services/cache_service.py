import hashlib
import logging
import os

import redis

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 900  # 15 minutes

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True,
)


def generate_cache_key(payload: str, namespace: str = "default") -> str:
    """
    Build a deterministic SHA256 cache key for an endpoint/payload pair.
    """
    normalized = f"{namespace}:{payload}"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def get_cached_response(payload: str, namespace: str = "default") -> str | None:
    """
    Return cached AI response when available, otherwise None.
    Redis failures are handled gracefully so the API can continue.
    """
    key = generate_cache_key(payload=payload, namespace=namespace)
    try:
        return redis_client.get(key)
    except redis.RedisError:
        logger.exception("Redis read failed for key=%s", key)
        return None


def set_cached_response(
    payload: str,
    response: str,
    namespace: str = "default",
) -> None:
    """
    Store AI response in Redis with a fixed 900-second TTL.
    Redis failures are non-fatal for request processing.
    """
    key = generate_cache_key(payload=payload, namespace=namespace)
    try:
        redis_client.setex(key, CACHE_TTL_SECONDS, response)
    except redis.RedisError:
        logger.exception("Redis write failed for key=%s", key)