from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Form
from typing import Optional
from database import crud
from database import exceptions as database_exceptions

from schemas import v1 as schemas
from schemas.v1.extra import err_responses

from utils.security import hash_password

from ..common import database_session

from .users import create_user


router = APIRouter(tags=['User'])


@router.post(
    '/register_user',
    response_model=schemas.user.User
)
async def register_user(
        session: Session = Depends(database_session),
        role: str = Form(...),
        email: str = Form(...),
        first_name: str = Form(...),
        second_name: str = Form(...),
        patronymic: str = Form(...),
        password: str = Form(...),
        telegram_id: Optional[str] = Form(None)
):
    normalized_request = schemas.user.CreateUser(
        role=role,
        email=email,
        first_name=first_name,
        second_name=second_name,
        patronymic=patronymic,
        password=password,
        telegram_id=telegram_id
    )
    return await create_user(session, normalized_request)
