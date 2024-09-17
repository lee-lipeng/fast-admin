from typing import List, Optional

from pydantic import BaseModel

from .role import Role


class UserBase(BaseModel):
    """
    用户基础数据模型.

    Attributes:
        username: 用户名.
        is_active: 用户是否激活.
        is_superuser: 是否是超级管理员.
    """
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    """
    创建用户时的请求数据模型.

    Attributes:
        password: 密码.
        role_ids: 角色 ID 列表 (可选).
    """
    password: str
    role_ids: Optional[List[int]] = None


class UserLogin(BaseModel):
    """
    用户登录数据模型.

    Attributes:
        username: 用户名.
        password: 密码.
    """
    username: str
    password: str


class UserUpdate(UserBase):
    """
    更新用户时的请求数据模型.

    Attributes:
        role_ids: 角色 ID 列表 (可选).
    """
    role_ids: Optional[List[int]] = None


class User(UserBase):
    """
    用户响应数据模型.

    Attributes:
        id: 用户 ID.
        roles: 角色列表 (可选).
    """
    id: int
    roles: Optional[List[Role]] = None

    class Config:
        from_attributes = True
