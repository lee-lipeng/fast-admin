from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from contextlib import asynccontextmanager
from aerich import Command

from fast_admin.core.config import settings, TORTOISE_ORM
from fast_admin.core.logger import setup_logging
from fast_admin.api import router

"""
FastAPI 应用程序的主入口点。

此模块包含 FastAPI 应用程序的初始化和配置，包括：

- 创建 FastAPI 应用程序实例。
- 使用 lifespan 上下文管理器管理数据库迁移和 Tortoise-ORM 注册。
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 应用程序的 Lifespan 上下文管理器。

    此函数在应用程序启动和关闭时执行，用于管理数据库迁移和 Tortoise-ORM 注册。

    Args:
        app: FastAPI 应用程序实例。
    """
    # 注册 Tortoise-ORM
    register_tortoise(
        app,
        config=TORTOISE_ORM
    )

    # 初始化 Aerich 的命令对象，用于数据库迁移
    command = Command(
        tortoise_config=TORTOISE_ORM,
        app=settings.APP_NAME,
        location="./migrations",
    )

    # 运行数据库迁移
    await command.init()
    await command.upgrade(run_in_transaction=True)

    # 注册 Redis 客户端到 FastAPI 应用程序状态
    # app.state.redis = Redis(
    #     host=settings.REDIS_HOST,
    #     port=settings.REDIS_PORT,
    #     db=settings.REDIS_DB,
    #     decode_responses=True
    # )

    # 设置应用程序日志
    setup_logging()

    yield


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.include_router(router)

"""
FastAPI 应用程序实例。

这是 FastAPI 应用程序的核心对象，用于定义 API 路由、中间件和其他应用程序组件。
"""
