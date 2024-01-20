from typing import List, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .models import CreateAccountRequest, UpdateAccountRequest, Account


class AccountsRepository:
    def __init__(self, database) -> None:
        self.database = database
        print(f"Initialized AccountsRepository with database: {self.database}")

    def create(self, request: CreateAccountRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                account = Account(user_id=request.user_id, account_number=request.account_number,
                                  balance=request.balance)
                session.add(account)
                session.commit()
        except SQLAlchemyError as e:
            print(f"Error occurred during create: {e}")
            raise e

    def update(self, account_number: str, request: UpdateAccountRequest):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                account = session.query(Account).filter_by(account_number=account_number).first()

                if account:
                    account.balance = request.balance
                    session.commit()
                else:
                    print(f"Account with account_number {account_number} not found.")
        except SQLAlchemyError as e:
            print(f"Error occurred during update: {e}")
            raise e

    def list(self) -> list[Type[Account]]:
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                accounts = session.query(Account).all()
                return accounts
        except SQLAlchemyError as e:
            print(f"Error occurred during list: {e}")
            raise e

    def get_by_number(self, account_number: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                account = session.query(Account).filter_by(account_number=account_number).first()
                return account
        except SQLAlchemyError as e:
            print(f"Error occurred during get_by_number: {e}")
            raise e

    def delete_by_id(self, account_id: int):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                account = session.query(Account).filter_by(account_id=account_id).first()

                if account:
                    session.delete(account)
                    session.commit()
                else:
                    print(f"Account with account_id {account_id} not found.")
        except SQLAlchemyError as e:
            print(f"Error occurred during delete_by_id: {e}")
            raise e

    def delete_by_number(self, account_number: str):
        try:
            with sessionmaker(bind=self.database.engine)() as session:
                account = session.query(Account).filter_by(account_number=account_number).first()

                if account:
                    session.delete(account)
                    session.commit()
                else:
                    print(f"Account with account_number {account_number} not found.")
        except SQLAlchemyError as e:
            print(f"Error occurred during delete_by_number: {e}")
            raise e