class JwtConfig:
    def __init__(self, encryption_key: str, algorithm: str, expiration: int):
        self.encryption_key = encryption_key
        self.algorithm = algorithm
        self.expiration = expiration
