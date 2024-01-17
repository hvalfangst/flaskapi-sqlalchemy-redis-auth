from environs import Env
from .configs import DatabaseConfig, JwtConfig, RedisCacheConfig
from .cache import BlackListCache
from .configs import DatabaseConfig, JwtConfig, RedisCacheConfig

env = Env()
env.read_env()

# Database Configuration
database_url = env.str('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment.")
db_config = DatabaseConfig(database_url)

# JWT Configuration
encryption_key = env.str('SECRET_KEY')
algorithm = env.str('JWT_ALGORITHM', 'HS256')
expiration = env.int('JWT_EXPIRATION')
if not all([encryption_key, expiration]):
    raise ValueError("SECRET_KEY or JWT_EXPIRATION is missing in the environment.")
jwt_config = JwtConfig(encryption_key=encryption_key, algorithm=algorithm, expiration=expiration)

# Redis Configuration
redis_host = env.str('REDIS_HOST', 'localhost')
redis_port = env.int('REDIS_PORT', 6379)
redis_password = env.str('REDIS_PASSWORD', '')
redis_key_prefix = env.str('REDIS_KEY_PREFIX', 'users')
redis_expiration = env.int('REDIS_EXPIRATION', 1)
if not all([redis_host, redis_port, redis_key_prefix, redis_expiration]):
    raise ValueError("REDIS_HOST, REDIS_PORT, REDIS_KEY_PREFIX, or REDIS_EXPIRATION is missing in the environment.")

redis_config = RedisCacheConfig(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    key_prefix=redis_key_prefix,
    expiration=redis_expiration
)

# Redis Blacklist cache
blacklist_cache = BlackListCache(redis_config)
