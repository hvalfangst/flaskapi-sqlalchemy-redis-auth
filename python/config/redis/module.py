class RedisCacheConfig:
    def __init__(self, host: str, port: int, password: str, key_prefix: str):
        self.host = host
        self.port = port
        self.password = password
        self.key_prefix = key_prefix
