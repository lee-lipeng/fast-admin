import asyncio
import sys
import json
import logging
from loguru import logger
from fast_admin.models.logs import Log

log_queue = asyncio.Queue()


class AsyncioQueueHandler:
    """将日志信息写入 asyncio 队列的处理器"""

    def __init__(self):
        self.log_queue = log_queue

    async def write(self, message):
        """写入日志记录到 asyncio 队列"""
        try:
            await self.log_queue.put(message)
        except Exception as e:
            logger.error(f"写入日志到队列失败: {e}")


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
        level="INFO",
        enqueue=True,  # 使用队列以确保多线程安全
        backtrace=True,  # 启用回溯以便于调试
        diagnose=True,  # 启用诊断信息
    )

    # 添加Redis队列处理器
    redis_handler = AsyncioQueueHandler()
    logger.add(
        redis_handler.write,
        format=log_format,
        level="INFO",
        serialize=True,  # 序列化为JSON格式
        enqueue=True
    )

    # 重定向标准的logging到loguru
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


async def process_logs_from_queue():
    """
   从 asyncio 队列中处理日志并写入数据库
   """
    while True:
        try:
            # 从队列中获取日志数据
            log_data = await log_queue.get()
            log_data = json.loads(log_data).get('record')
            # 处理日志数据
            await Log.create(
                level=log_data['level'].get('name'),
                message=log_data['message'],
                logger_name=log_data.get('name', ''),
                module=log_data.get('module', ''),
                line_no=log_data.get('line', 0),
                function_name=log_data.get('function', ''),
                exception=log_data.get('exception', ''),
            )
            # 标记任务完成
            log_queue.task_done()
        except json.JSONDecodeError as json_error:
            logger.error(f"JSON解码错误: {json_error}")
        except Exception as e:
            logger.error(f"处理日志队列时出错: {e}")
