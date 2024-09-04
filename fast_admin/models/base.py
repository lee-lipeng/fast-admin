from tortoise import models
from tortoise.fields import DatetimeField


class BaseModel(models.Model):
    """基础模型，所有模型都应该继承自此模型"""

    created_at = DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True  # 将此模型设置为抽象模型，不会创建对应的数据库表
