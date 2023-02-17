from typing import Optional

from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class Permission(Enum):
    READ = 'READ'
    WRITE = 'WRITE'
    OWNER = 'OWNER'


class CreateAccessRelation(BaseModel):
    permission: Permission
    user_id: int
    task_id: Optional[int] = None
    project_id: Optional[int] = None


class AccessRelation(BaseModel):
    id: int
    permission: Permission
    user_id: int
    task_id: Optional[int] = None
    project_id: Optional[int] = None


class AccessRelationList(BaseModel):
    __root__: list[AccessRelation]
