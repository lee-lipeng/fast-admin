import time

from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fast_admin.core.config import settings
from fast_admin.core.security import get_current_user


# 自定义中间件，用于记录请求处理时间
async def process_time_middleware(request: Request, call_next):
    # Request处理
    start_time = time.time()
    response: Response = await call_next(request)
    # Response处理
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def auth_middleware(request: Request, call_next):
    """
    身份验证中间件.

    此中间件用于验证请求中的 JWT 令牌，并获取当前用户信息。
    """
    if request.url.path not in settings.AUTH_WHITELIST:
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            # 获取当前用户
            request.state.user = await get_current_user(token)
        else:
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "未提供有效的身份验证令牌"}
            )
    return await call_next(request)


# 使用FastAPI自带的CORSMiddleware跨域中间件
def cors_middleware(app, settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )
