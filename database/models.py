from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from .database import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column()
    second_name: Mapped[str] = mapped_column()
    patronymic: Mapped[str] = mapped_column()

    password_hash: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    telegram_id: Mapped[int] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column()
    deleted_at: Mapped[Optional[datetime]] = mapped_column()


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    majority: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)


class Project(Base):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()


class AccessRelation(Base):
    __tablename__ = 'access_relation'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    permission: Mapped[str] = mapped_column()

    fk_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    fk_task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=True)
    fk_project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=True)


Base.metadata.create_all(engine)
