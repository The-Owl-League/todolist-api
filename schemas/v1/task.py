from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class CreateTask(BaseModel):
    owner_id: int
    title: str
    deadline: datetime
    majority: str
    text: Optional[str] = None


class Task(BaseModel):
    id: int

    first_name: str
    second_name: str
    patronymic: str

    role: str
    email: str
    telegram_id: Optional[str]

    created_at: datetime
    deleted_at: Optional[datetime]


class TaskList(BaseModel):
    __root__: list[Task]
