import datetime
from typing import Optional, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Task, AccessRelation, User, Project
from .access_relation import find_access_relations


async def get_task(
        session: Session,
        id_: int = None,
) -> Optional[Task]:
    query = select(Task)

    if id_ is not None:
        query = query.where(Task.id == id_)

    result = session.execute(query).scalar_one_or_none()

    return result


async def find_task_list(
        session: Session,
        user_id: int = None,
        project_id: int = None,
        status: str = None
) -> list[Task]:

    # I'm sorry about this :)

    access_relations = await find_access_relations(
        session, user_id, project_id
    )

    result = []

    for (i,) in access_relations:
        i: AccessRelation
        task = await get_task(session, i.fk_task_id)
        if status is None or task.status == status:
            result.append(task)

    return result


async def create_task(
        session: Session,
        title: str,
        status: str,
        deadline: datetime,
        majority: str,
        text: str,
        project_id: int
) -> int:

    obj = Task(
        title=title,
        status=status,
        deadline=deadline,
        majority=majority,
        text=text,
        fk_project_id=project_id
    )

    session.add(obj)
    session.flush()
    session.commit()

    return obj.id


async def get_all_tasks(session: Session) -> Iterable[Task]:
    result = session.execute(select(Task))
    return result
