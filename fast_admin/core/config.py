import secrets

from pydantic_settings import BaseSettings
from dotenv import load_dotenv, set_key
import os

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

    - APP_NAME: 应用程序的名称。
    - SECRET_KEY: 应用程序的密钥。
    - DATABASE_USER: 数据库用户名。
    - DATABASE_PASSWORD: 数据库密码。
    - DATABASE_HOST: 数据库主机名。
    - DATABASE_PORT: 数据库端口号。
    - DATABASE_NAME: 数据库名称。
    - DB_MIN_CONNECTIONS: 数据库连接池最小连接数。
    - DB_MAX_CONNECTIONS: 数据库连接池最大连接数。

    """
    APP_NAME: str = "FastAdmin"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")  # 从环境变量中获取密钥
    DATABASE_USER: str = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST")
    DATABASE_PORT: int = os.environ.get("DATABASE_PORT")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")
    DB_MIN_CONNECTIONS: int = os.environ.get("DB_MIN_CONNECTIONS", 5)  # 数据库连接池最小连接数
    DB_MAX_CONNECTIONS: int = os.environ.get("DB_MAX_CONNECTIONS", 10) # 数据库连接池最大连接数


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
            "minsize": settings.DB_MIN_CONNECTIONS,  # 最小连接数
            "maxsize": settings.DB_MAX_CONNECTIONS,  # 最大连接数
        }
    },
    "apps": {
        "models": {
            "models": ["fast_admin.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}