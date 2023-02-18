from fastapi import APIRouter

from . import users, tasks, access_relations, public

router = APIRouter(prefix='/v1')


router.include_router(users.router)
router.include_router(tasks.router)
router.include_router(access_relations.router)
router.include_router(public.router)
