import os
import sys
import logging
from datetime import datetime

from loguru import logger

from fast_admin.models.logs import Log
from fast_admin.core.config import settings


class AsyncioHandler:
    """将日志信息写入到数据库的处理器"""

    async def write(self, message) -> None:
        """写入日志记录到数据库"""
        record = message.record

        await Log.create(
            level=record["level"].name,
            message=record["message"],
            process=str(record.get("process")),
            thread=str(record.get("thread")),
            logger_name=record.get("name", ""),
            module=record.get("module", ""),
            line_no=record.get("line", 0),
            function_name=record.get("function", ""),
            exception=record.get("exception", ""),
        )


def setup_logging() -> None:
    """
    配置日志记录，并将uvicorn日志重定向到loguru

    Args:
        app: FastAPI应用实例
    """
    # 移除默认的处理器
    logger.remove()

    # 定义日志格式
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: ^8}</level> | "
        "process [<cyan>{process}</cyan>]:<cyan>{thread}</cyan> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 添加控制台处理器
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.DEBUG else "INFO",  # 调试模式下输出DEBUG级别日志
        enqueue=True,  # 使用队列以确保多线程安全
        backtrace=True,  # 启用回溯以便于调试
        diagnose=True,  # 启用诊断信息
    )

    # 添加异步数据库处理器
    logger.add(
        AsyncioHandler().write,
        format=log_format,
        level="INFO",
        enqueue=True,
        serialize=True,
        backtrace=True,

    )

    # 日志文件路径
    log_path = os.path.join(settings.BASE_DIR, 'logs', f'{datetime.now():%Y-%m-%d}.log')

    # 如果文件夹不存在则创建
    if not os.path.exists(os.path.dirname(log_path)):
        os.mkdir(os.path.dirname(log_path))

    # 添加文件处理器
    logger.add(
        log_path,
        format=log_format,
        level="INFO",
        rotation="00:00",  # 每天午夜轮换日志文件
        retention="30 days",  # 日志保留30天
        compression="zip",  # 旧日志文件压缩为zip
        enqueue=True,
        backtrace=True,
        diagnose=True
    )

    # 重定向logging到loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # 将日志级别从标准logging映射到loguru的字符串级别
            level = logging.getLevelName(record.levelno)
            # 将日志消息发送到loguru
            logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # 重定向Uvicorn的日志到Loguru
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [InterceptHandler()]
        uvicorn_logger.propagate = False
