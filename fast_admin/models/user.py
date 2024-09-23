from passlib.context import CryptContext

from tortoise import fields
from starlette import status

from fast_admin.core.exceptions import CustomException
from fast_admin.models.base import BaseModel
from .role import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """
    用户模型

    Attributes:
        id: 用户ID，主键.
        username: 用户名.
        password_hash: 密码哈希值.
        is_active: 用户是否激活.
        is_superuser: 是否是超级管理员权限.
        roles: 用户拥有的角色.
    """
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=255, unique=True, description="用户名")
    password_hash = fields.CharField(max_length=128, description="密码哈希值")
    is_active = fields.BooleanField(default=True, description="用户是否激活")
    is_superuser = fields.BooleanField(default=False, description="是否是超级管理员权限")
    roles: fields.ManyToManyRelation[Role] = fields.ManyToManyField(
        "fast_admin.Role",
        related_name="users",
        # through="user_role",
        description="用户拥有的角色"
    )

    def __str__(self):
        return self.username

    async def has_permission(self, permission_code: str, permission_type: str = "operation") -> bool:
        """
        检查用户是否拥有指定权限.

        Args:
            permission_code: 权限代码.
            permission_type: 权限类型.

        Returns:
            如果用户拥有该权限，则返回 True，否则返回 False.
        """
        # 超级管理员拥有所有权限
        if self.is_superuser:
            return True

        for role in await self.roles:
            for permission in await role.permissions:
                if permission.code == permission_code and permission.type == permission_type:
                    return True
        return False

    def verify_password(self, password: str):
        """
        验证密码是否正确.

        Args:
            password: 明文密码.

        Returns:
            如果密码正确，则返回 True，否则返回 False.
        """
        return pwd_context.verify(password, self.password_hash)


async def get_user_by_username(username: str):
    """
    根据用户名获取用户信息.

    Args:
        username: 用户名.

    Returns:
        用户信息.

    Raises:
        CustomException: 如果用户不存在.
    """
    user = await User.filter(username=username).prefetch_related('roles__permissions').first()
    if not user:
        raise CustomException(msg="用户不存在", status_code=status.HTTP_404_NOT_FOUND)
    return user
