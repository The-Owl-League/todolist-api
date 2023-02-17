from sqlalchemy.orm import Session

from database.database import engine


async def database_session():
    with Session(engine) as session:
        yield session
