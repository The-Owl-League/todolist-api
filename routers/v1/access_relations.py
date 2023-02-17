from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from database import crud
from database import exceptions as database_exceptions

from schemas import v1 as schemas
from schemas.v1.extra import err_responses


from ..common import database_session


router = APIRouter(tags=['User'])


@router.post(
    '/access_relations',
    response_model=schemas.access_relation.AccessRelation,
)
async def create_access_relation(
        session: Session = Depends(database_session),
        access_relation: schemas.access_relation.CreateAccessRelation = ...
):

    """ Create user endpoint """

    access_relation_id = await crud.access_relation.create_access_relation(
        session,
        user_id=access_relation.user_id,
        permission=str(access_relation.permission.value),
        task_id=access_relation.task_id,
        project_id=access_relation.project_id
    )

    access_relation = await get_access_relation(
        session,
        access_relation_id=access_relation_id
    )

    return access_relation


@router.get(
    '/access_relations',
    response_model=schemas.access_relation.AccessRelationList
)
async def access_relation_search(
        session: Session = Depends(database_session),
):
    """ Search user endpoint """

    result = []

    for (i,) in await crud.access_relation.get_all_access_relations(session):
        i: crud.access_relation.AccessRelation
        result.append(
            schemas.access_relation.AccessRelation(
                id=i.id,
                permission=i.permission,
                user_id=i.fk_user_id,
                task_id=i.fk_task_id,
                project_id=i.fk_project_id
            )
        )

    return result


@router.get(
    '/access_relations/{access_relation_id}',
    response_model=schemas.access_relation.AccessRelation,
    responses={
        404: {"model": err_responses.Schemas.AccessRelationNotFound}
    }
)
async def get_access_relation(
        session: Session = Depends(database_session),
        access_relation_id: int = ...
):
    """ Get user by id endpoint """

    db_obj = await crud.access_relation.get_access_relation(
        session,
        id_=access_relation_id
    )

    if db_obj is None:
        raise err_responses.Exceptions.AccessRelationNotFound()

    result = schemas.access_relation.AccessRelation(
        id=db_obj.id,
        permission=db_obj.permission,
        user_id=db_obj.fk_user_id,
        task_id=db_obj.fk_task_id,
        project_id=db_obj.fk_project_id
    )

    return result
