from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from database import crud
from database import exceptions as database_exceptions

from schemas import v1 as schemas
from schemas.v1.extra import err_responses


from ..common import database_session


router = APIRouter(tags=['User'])


@router.post(
    '/tasks/',
    response_model=schemas.task.Task,
)
async def create_task(
        session: Session = Depends(database_session),
        task: schemas.task.CreateTask = ...
):

    """ Create user endpoint """

    task_id = await crud.task.create_task(
        session,
        title=task.title,
        status=str(task.status.value),
        deadline=task.deadline,
        majority=task.majority,
        text=task.text
    )

    task = await get_task(
        session,
        task_id=task_id
    )

    return task


@router.get(
    '/tasks',
    response_model=schemas.user.UserList
)
async def tasks_search(
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
    '/tasks/{task_id}',
    response_model=schemas.task.Task,
    responses={
        404: {"model": err_responses.Schemas.TaskNotFound}
    }
)
async def get_task(
        session: Session = Depends(database_session),
        task_id: int = ...
):
    """ Get user by id endpoint """

    db_task = await crud.task.get_task(
        session,
        id_=task_id
    )

    if db_task is None:
        raise err_responses.Exceptions.TaskNotFound()

    result = schemas.task.Task(
        id=db_task.id,
        title=db_task.title,
        status=db_task.status,
        deadline=db_task.deadline,
        majority=db_task.majority,
        text=db_task.text
    )

    return result
