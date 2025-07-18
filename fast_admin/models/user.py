from tortoise import fields
from starlette import status
from datetime import datetime
from zoneinfo import ZoneInfo

from fast_admin.core.config import settings
from fast_admin.core.exceptions import CustomException
from fast_admin.models.base import BaseModel
from fast_admin.models.role import Role


class User(BaseModel):
    """
    用户模型

    Attributes:
        id: 用户ID，主键.
        username: 用户名.
        password_hash: 密码哈希值.
        is_active: 用户是否激活.
        is_superuser: 是否是超级管理员权限.
        last_login: 最后登录时间.
        roles: 用户拥有的角色.
    """
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=255, unique=True, description="用户名")
    password_hash = fields.CharField(max_length=128, description="密码哈希值")
    is_active = fields.BooleanField(default=True, description="用户是否激活")
    is_superuser = fields.BooleanField(default=False, description="是否是超级管理员权限")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")
    roles: fields.ManyToManyRelation[Role] = fields.ManyToManyField(
        "fast_admin.Role",
        related_name="users",
        description="用户拥有的角色"
    )

    def __str__(self) -> str:
        """返回用户名作为字符串表示"""
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

    def verify_password(self, password: str) -> bool:
        """
        验证密码是否正确.

        Args:
            password: 明文密码.

        Returns:
            bool: 如果密码正确，则返回 True，否则返回 False.
        """
        from fast_admin.core.security import verify_password
        return verify_password(password, self.password_hash)

    async def update_last_login(self) -> None:
        """更新用户最后登录时间"""
        self.last_login = datetime.now(ZoneInfo(settings.TIMEZONE))
        await self.save(update_fields=["last_login"])


async def get_user_by_username(username: str) -> User:
    """
    根据用户名获取用户信息.

    Args:
        username: 用户名.

    Returns:
        User: 用户信息.

    Raises:
        CustomException: 如果用户不存在.
    """
    user = await User.filter(username=username).prefetch_related('roles__permissions').first()
    if not user:
        raise CustomException(msg="用户不存在", status_code=status.HTTP_404_NOT_FOUND)
    return user


async def get_user_by_id(user_id: int) -> User:
    """
    根据ID获取用户信息.

    Args:
        user_id: 用户ID.

    Returns:
        User: 用户信息.

    Raises:
        CustomException: 如果用户不存在.
    """
    user = await User.filter(id=user_id).prefetch_related('roles__permissions').first()
    if not user:
        raise CustomException(msg="用户不存在", status_code=status.HTTP_404_NOT_FOUND)
    return user
