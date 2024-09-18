from typing import List

from fastapi import APIRouter, status, Depends
from tortoise.exceptions import IntegrityError

from fast_admin.models.permission import Permission
from fast_admin.core.exceptions import CustomException
from fast_admin.models.role import Role
from fast_admin.schemas.role import Role as RoleSchema, RoleCreate, RoleUpdate
from fast_admin.core.dependencies import permission_required

router = APIRouter()


@router.post("/", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
async def create_role(role_in: RoleCreate):
    """
    创建新的角色.

    Args:
        role_in: 创建角色的请求数据.

    Returns:
        创建的角色信息.

    Raises:
        HTTPException: 如果角色名称已存在，则抛出 HTTP 400 错误.
    """
    try:
        role = await Role.create(**role_in.model_dump(exclude={"permission_ids"}))
        if role_in.permission_ids:
            await role.permissions.add(
                *[
                    await Permission.get(id=permission_id)
                    for permission_id in role_in.permission_ids
                ]
            )
    except IntegrityError:
        raise CustomException(
            msg="角色名称已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return await Role.get(id=role.id).prefetch_related("permissions")


@router.get("/", response_model=List[RoleSchema], dependencies=[Depends(permission_required(permission_code="role:list"))])
async def list_roles():
    """
    获取所有角色列表.

    Returns:
        所有角色的列表.
    """
    roles = await Role.all().prefetch_related("permissions")
    return roles


@router.get("/{role_id}", response_model=RoleSchema, dependencies=[Depends(permission_required(permission_code="role:read"))])
async def get_role(role_id: int):
    """
    根据 ID 获取角色信息.

    Args:
        role_id: 角色 ID.

    Returns:
        角色信息.

    Raises:
        HTTPException: 如果角色不存在，则抛出 HTTP 404 错误.
    """
    role = await Role.get_or_none(id=role_id).prefetch_related("permissions")
    if not role:
        raise CustomException(
            msg="角色不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return role


@router.put("/{role_id}", response_model=RoleSchema, dependencies=[Depends(permission_required(permission_code="role:update"))])
async def update_role(role_id: int, role_in: RoleUpdate):
    """
    更新角色信息.

    Args:
        role_id: 角色 ID.
        role_in: 更新角色的请求数据.

    Returns:
        更新后的角色信息.

    Raises:
        HTTPException: 如果角色不存在，则抛出 HTTP 404 错误.
                  如果角色名称已存在，则抛出 HTTP 400 错误.
    """
    role = await Role.get_or_none(id=role_id)
    if not role:
        raise CustomException(
            msg="角色不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        for key, value in role_in.model_dump(exclude_unset=True, exclude={"permission_ids"}).items():
            setattr(role, key, value)
        await role.save()

        if role_in.permission_ids is not None:
            await role.permissions.clear()
            await role.permissions.add(
                *[
                    await Permission.get(id=permission_id)
                    for permission_id in role_in.permission_ids
                ]
            )

    except IntegrityError:
        raise CustomException(
            msg="角色名称已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return await Role.get(id=role.id).prefetch_related("permissions")


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(permission_required(permission_code="role:delete"))])
async def delete_role(role_id: int):
    """
    删除角色.

    Args:
        role_id: 角色 ID.

    Raises:
        HTTPException: 如果角色不存在，则抛出 HTTP 404 错误.
    """
    role = await Role.get_or_none(id=role_id)
    if not role:
        raise CustomException(
            msg="角色不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
    await role.delete()
