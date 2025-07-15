import time
from typing import Callable

from fastapi import Request, Response, status, FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fast_admin.core.config import settings
from fast_admin.core.security import get_current_user


# 自定义中间件，用于记录请求处理时间
async def process_time_middleware(request: Request, call_next: Callable) -> Response:
    # Request处理
    start_time = time.time()
    response: Response = await call_next(request)
    # Response处理
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def auth_middleware(request: Request, call_next: Callable) -> Response:
    """
    身份验证中间件。

    此中间件用于验证请求中的 JWT 令牌，并获取当前用户信息。

    Args:
        request: FastAPI请求对象
        call_next: 下一个中间件或路由处理函数

    Returns:
        Response: 响应对象
    """
    # 检查是否在白名单中
    if _is_path_in_whitelist(request.url.path):
        return await call_next(request)

    # 获取Authorization头
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "未提供有效的身份验证令牌"}
        )

    # 提取token
    token = authorization.split(" ")[1]

    # 获取当前用户并存储在请求状态中
    request.state.user = await get_current_user(token)

    return await call_next(request)


def cors_middleware(app: FastAPI) -> None:
    """
    配置CORS中间件。

    Args:
        app: FastAPI应用实例
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )


def _is_path_in_whitelist(path: str) -> bool:
    """
    检查路径是否在白名单中。

    Args:
        path: 请求路径

    Returns:
        bool: 如果在白名单中返回True，否则返回False
    """
    # 精确匹配
    if path in settings.AUTH_WHITELIST:
        return True

    # 前缀匹配（用于处理带参数的路径）
    for whitelist_path in settings.AUTH_WHITELIST:
        if whitelist_path.endswith("/") and path.startswith(whitelist_path):
            return True

    return False
