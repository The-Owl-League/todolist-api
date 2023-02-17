from typing import Optional

from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class TaskStatus(Enum):
    NEW = 'NEW'
    DONE = 'DONE'


class CreateTask(BaseModel):
    status: TaskStatus = TaskStatus.NEW
    owner_id: int
    title: str
    deadline: datetime
    majority: str
    text: Optional[str] = None
    project_id: Optional[int] = None


class Task(BaseModel):
    id: int
    title: str
    status: str
    deadline: Optional[datetime]
    majority: Optional[str]
    text: Optional[str]


class TaskList(BaseModel):
    __root__: list[Task]
