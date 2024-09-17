from functools import wraps

from fastapi import status, Depends
from fastapi.requests import Request

from fast_admin.models.user import User
from fast_admin.core.config import settings
from fast_admin.core.exceptions import CustomException


def permission_required_decorator(permission_code: str, permission_type: str = "operation"):
    """
    权限校验装饰器, 此项目使用的依赖注入的方式没有使用装饰器方式

    Args:
        permission_code: 权限代码.
        permission_type: 权限类型，默认为 "operation".

    Returns:
        装饰器函数.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户
            request: Request = kwargs.get("request")
            user: User = request.state.user

            # 如果用户未登录且访问的是白名单内的路由，则允许访问
            if not user and request.url.path in settings.AUTH_WHITELIST:
                return await func(*args, **kwargs)

            if not user:
                raise CustomException(
                    msg="用户未登录",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

            # 检查用户是否拥有该权限或是否是超级管理员
            if user.is_superuser or user.has_permission(permission_code, permission_type):
                return await func(*args, **kwargs)

            raise CustomException(
                msg="无权访问该资源",
                status_code=status.HTTP_403_FORBIDDEN
            )

        return wrapper

    return decorator


async def get_current_user_from_request(request: Request):
    """
    获取当前用户的依赖函数.

    Args:
        request: FastAPI 的 Request 对象.

    Returns:
        User 或 None: 如果请求在白名单中，返回 None，否则返回当前用户.
    """
    # 如果请求路径在白名单中，直接返回 None，表示允许匿名访问
    if request.url.path in settings.AUTH_WHITELIST:
        return None

    # 获取中间件中设置的用户
    user = getattr(request.state, "user", None)
    if not user:
        raise CustomException(
            msg="用户未登录",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return user


def permission_required(permission_code: str, permission_type: str = "operation"):
    """
    权限校验依赖函数.

    Args:
        permission_code: 权限代码.
        permission_type: 权限类型，默认为 "operation".

    Returns:
        依赖注入函数.
    """

    async def verify_permission(user: User = Depends(get_current_user_from_request)):
        # 如果用户为 None，说明在白名单中，直接允许通过
        if user is None:
            return True

        # 检查用户是否拥有该权限或是否是超级管理员
        if user.is_superuser or await user.has_permission(permission_code, permission_type):
            return True

        raise CustomException(
            msg="无权访问该资源",
            status_code=status.HTTP_403_FORBIDDEN
        )

    return verify_permission
