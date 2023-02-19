from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Form

from database import crud
from database import exceptions as database_exceptions

from schemas import v1 as schemas
from schemas.v1.extra import err_responses

from utils.security import hash_password

from ..common import database_session


router = APIRouter(tags=['User'])


@router.post(
    '/users',
    response_model=schemas.user.User,
)
async def create_user(
        session: Session = Depends(database_session),
        user: schemas.user.CreateUser = ...
):

    """ Create user endpoint """

    user_id = await crud.user.create_user(
        session,
        first_name=user.first_name,
        second_name=user.second_name,
        patronymic=user.patronymic,
        password_hash=hash_password(user.password),
        role=user.role,
        email=user.email,
        telegram_id=user.telegram_id
    )

    user = await get_user(
        session,
        user_id=user_id
    )

    return user


@router.get(
    '/users/search',
    response_model=schemas.user.UserList
)
async def users_search(
        session: Session = Depends(database_session),
):
    """ Search user endpoint """

    result = []

    for (i,) in await crud.user.get_all_users(session):
        result.append(
            schemas.user.User(
                id=i.id,
                first_name=i.first_name,
                second_name=i.second_name,
                patronymic=i.patronymic,
                role=i.role,
                email=i.email,
                created_at=i.created_at,
                deleted_at=i.deleted_at
            )
        )

    return result


@router.get(
    '/users/{user_id}',
    response_model=schemas.user.User,
    responses={
        404: {"model": err_responses.Schemas.UserNotFound}
    }
)
async def get_user(
        session: Session = Depends(database_session),
        user_id: int = ...
):
    """ Get user by id endpoint """

    db_user = await crud.user.get_user(
        session,
        id_=user_id
    )

    if db_user is None:
        raise err_responses.Exceptions.UserNotFound()

    result = schemas.user.User(
        id=db_user.id,
        first_name=db_user.first_name,
        second_name=db_user.second_name,
        patronymic=db_user.patronymic,
        role=db_user.role,
        email=db_user.email,
        created_at=db_user.created_at,
        deleted_at=db_user.deleted_at
    )

    return result
