from tortoise import fields

from fast_admin.models.base import BaseModel


class Permission(BaseModel):
    """
    权限模型

    Attributes:
        id: 权限ID.
        name: 权限名称 (例如: "查看用户列表").
        code: 权限代码 (例如: "user:list").
               建议使用 "资源:操作" 的格式，例如 "user:list" 表示对用户资源进行列表操作.
        type: 权限类型 (例如: "page", "operation", "data").
        description: 权限描述.
    """
    id = fields.IntField(pk=True, description="权限ID")
    name = fields.CharField(max_length=255, unique=True, description="权限名称")
    code = fields.CharField(max_length=255, unique=True, description="权限代码")
    type = fields.CharField(max_length=20, choices=[("page", "页面权限"), ("operation", "操作权限"), ("data", "数据权限")], description="权限类型")
    description = fields.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
