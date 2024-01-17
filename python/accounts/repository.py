from .models import CreateAccountRequest, UpdateAccountRequest, Account
from .queries import (
    CREATE_ACCOUNT_QUERY,
    UPDATE_ACCOUNT_QUERY,
    LIST_ACCOUNTS_QUERY,
    GET_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY,
    DELETE_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY,
    DELETE_ACCOUNT_BY_ACCOUNT_ID_QUERY)
from common.configs import DatabaseConfig
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class AccountsRepository:
    def __init__(self, config: DatabaseConfig) -> None:
        self.engine = create_engine(config.database_url)

    def create(self, request: CreateAccountRequest):
        with Session(bind=self.engine) as db:
            db.execute(
                CREATE_ACCOUNT_QUERY,
                {"user_id": request.user_id, "account_number": request.account_number, "balance": request.balance}
            )
            db.commit()

    def update(self, account_number: str, request: UpdateAccountRequest):
        with Session(bind=self.engine) as db:
            db.execute(
                UPDATE_ACCOUNT_QUERY,
                {"balance": request.balance, "account_number": account_number}
            )
            db.commit()

    def list(self) -> List[Account]:
        with Session(bind=self.engine) as db:
            result = db.execute(LIST_ACCOUNTS_QUERY)
            rows = result.fetchall()
        accounts = [Account(row.account_id, row.account_number, row.user_id, row.balance) for row in rows]
        return accounts

    def get_by_number(self, account_number: str):
        with Session(bind=self.engine) as db:
            result = db.execute(GET_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY, {"account_number": account_number})
            row = result.fetchone()
        return Account(row.account_number, row.user_email, row.account_number, row.balance)

    def delete_by_id(self, account_id: int):
        with Session(bind=self.engine) as db:
            db.execute(DELETE_ACCOUNT_BY_ACCOUNT_ID_QUERY, {"account_id": account_id})
            db.commit()

    def delete_by_number(self, account_number: str):
        with Session(bind=self.engine) as db:
            db.execute(DELETE_ACCOUNT_BY_ACCOUNT_NUMBER_QUERY, {"account_number": account_number})
            db.commit()
