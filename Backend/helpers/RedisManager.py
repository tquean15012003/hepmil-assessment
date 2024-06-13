import os
import redis
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(self) -> None:
        logger.info("RedisManager initialized")
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            decode_responses=True,
        )

    def get(self, key: str) -> str | None:
        return self.redis_client.get(key)

    def set(self, key: str, value: str, expiry_time: int = 3600) -> None:
        self.redis_client.set(name=key, value=value, ex=expiry_time)


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, force=True)
    redis_manager = RedisManager()
    KEY = "hello"
    VALUE = "world"
    redis_manager.set(KEY, VALUE)
    retrieved_value = redis_manager.get(KEY)
    logger.info(f"Retrieved value: {retrieved_value}")
    if retrieved_value == VALUE:
        logger.info("Redis is working properly!")
    else:
        logger.error("Something went wrong in Redis Server")
