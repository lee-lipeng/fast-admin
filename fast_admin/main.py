from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fast_admin.core.config import settings, TORTOISE_ORM
from contextlib import asynccontextmanager
from aerich import Command

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
    command = Command(
        tortoise_config=TORTOISE_ORM,
        app=settings.APP_NAME,
        location="./migrations",
    )
    await command.init()
    await command.upgrade(run_in_transaction=True)  # 在启动时执行数据库迁移

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=False,  # 这里设置为 False，因为我们将在后面实现全局异常处理
    )
    yield


app = FastAPI(lifespan=lifespan)

"""
FastAPI 应用程序实例。

这是 FastAPI 应用程序的核心对象，用于定义 API 路由、中间件和其他应用程序组件。
"""
