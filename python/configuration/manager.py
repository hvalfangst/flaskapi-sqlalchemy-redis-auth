from os import path

from dotenv import load_dotenv
from environs import Env

from security.blacklist_cache import BlackListCache
from configuration.models import DatabaseConfig, JwtConfig, RedisCacheConfig

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

env = Env()
env.read_env()

# General Config
ENVIRONMENT = env.str('ENVIRONMENT')

# Flask Config
FLASK_APP = "main.py"
FLASK_DEBUG = env.str('FLASK_DEBUG')
SECRET_KEY = env.str('SECRET_KEY')

# Database Configuration
DATABASE_URL = env.str('SQLALCHEMY_DATABASE_URI')
if not DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URI is not set in the environment.")
db_config = DatabaseConfig(DATABASE_URL)

# JWT Configuration
ENCRYPTION_KEY = env.str('SECRET_KEY')
ALGORITHM = env.str('JWT_ALGORITHM', 'HS256')
EXPIRATION = env.int('JWT_EXPIRATION')
if not all([ENCRYPTION_KEY, EXPIRATION]):
    raise ValueError("SECRET_KEY or JWT_EXPIRATION is missing in the environment.")
jwt_config = JwtConfig(encryption_key=ENCRYPTION_KEY, algorithm=ALGORITHM, expiration=EXPIRATION)

# Redis Configuration
REDIS_HOST = env.str('REDIS_HOST', 'localhost')
REDIS_PORT = env.int('REDIS_PORT', 6379)
REDIS_PASSWORD = env.str('REDIS_PASSWORD', '')
REDIS_KEY_PREFIX = env.str('REDIS_KEY_PREFIX', 'users')
REDIS_EXPIRATION = env.int('REDIS_EXPIRATION', 1)
if not all([REDIS_HOST, REDIS_PORT, REDIS_KEY_PREFIX, REDIS_EXPIRATION]):
    raise ValueError("REDIS_HOST, REDIS_PORT, REDIS_KEY_PREFIX, or REDIS_EXPIRATION is missing in the environment.")

redis_config = RedisCacheConfig(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    key_prefix=REDIS_KEY_PREFIX,
    expiration=REDIS_EXPIRATION
)

# Redis Blacklist cache
blacklist_cache = BlackListCache(redis_config)