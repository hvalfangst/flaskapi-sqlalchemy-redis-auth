from configuration.models import RedisCacheConfig
import redis

from datetime import datetime, timedelta


class BlackListCache:
    def __init__(self, config: RedisCacheConfig):
        self.expiration = config.expiration
        self.redis_client = redis.StrictRedis(
            host=config.host,
            port=config.port,
            password=config.password,
            decode_responses=True
        )
        self.key_prefix = config.key_prefix

    def _get_key(self, email):
        return f"{self.key_prefix}:{email}"

    def set(self, email: str):
        key = self._get_key(email)
        self.redis_client.setex(key, timedelta(days=self.expiration).seconds, datetime.utcnow().second)

    def get(self, email: str):
        key = self._get_key(email)
        return self.redis_client.get(key)

    def list(self):
        keys = self.redis_client.keys(f"{self.key_prefix}:*")
        return {key[len(self.key_prefix) + 1:]: self.redis_client.get(key) for key in keys}

    def delete(self, email: str):
        key = self._get_key(email)
        self.redis_client.delete(key)
