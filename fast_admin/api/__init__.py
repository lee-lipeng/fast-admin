from fastapi import APIRouter
from fast_admin.api import logs

router = APIRouter()

router.include_router(
    logs.router,
    prefix="/logs",
    tags=["日志"],
)
