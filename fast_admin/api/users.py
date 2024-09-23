from typing import List

from fastapi import APIRouter, status, Depends
from tortoise.exceptions import IntegrityError

from fast_admin.models.role import Role
from fast_admin.models.user import User, pwd_context
from fast_admin.core.exceptions import CustomException
from fast_admin.schemas.user import User as UserSchema, UserCreate, UserUpdate
from fast_admin.core.dependencies import permission_required, get_current_user_from_request

router = APIRouter()


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_required(permission_code="user:create"))])
async def create_user(user_in: UserCreate):
    """
    创建新的用户.

    Args:
        user_in: 创建用户的请求数据.

    Returns:
        创建的用户信息.

    Raises:
        CustomException: 如果用户名已存在，则抛出 HTTP 400 错误.
    """
    try:
        # 创建用户
        user = await User.create(
            username=user_in.username,
            password_hash=pwd_context.hash(user_in.password),
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser
        )

        # 如果有角色，分配角色
        if user_in.role_ids:
            roles = await Role.filter(id__in=user_in.role_ids).all()  # 批量获取角色
            if roles:
                await user.roles.add(*roles)  # 分配角色

    except IntegrityError:
        raise CustomException(
            msg="用户名已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # 获取创建后的用户及其角色
    return await User.get(id=user.id).prefetch_related("roles__permissions")


@router.get("/", response_model=List[UserSchema], dependencies=[Depends(permission_required(permission_code="user:list"))])
async def list_users():
    """
    获取所有用户列表.

    Returns:
        所有用户的列表.
    """
    users = await User.all().prefetch_related("roles__permissions")
    return users


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(current_user: User = Depends(get_current_user_from_request)):
    """
    获取当前登录用户的信息.
    """
    return current_user


@router.get("/{user_id}", response_model=UserSchema, dependencies=[Depends(permission_required(permission_code="user:read"))])
async def get_user(user_id: int):
    """
    根据 ID 获取用户信息.

    Args:
        user_id: 用户 ID.

    Returns:
        用户信息.

    Raises:
        HTTPException: 如果用户不存在，则抛出 HTTP 404 错误.
    """
    user = await User.get_or_none(id=user_id).prefetch_related("roles__permissions")
    if not user:
        raise CustomException(
            msg="用户不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return user


@router.put("/{user_id}", response_model=UserSchema, dependencies=[Depends(permission_required(permission_code="user:update"))])
async def update_user(user_id: int, user_in: UserUpdate):
    """
    更新用户信息
    注意暂不提供用户自己修改信息的功能，需要对应角色的权限才能修改用户信息，若使用此接口修改用户信息，会出现越权行为。

    Args:
        user_id: 用户 ID.
        user_in: 更新用户的请求数据.

    Returns:
        更新后的用户信息.

    Raises:
        HTTPException: 如果用户不存在，则抛出 HTTP 404 错误.
                  如果用户名已存在，则抛出 HTTP 400 错误.
    """
    user = await User.get_or_none(id=user_id)
    if not user:
        raise CustomException(
            msg="用户不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        for key, value in user_in.model_dump(exclude_unset=True, exclude={"role_ids"}).items():
            setattr(user, key, value)
        await user.save()

        if user_in.role_ids is not None:
            await user.roles.clear()
            await user.roles.add(
                *[await Role.get(id=role_id) for role_id in user_in.role_ids]
            )
    except IntegrityError:
        raise CustomException(
            msg="用户名已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return await User.get(id=user.id).prefetch_related("roles__permissions")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(permission_required(permission_code="user:delete"))])
async def delete_user(user_id: int):
    """
    删除用户.

    Args:
        user_id: 用户 ID.

    Raises:
        HTTPException: 如果用户不存在，则抛出 HTTP 404 错误.
    """
    user = await User.get_or_none(id=user_id)
    if not user:
        raise CustomException(
            msg="用户不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
    await user.delete()
    return {"message": "删除成功"}
