import datetime
from typing import Optional, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Project, AccessRelation, User, Project
from .access_relation import find_access_relations


async def get_project(
        session: Session,
        id_: int = None,
) -> Optional[Project]:
    query = select(Project)

    if id_ is not None:
        query = query.where(Project.id == id_)

    result = session.execute(query).scalar_one_or_none()

    return result


async def get_user_project_by_tittle(
        session: Session,
        user_id: int,
        tittle: str,
) -> Optional[Project]:
    query = select(Project)

    query = query.where(Project.fk_user_id == user_id)
    query = query.where(Project.title == tittle)

    result = session.execute(query).scalar_one_or_none()

    return result


async def create_project(
        session: Session,
        user_id: int,
        title: str
) -> int:

    obj = Project(
        fk_user_id=user_id,
        title=title,
    )

    session.add(obj)
    session.flush()
    session.commit()

    return obj.id


async def get_all_projects(session: Session) -> Iterable[Project]:
    result = session.execute(select(Project))
    return result
