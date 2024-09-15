from pydantic import BaseModel


class PermissionCreate(BaseModel):
    """
    创建权限时的请求数据模型.
    """
    name: str
    code: str
    type: str
    description: str | None = None


class PermissionUpdate(BaseModel):
    """
    更新权限时的请求数据模型.
    """
    name: str | None = None
    code: str | None = None
    type: str | None = None
    description: str | None = None


class Permission(BaseModel):
    """
    权限响应数据模型.
    """
    id: int
    name: str
    code: str
    type: str
    description: str | None = None

    class Config:
        from_attributes = True
