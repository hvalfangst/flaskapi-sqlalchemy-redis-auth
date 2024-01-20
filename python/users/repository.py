from typing import List

from sqlalchemy.orm import sessionmaker

from .models import CreateUserRequest, UpdateUserRequest, User
from .queries import (
    CREATE_USER_QUERY,
    UPDATE_USER_QUERY,
    LIST_USERS_QUERY,
    GET_USER_BY_EMAIL_QUERY,
    DELETE_USER_BY_EMAIL_QUERY
)


class UsersRepository:
    def __init__(self, database) -> None:
        self.database = database
        print(f"Initialized UsersRepository with database: {self.database}")

    def create(self, request: CreateUserRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                session.execute(
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
                session.commit()
        except Exception as e:
            print(f"Error occurred during create: {e}")
            raise e

    def update(self, email: str, request: UpdateUserRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                session.execute(
                    UPDATE_USER_QUERY,
                    {
                        "phone_number": request.phone_number,
                        "address": request.address,
                        "email": email
                    }
                )
                session.commit()
        except Exception as e:
            print(f"Error occurred during update: {e}")
            raise e

    def list(self) -> List[User]:
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                print(f"Initialized UsersRepository with session: {session}")
                result = session.execute(LIST_USERS_QUERY)
                rows = result.fetchall()
                users = [User(*row) for row in rows]
                return users
        except Exception as e:
            print(f"Error occurred during list: {e}")
            raise e

    def get_by_email(self, email: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                result = session.execute(GET_USER_BY_EMAIL_QUERY, {"email": email})
                row = result.fetchone()

                if row is None:
                    return None

                return User(*row)
        except Exception as e:
            print(f"Error occurred during get_by_email: {e}")
            raise e

    def delete_by_email(self, email: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                session.execute(DELETE_USER_BY_EMAIL_QUERY, {"email": email})
                session.commit()
        except Exception as e:
            print(f"Error occurred during delete_by_email: {e}")
            raise e
