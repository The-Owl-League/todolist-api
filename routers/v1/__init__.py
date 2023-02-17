from fastapi import APIRouter

from . import user, task, access_relaction

router = APIRouter(prefix='/v1')


router.include_router(user.router)
router.include_router(task.router)
router.include_router(access_relaction.router)
