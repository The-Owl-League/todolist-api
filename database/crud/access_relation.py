from typing import Optional, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import AccessRelation


async def get_access_relation(
        session: Session,
        id_: int = None,
) -> Optional[AccessRelation]:

    query = select(AccessRelation)

    if id_ is not None:
        query = query.where(AccessRelation.id == id_)

    result = session.execute(query).scalar_one_or_none()

    return result


async def create_access_relation(
        session: Session,
        user_id: int,
        permission: str,
        task_id: Optional[int] = None,
        project_id: Optional[int] = None
) -> int:

    obj = AccessRelation(
        permission=permission,
        fk_user_id=user_id,
        fk_task_id=task_id,
        fk_project_id=project_id
    )

    session.add(obj)
    session.flush()
    session.commit()

    return obj.id


async def find_access_relations(
        session: Session,
        user_id: int,
        project_id: int = None,
        task_id: int = None
):
    query = (select(AccessRelation)
             .where(AccessRelation.fk_user_id == user_id))

    if project_id is not None:
        query = query.where(AccessRelation.fk_project_id == project_id)

    if task_id is not None:
        query = query.where(AccessRelation.fk_task_id == task_id)

    result = session.execute(query)

    return result


async def get_all_access_relations(session: Session) -> Iterable[AccessRelation]:
    result = session.execute(select(AccessRelation))
    return result
