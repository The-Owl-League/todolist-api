from typing import Union

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Cookie

from database import crud
from database import exceptions as database_exceptions

from schemas import v1 as schemas
from schemas.v1.extra import err_responses


from ..common import database_session


router = APIRouter(tags=['User'])


async def user_auth(user_id: int):
    return user_id


@router.post(
    '/tasks/',
    response_model=schemas.task.Task,
    responses={
        404: {"model": Union[
            err_responses.Schemas.UserNotFound,
            err_responses.Schemas.TaskNotFound,
            err_responses.Schemas.ProjectNotFound
        ]}
    }
)
async def create_task(
        session: Session = Depends(database_session),
        user_id: int = Depends(user_auth),
        task: schemas.task.CreateTask = ...
):

    """ Create user endpoint """

    owner = await crud.user.get_user(
        session,
        user_id
    )

    if owner is None:
        raise err_responses.Exceptions.UserNotFound()

    if isinstance(task.project, int):
        project_id = task.project
    elif isinstance(task.project, str):
        project = await crud.project.get_user_project_by_tittle(
            session,
            user_id=user_id,
            tittle=task.project
        )
        if project is None:
            project_id = await crud.project.create_project(
                session,
                user_id=user_id,
                title=task.project
            )
        else:
            project_id = project.id
    else:
        raise RuntimeError

    task_id = await crud.task.create_task(
        session,
        title=task.title,
        status=str(task.status.value),
        deadline=task.deadline,
        majority=task.majority,
        text=task.text,
        project_id=project_id
    )

    await crud.access_relation.create_access_relation(
        session,
        user_id=user_id,
        permission=str(schemas.access_relation.Permission.OWNER.value),
        task_id=task_id,
        project_id=project_id
    )

    task = await get_task(
        session,
        task_id=task_id
    )

    return task


@router.get(
    '/tasks',
    response_model=schemas.task.TaskList,
)
async def tasks_search(
        session: Session = Depends(database_session),
        user_id: int = Depends(user_auth),
        project_id: int = None,
        status: schemas.task.TaskStatus = None,

):
    """ Search user endpoint """

    result = []

    for i in await crud.task.find_task_list(
        session,
        user_id=user_id,
        project_id=project_id,
        status=str(status.value) if status else None
    ):
        if i.fk_project_id is not None:
            project = await crud.project.get_project(
                session=session,
                id_=i.fk_project_id
            )
        else:
            project = None

        result.append(
            schemas.task.Task(
                id=i.id,
                title=i.title,
                status=i.status,
                deadline=i.deadline,
                majority=i.majority,
                text=i.text,
                project_id=i.fk_project_id,
                project=project.title if i.fk_project_id else None
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

    if db_task.fk_project_id is not None:
        # noinspection PyTypeChecker
        project = await crud.project.get_project(
            session,
            id_=db_task.fk_project_id
        )
    else:
        project = None

    result = schemas.task.Task(
        id=db_task.id,
        title=db_task.title,
        status=db_task.status,
        deadline=db_task.deadline,
        majority=db_task.majority,
        text=db_task.text,
        project=project.title if project else None,
        project_id=project.id if project else None
    )

    return result
