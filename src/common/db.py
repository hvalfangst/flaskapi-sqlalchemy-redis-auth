from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from configuration.manager import DatabaseConfig


class Database:
    def __init__(self, config: DatabaseConfig) -> None:
        self.engine = create_engine(config.database_url)


db = SQLAlchemy()
