from .models import CreateUserRequest, UpdateUserRequest, User
from common.configs import DatabaseConfig
from .queries import (
    CREATE_USER_QUERY,
    UPDATE_USER_QUERY,
    LIST_USERS_QUERY,
    GET_USER_BY_EMAIL_QUERY,
    DELETE_USER_BY_EMAIL_QUERY
)
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class UsersRepository:
    def __init__(self, config: DatabaseConfig) -> None:
        self.engine = create_engine(config.database_url)

    def create(self, request: CreateUserRequest):
        with Session(bind=self.engine) as db:
            db.execute(
                CREATE_USER_QUERY,
                {
                    "first_name": request.first_name,
                    "last_name": request.last_name,
                    "phone_number": request.phone_number,
                    "address": request.address,
                    "email": request.email,
                    "password": request.password,
                    "ssn": request.ssn,
                    "access": request.access.to_string()
                }
            )
            db.commit()

    def update(self, email: str, request: UpdateUserRequest):
        with Session(bind=self.engine) as db:
            db.execute(
                UPDATE_USER_QUERY,
                {
                    "phone_number": request.phone_number,
                    "address": request.address,
                    "email": email
                }
            )
            db.commit()

    def list(self) -> List[User]:
        with Session(bind=self.engine) as db:
            result = db.execute(LIST_USERS_QUERY)
            rows = result.fetchall()
        users = [User(*row) for row in rows]
        return users

    def get_by_email(self, email: str):
        with Session(bind=self.engine) as db:
            result = db.execute(GET_USER_BY_EMAIL_QUERY, {"email": email})
            row = result.fetchone()

            if row is None:
                return None

            return User(*row)

    def delete_by_email(self, email: str):
        with Session(bind=self.engine) as db:
            db.execute(DELETE_USER_BY_EMAIL_QUERY, {"email": email})
            db.commit()
