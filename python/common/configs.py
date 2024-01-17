class JwtConfig:
    def __init__(self, encryption_key: str, algorithm: str, expiration: int):
        self.encryption_key = encryption_key
        self.algorithm = algorithm
        self.expiration = expiration


class DatabaseConfig:
    def __init__(self, database_url: str):
        self.database_url = database_url


class RedisCacheConfig:
    def __init__(self, host: str, port: int, password: str, key_prefix: str, expiration: int):
        self.host = host
        self.port = port
        self.password = password
        self.key_prefix = key_prefix
        self.expiry = expiration
