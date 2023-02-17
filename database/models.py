from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from .database import engine


class Base(DeclarativeBase):
    pass


# place to declare models


Base.metadata.create_all(engine)
