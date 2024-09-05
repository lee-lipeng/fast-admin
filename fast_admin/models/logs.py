from tortoise import fields

from fast_admin.models.base import BaseModel


class Log(BaseModel):
    """日志模型"""

    id = fields.IntField(pk=True, description="日志ID")
    level = fields.CharField(max_length=20, description="日志级别")
    message = fields.TextField(description="日志消息")
    timestamp = fields.DatetimeField(auto_now_add=True, description="时间戳")
    process = fields.CharField(max_length=255, null=True, description="进程信息")
    thread = fields.CharField(max_length=255, null=True, description="线程信息")
    logger_name = fields.CharField(max_length=255, null=True, description="记录器名称")
    module = fields.CharField(max_length=255, null=True, description="模块名称")
    line_no = fields.IntField(null=True, description="行号")
    function_name = fields.CharField(max_length=255, null=True, description="函数名称")
    exception = fields.TextField(null=True, description="异常信息")

    class Meta:
        table = "logs"
        ordering = ["-timestamp"]  # 默认按时间倒序排列
