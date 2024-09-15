from tortoise import fields
from .permission import Permission
from fast_admin.models.base import BaseModel


class Role(BaseModel):
    """
    角色模型

    Attributes:
        id: 角色ID.
        name: 角色名称 (例如: "管理员", "普通用户").
        description: 角色描述.
        permissions: 角色拥有的权限.
    """
    id = fields.IntField(pk=True, description="角色ID")
    name = fields.CharField(max_length=255, unique=True, description="角色名称")
    description = fields.TextField(null=True, blank=True, description="角色描述")
    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField(
        "fast_admin.Permission",
        related_name="roles",
        # through="role_permission",  # 注意若传递through参数，则需要手动创建中间表
        description="角色拥有的权限"
    )

    def __str__(self):
        return self.name
