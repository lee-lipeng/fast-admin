import os
import secrets
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, set_key

"""
配置模块。

此模块包含应用程序的配置信息，包括：

- 加载环境变量。
- 定义 Settings 类，用于存储应用程序的配置信息。
- 定义 TORTOISE_ORM 字典，用于配置 Tortoise-ORM。

"""

# 加载.env文件中的环境变量
load_dotenv()

# 检查.env文件中是否存在SECRET_KEY，若不存在则随机生成并添加到.env文件中
if not os.environ.get("SECRET_KEY"):
    secret_key = secrets.token_urlsafe(32)
    set_key(".env", "SECRET_KEY", secret_key)
    # 将生成的密钥添加到环境变量中
    os.environ["SECRET_KEY"] = secret_key


class Settings(BaseSettings):
    """
    应用程序的配置信息。

    此类继承自 pydantic_settings.BaseSettings，用于定义应用程序的配置信息，包括：

    - DEBUG: 调试模式。
    - APP_NAME: 应用程序的名称。
    - APP_VERSION: 应用程序的版本号。
    - APP_TITLE: 应用程序的标题。
    - APP_DESCRIPTION: 应用程序的描述。
    - SECRET_KEY: 应用程序的密钥。
    - DATABASE_USER: 数据库用户名。
    - DATABASE_PASSWORD: 数据库密码。
    - DATABASE_HOST: 数据库主机名。
    - DATABASE_PORT: 数据库端口号。
    - DATABASE_NAME: 数据库名称。
    - DB_MIN_CONNECTIONS: 数据库连接池最小连接数。
    - DB_MAX_CONNECTIONS: 数据库连接池最大连接数。
    - TIMEZONE: 时区设置。
    - REDIS_HOST: Redis 主机名。
    - REDIS_PORT: Redis 端口号。
    - REDIS_DB: Redis 数据库号。
    - ALLOW_ORIGINS: 允许跨域请求的源。
    - ALLOW_CREDENTIALS: 是否允许跨域请求携带凭据。
    - ALLOW_METHODS: 允许跨域请求的方法。
    - ALLOW_HEADERS: 允许跨域请求的头部。
    - MIDDLEWARE: 中间件配置列表。

    """
    DEBUG: bool = False

    APP_NAME: str = "fast_admin"
    APP_VERSION: str = "0.1.0"
    APP_TITLE: str = f"{APP_NAME} v{APP_VERSION}"
    APP_DESCRIPTION: str = "本项目是一个基于 FastAPI 框架、Tortoise-ORM 和 PostgreSQL 数据库构建的开源角色权限管理系统"

    SECRET_KEY: str = os.environ.get("SECRET_KEY")

    DATABASE_USER: str = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST")
    DATABASE_PORT: int = os.environ.get("DATABASE_PORT")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")
    DB_MIN_CONNECTIONS: int = os.environ.get("DB_MIN_CONNECTIONS", 5)
    DB_MAX_CONNECTIONS: int = os.environ.get("DB_MAX_CONNECTIONS", 10)
    TIMEZONE: str = "Asia/Shanghai"

    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: int = os.environ.get("REDIS_PORT")
    REDIS_DB: int = os.environ.get("REDIS_DB")

    ALLOW_ORIGINS: list = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list = ["*"]
    ALLOW_HEADERS: list = ["*"]

    MIDDLEWARE: list = [
        # 按序加载中间件配置列表
        "process_time_middleware",
        "cors_middleware",
    ]


settings = Settings()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.DATABASE_HOST,
                "port": settings.DATABASE_PORT,
                "user": settings.DATABASE_USER,
                "password": settings.DATABASE_PASSWORD,
                "database": settings.DATABASE_NAME,
            },
            "minsize": settings.DB_MIN_CONNECTIONS,
            "maxsize": settings.DB_MAX_CONNECTIONS,
        }
    },
    "apps": {
        settings.APP_NAME: {
            "models": [f"{settings.APP_NAME}.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": settings.TIMEZONE,
}
