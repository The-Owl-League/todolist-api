import datetime
from typing import Optional, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User


async def get_user(
        session: Session,
        id_: int = None,
) -> Optional[User]:
    query = select(User)

    if id_ is not None:
        query = query.where(User.id == id_)

    result = session.execute(query).scalar_one_or_none()

    return result


async def create_user(
        session: Session,
        first_name: str,
        second_name: str,
        patronymic: str,
        password_hash: str,
        role: str,
        email: str,
        telegram_id: Optional[str]
) -> int:
    obj = User(
        first_name=first_name,
        second_name=second_name,
        patronymic=patronymic,
        password_hash=password_hash,
        role=role,
        email=email,
        telegram_id=telegram_id,
        created_at=datetime.datetime.utcnow()
    )

    session.add(obj)
    session.flush()
    session.commit()

    return obj.id


async def get_all_users(session: Session) -> Iterable[User]:
    result = session.execute(select(User))
    return result
