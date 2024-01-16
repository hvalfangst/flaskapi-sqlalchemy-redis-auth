from typing import Any, Dict
import json

import bcrypt
import redis
from python.config.redis.module import RedisCacheConfig
from python.util.module import UserPayload


class RedisUserRepository:
    def __init__(self, config: RedisCacheConfig) -> None:
        self.redis_client = redis.StrictRedis(host=config.host, port=config.port,
                                              password=config.password, decode_responses=True)
        self.key_prefix = config.key_prefix

    def create(self, key: str, user: UserPayload) -> None:
        full_key = f"{self.key_prefix}:{key}"
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        hashed_user = UserPayload(user.email, hashed_password.decode('utf-8'), user.access)
        serialized_data = json.dumps(hashed_user.to_dict())
        self.redis_client.set(full_key, serialized_data)

    def get(self, key: str) -> Dict[str, Any]:
        full_key = f"{self.key_prefix}:{key}"
        data = self.redis_client.get(full_key)
        if data:
            return json.loads(data)
        else:
            raise KeyError(f"Key '{full_key}' not found in Redis.")

    def list(self) -> Dict[str, Any]:
        keys = self.redis_client.keys(f"{self.key_prefix}:*")
        result = {}
        for full_key in keys:
            key = full_key[len(self.key_prefix) + 1:]
            result[key] = self.get(key)
        return result

    def delete(self, key: str) -> None:
        full_key = f"{self.key_prefix}:{key}"
        self.redis_client.delete(full_key)

    def email_exists(self, email: str) -> bool:
        keys = self.redis_client.keys(f"{self.key_prefix}:*")
        for full_key in keys:
            user_data = self.get(full_key[len(self.key_prefix) + 1:])
            if user_data and user_data.get("email") == email:
                return True
        return False
