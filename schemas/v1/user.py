from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    role: str
    email: str
    first_name: str
    second_name: str
    patronymic: str
    password: str
    telegram_id: Optional[str] = None


class User(BaseModel):
    id: int
    first_name: str
    second_name: str
    patronymic: str
    role: str
    email: str
    telegram_id: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime]


class UserAuthInfo(BaseModel):
    user_id: int
    password_hash: str


class UserList(BaseModel):
    __root__: list[User]
