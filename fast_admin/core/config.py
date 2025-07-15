"""
配置模块。

此模块包含应用程序的配置信息，包括：

- 加载环境变量。
- 定义 Settings 类，用于存储应用程序的配置信息。
- 定义 TORTOISE_ORM 字典，用于配置 Tortoise-ORM。

"""

import os
import secrets
from pathlib import Path
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, set_key

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 加载.env文件中的环境变量
load_dotenv(BASE_DIR / ".env")


# 检查.env文件中是否存在SECRET_KEY，若不存在则随机生成并添加到.env文件中
def ensure_secret_key() -> str:
    """确保SECRET_KEY存在，如果不存在则生成一个新的"""
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        secret_key = secrets.token_urlsafe(32)
        env_file = BASE_DIR / ".env"
        if env_file.exists():
            set_key(str(env_file), "SECRET_KEY", secret_key)
        # 将生成的密钥添加到环境变量中
        os.environ["SECRET_KEY"] = secret_key
    return secret_key


class Settings(BaseSettings):
    """
    应用程序的配置信息。

    此类继承自 pydantic_settings.BaseSettings，用于定义应用程序的配置信息。
    """
    # 应用基本信息
    DEBUG: bool = Field(default=False, description="调试模式")
    APP_NAME: str = Field(default="fast_admin", description="应用程序名称")
    APP_VERSION: str = Field(default="0.1.0", description="应用程序版本号")
    APP_TITLE: Optional[str] = Field(default=None, description="应用程序标题")
    APP_DESCRIPTION: str = Field(
        default="本项目是一个基于 FastAPI 框架、Tortoise-ORM 和 PostgreSQL 数据库构建的开源角色权限管理系统",
        description="应用程序描述"
    )

    # 安全配置
    SECRET_KEY: str = Field(default_factory=ensure_secret_key, description="应用程序密钥")
    ALGORITHM: str = Field(default="HS256", description="JWT加密算法")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 8, description="访问令牌有效期（分钟）")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 8, description="刷新令牌有效期（分钟）")
    AUTH_WHITELIST: List[str] = Field(
        default=["/docs", "/redoc", "/openapi.json", "/auth/login", "/users/"],
        description="不需要登录即可访问的路由列表"
    )

    # 数据库配置
    DATABASE_USER: str = Field(..., description="数据库用户名")
    DATABASE_PASSWORD: str = Field(..., description="数据库密码")
    DATABASE_HOST: str = Field(..., description="数据库主机名")
    DATABASE_PORT: int = Field(..., description="数据库端口号")
    DATABASE_NAME: str = Field(..., description="数据库名称")
    DB_MIN_CONNECTIONS: int = Field(default=5, description="数据库连接池最小连接数")
    DB_MAX_CONNECTIONS: int = Field(default=10, description="数据库连接池最大连接数")
    TIMEZONE: str = Field(default="Asia/Shanghai", description="时区设置")

    # Redis配置
    REDIS_HOST: Optional[str] = Field(default=None, description="Redis主机名")
    REDIS_PORT: Optional[int] = Field(default=None, description="Redis端口号")
    REDIS_DB: Optional[int] = Field(default=None, description="Redis数据库号")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis密码")

    # CORS配置
    ALLOW_ORIGINS: List[str] = Field(default=["*"], description="允许跨域请求的源")
    ALLOW_CREDENTIALS: bool = Field(default=True, description="是否允许跨域请求携带凭据")
    ALLOW_METHODS: List[str] = Field(default=["*"], description="允许跨域请求的方法")
    ALLOW_HEADERS: List[str] = Field(default=["*"], description="允许跨域请求的头部")

    # 中间件配置
    MIDDLEWARE: List[str] = Field(
        default=[
            "process_time_middleware",
            "cors_middleware",
            "auth_middleware"
        ],
        description="中间件配置列表"
    )

    @field_validator("APP_TITLE", mode="before")
    @classmethod
    def set_app_title(cls, v, info):
        """如果未设置APP_TITLE，则根据APP_NAME和APP_VERSION生成"""
        if v is None and info.data:
            app_name = info.data.get("APP_NAME", "fast_admin")
            app_version = info.data.get("APP_VERSION", "0.1.0")
            return f"{app_name} v{app_version}"
        return v

    class Config:
        """Pydantic配置"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的环境变量


# 创建全局设置实例
settings = Settings()

# Tortoise-ORM配置
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
