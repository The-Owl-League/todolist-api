from fastapi import APIRouter

from . import user, task

router = APIRouter(prefix='/v1')


router.include_router(user.router)
router.include_router(task.router)
