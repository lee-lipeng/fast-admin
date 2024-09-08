from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware


# 示例自定义中间件
async def header_middleware(request: Request, call_next):
    # Request处理
    response: Response = await call_next(request)
    # Response处理
    response.headers["X-Header"] = "fast_admin"
    return response


# 使用FastAPI自带的CORSMiddleware跨域中间件
def cors_middleware(app, settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )
