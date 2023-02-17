import datetime
from typing import Optional, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Task


async def get_task(
        session: Session,
        id_: int = None,
) -> Optional[Task]:
    query = select(Task)

    if id_ is not None:
        query = query.where(Task.id == id_)

    result = session.execute(query).scalar_one_or_none()

    return result


async def create_task(
        session: Session,
        title: str,
        status: str,
        deadline: datetime,
        majority: str,
        text: str
) -> int:

    obj = Task(
        title=title,
        status=status,
        deadline=deadline,
        majority=majority,
        text=text
    )

    session.add(obj)
    session.flush()
    session.commit()

    return obj.id


async def get_all_tasks(session: Session) -> Iterable[Task]:
    result = session.execute(select(Task))
    return result
