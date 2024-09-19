from fastapi import APIRouter
from fast_admin.api import logs, permissions, roles, users, auth

router = APIRouter()

router.include_router(
    logs.router,
    prefix="/logs",
    tags=["日志"],
)
router.include_router(
    permissions.router,
    prefix="/permissions",
    tags=["权限"],
)
router.include_router(
    roles.router,
    prefix="/roles",
    tags=["角色"],
)
router.include_router(
    users.router,
    prefix="/users",
    tags=["用户"],
)
router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证"],
)
