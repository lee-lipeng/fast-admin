import time

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware

# 自定义中间件，用于记录请求处理时间
async def process_time_middleware(request: Request, call_next):
    # Request处理
    start_time = time.time()
    response: Response = await call_next(request)
    # Response处理
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
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
