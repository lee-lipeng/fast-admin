from typing import List, Optional

from pydantic import BaseModel

from .permission import Permission


class RoleCreate(BaseModel):
    """
    创建角色时的请求数据模型.

    Attributes:
        name: 角色名称.
        description: 角色描述 (可选).
        permission_ids: 权限 ID 列表 (可选).
    """
    name: str
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None


class RoleUpdate(BaseModel):
    """
    更新角色时的请求数据模型.

    Attributes:
        name: 角色名称 (可选).
        description: 角色描述 (可选).
        permission_ids: 权限 ID 列表 (可选).
    """
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None


class Role(BaseModel):
    """
    角色响应数据模型.

    Attributes:
        id: 角色 ID.
        name: 角色名称.
        description: 角色描述 (可选).
        permissions: 权限列表 (可选).
    """
    id: int
    name: str
    description: Optional[str] = None
    permissions: Optional[List[Permission]] = None

    class Config:
        from_attributes = True
