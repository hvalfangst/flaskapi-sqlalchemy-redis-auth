from sqlalchemy import UniqueConstraint, Column, String, Integer
from security.models import AccessType
from typing import Dict, Optional
from pydantic import BaseModel, EmailStr
from common.db import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(15))
    address = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    ssn = Column(String(11), unique=True, nullable=False)
    access = Column(String(6), nullable=False)

    __table_args__ = (UniqueConstraint('email'),)

    def to_dict(self) -> Dict[str, str]:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "address": self.address,
            "email": self.email,
            "password": self.password,
            "ssn": self.ssn,
            "access": self.access
        }


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: Optional[str]
    email: EmailStr
    password: str
    ssn: str
    access: AccessType


class UpdateUserRequest(BaseModel):
    phone_number: Optional[str]
    address: Optional[str]


class Claims:
    def __init__(self, email, access, exp):
        self.email = email
        self.access = access
        self.exp = exp

    def to_dict(self):
        return {
            "email": self.email,
            "access": self.access,
            "exp": self.exp
        }
