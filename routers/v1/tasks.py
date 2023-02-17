from typing import Union

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
    responses={
        404: {"models": Union[
            err_responses.Schemas.UserNotFound,
            err_responses.Schemas.TaskNotFound,
            err_responses.Schemas.ProjectNotFound
        ]}
    }
)
async def create_task(
        session: Session = Depends(database_session),
        task: schemas.task.CreateTask = ...
):

    """ Create user endpoint """

    owner = await crud.user.get_user(
        session,
        task.owner_id
    )

    if owner is None:
        raise err_responses.Exceptions.UserNotFound()

    task_id = await crud.task.create_task(
        session,
        title=task.title,
        status=str(task.status.value),
        deadline=task.deadline,
        majority=task.majority,
        text=task.text,
        project_id=task.project_id
    )

    await crud.access_relation.create_access_relation(
        session,
        user_id=task.owner_id,
        permission=str(schemas.access_relation.Permission.READ.value),
        task_id=task_id,
        project_id=task.project_id
    )

    task = await get_task(
        session,
        task_id=task_id
    )

    return task


@router.get(
    '/tasks',
    response_model=schemas.task.TaskList
)
async def tasks_search(
        session: Session = Depends(database_session),
        user_id: int = None,
        project_id: int = None,
        status: schemas.task.TaskStatus = None,

):
    """ Search user endpoint """

    result = []

    for i in await crud.task.find_task_list(
        session,
        user_id=user_id,
        project_id=project_id,
        status=str(status.value)
    ):
        result.append(
            schemas.task.Task(
                id=i.id,
                title=i.title,
                status=i.status,
                deadline=i.deadline,
                majority=i.majority,
                text=i.text
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
