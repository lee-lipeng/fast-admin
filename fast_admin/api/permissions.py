from typing import List

from fastapi import APIRouter, Depends, status
from tortoise.exceptions import IntegrityError

from fast_admin.core.exceptions import CustomException
from fast_admin.models.permission import Permission
from fast_admin.schemas.permission import Permission as PermissionSchema, PermissionCreate, PermissionUpdate
from fast_admin.core.dependencies import permission_required

router = APIRouter()


@router.post("/", response_model=PermissionSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_required(permission_code="permission:create"))])
async def create_permission(permission_in: PermissionCreate):
    """
    创建新的权限.

    Args:
        permission_in: 权限创建数据.

    Returns:
        创建的权限信息.

    Raises:
        CustomException:
            - 如果权限名称或代码已存在，则抛出 HTTP 400 错误.
    """
    try:
        permission = await Permission.create(**permission_in.model_dump())
    except IntegrityError:
        raise CustomException(
            msg="权限名称或代码已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return permission


@router.get("/", response_model=List[PermissionSchema], dependencies=[Depends(permission_required(permission_code="permission:list", permission_type="page"))])
async def list_permissions():
    """
    获取所有权限列表.

    Returns:
        所有权限的列表.
    """
    permissions = await Permission.all()
    return permissions


@router.get("/{permission_id}", response_model=PermissionSchema, dependencies=[Depends(permission_required(permission_code="permission:read"))])
async def get_permission(permission_id: int):
    """
    根据 ID 获取权限信息.

    Args:
        permission_id: 权限 ID.

    Returns:
        权限信息.

    Raises:
        CustomException:
            - 如果权限不存在，则抛出 HTTP 404 错误.
    """
    permission = await Permission.get_or_none(id=permission_id)
    if not permission:
        raise CustomException(
            msg="权限不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return permission


@router.put("/{permission_id}", response_model=PermissionSchema, dependencies=[Depends(permission_required(permission_code="permission:update"))])
async def update_permission(permission_id: int, permission_in: PermissionUpdate):
    """
    更新权限信息.

    Args:
        permission_id: 权限 ID.
        permission_in: 权限更新数据.

    Returns:
        更新后的权限信息.

    Raises:
        CustomException:
            - 如果权限不存在，则抛出 HTTP 404 错误.
            - 如果权限名称或代码已存在，则抛出 HTTP 400 错误.
    """
    permission = await Permission.get_or_none(id=permission_id)
    if not permission:
        raise CustomException(
            msg="权限不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        for key, value in permission_in.model_dump(exclude_unset=True).items():
            setattr(permission, key, value)
        await permission.save()
    except IntegrityError:
        raise CustomException(
            msg="权限名称或代码已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return permission


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(permission_required(permission_code="permission:delete"))])
async def delete_permission(permission_id: int):
    """
    删除权限.

    Args:
        permission_id: 权限 ID.

    Raises:
        CustomException:
            - 如果权限不存在，则抛出 HTTP 404 错误.
    """
    permission = await Permission.get_or_none(id=permission_id)
    if not permission:
        raise CustomException(
            msg="权限不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
    await permission.delete()
