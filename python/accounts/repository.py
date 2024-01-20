from typing import List

from sqlalchemy.orm import sessionmaker

from .models import CreateAccountRequest, UpdateAccountRequest, Account
from .queries import (
    CREATE_ACCOUNT_QUERY,
    UPDATE_ACCOUNT_QUERY,
    LIST_ACCOUNTS_QUERY,
    GET_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY,
    DELETE_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY,
    DELETE_ACCOUNT_BY_ACCOUNT_ID_QUERY)


class AccountsRepository:
    def __init__(self, database) -> None:
        self.database = database
        print(f"Initialized AccountsRepository with database: {self.database}")

    def create(self, request: CreateAccountRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                session.execute(
                    CREATE_ACCOUNT_QUERY,
                    {"user_id": request.user_id, "account_number": request.account_number, "balance": request.balance}
                )
                session.commit()
        except Exception as e:
            print(f"Error occurred during create: {e}")
            raise e

    def update(self, account_number: str, request: UpdateAccountRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                session.execute(
                    UPDATE_ACCOUNT_QUERY,
                    {"balance": request.balance, "account_number": account_number}
                )
                session.commit()
        except Exception as e:
            print(f"Error occurred during update: {e}")
            raise e

    def list(self) -> List[Account]:
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                print(f"Initialized AccountsRepository with session: {session}")
                result = session.execute(LIST_ACCOUNTS_QUERY)
                rows = result.fetchall()
                accounts = [Account(*row) for row in rows]
                return accounts
        except Exception as e:
            print(f"Error occurred during list: {e}")
            raise e

    def get_by_number(self, account_number: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                result = session.execute(GET_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY, {"account_number": account_number})
                row = result.fetchone()

                if row is None:
                    return None

                return Account(*row)
        except Exception as e:
            print(f"Error occurred during get_by_number: {e}")
            raise e

    def delete_by_id(self, account_id: int):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                session.execute(DELETE_ACCOUNT_BY_ACCOUNT_ID_QUERY, {"account_id": account_id})
                session.commit()
        except Exception as e:
            print(f"Error occurred during delete_by_id: {e}")
            raise e

    def delete_by_number(self, account_number: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                session.execute(DELETE_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY, {"account_number": account_number})
                session.commit()
        except Exception as e:
            print(f"Error occurred during delete_by_number: {e}")
            raise e