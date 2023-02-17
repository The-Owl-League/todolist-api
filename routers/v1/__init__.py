from fastapi import APIRouter

from . import users, tasks, access_relations

router = APIRouter(prefix='/v1')


router.include_router(users.router)
router.include_router(tasks.router)
router.include_router(access_relations.router)
