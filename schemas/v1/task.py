from typing import Optional, Union

from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class TaskStatus(Enum):
    NEW = 'NEW'
    DONE = 'DONE'


class CreateTask(BaseModel):
    status: TaskStatus = TaskStatus.NEW
    title: str
    deadline: datetime
    majority: str
    text: Optional[str] = None
    project: Optional[Union[int, str]] = None


class Task(BaseModel):
    id: int
    title: str
    status: str
    deadline: Optional[datetime]
    majority: Optional[str]
    text: Optional[str]
    project: Optional[str]
    project_id: Optional[int]


class TaskList(BaseModel):
    __root__: list[Task]
