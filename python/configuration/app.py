from configuration.manager import *


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    ENVIRONMENT = ENVIRONMENT

    # Flask Config
    FLASK_APP = FLASK_APP
    FLASK_DEBUG = FLASK_DEBUG
    SECRET_KEY = SECRET_KEY

    # Database
    SQLALCHEMY_DATABASE_URI = db_config.database_url
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_ALGORITHM = jwt_config.algorithm
    JWT_EXPIRATION = jwt_config.expiration

    # Redis Config
    REDIS_HOST = redis_config.host
    REDIS_PORT = redis_config.port
    REDIS_PASSWORD = redis_config.password
    REDIS_KEY_PREFIX = redis_config.key_prefix
    REDIS_EXPIRATION = redis_config.expiration
