from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .models import CreateUserRequest, UpdateUserRequest, User


class UsersRepository:
    def __init__(self, database) -> None:
        self.database = database
        print(f"Initialized UsersRepository with database: {self.database}")

    def create(self, request: CreateUserRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                user = User(
                    first_name=request.first_name,
                    last_name=request.last_name,
                    phone_number=request.phone_number,
                    address=request.address,
                    email=request.email,
                    password=request.password,
                    ssn=request.ssn,
                    access=request.access.to_string()
                )
                session.add(user)
                session.commit()
        except SQLAlchemyError as e:
            print(f"Error occurred during create: {e}")
            raise e

    def update(self, email: str, request: UpdateUserRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                user = session.query(User).filter_by(email=email).first()

                if user:
                    user.phone_number = request.phone_number
                    user.address = request.address
                    session.commit()
                else:
                    print(f"User with email {email} not found.")
        except SQLAlchemyError as e:
            print(f"Error occurred during update: {e}")
            raise e

    def list(self) -> list[Type[User]]:
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                users = session.query(User).all()
                return users
        except SQLAlchemyError as e:
            print(f"Error occurred during list: {e}")
            raise e

    def get_by_email(self, email: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                user = session.query(User).filter_by(email=email).first()
                return user
        except SQLAlchemyError as e:
            print(f"Error occurred during get_by_email: {e}")
            raise e

    def delete_by_email(self, email: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                user = session.query(User).filter_by(email=email).first()

                if user:
                    session.delete(user)
                    session.commit()
                else:
                    print(f"User with email {email} not found.")
                    return None
        except SQLAlchemyError as e:
            print(f"Error occurred during delete_by_email: {e}")
            raise e
