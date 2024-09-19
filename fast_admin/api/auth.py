from datetime import timedelta

from fastapi import APIRouter, Body, status
from jwt import decode, PyJWTError
from pydantic import ValidationError

from fast_admin.core.config import settings
from fast_admin.core.exceptions import CustomException
from fast_admin.core.security import (
    create_access_token,
    create_refresh_token,
)
from fast_admin.models.user import get_user_by_username
from fast_admin.schemas.token import Token, TokenPayload
from fast_admin.schemas.user import UserLogin

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(user_in: UserLogin = Body(...)):
    """
    用户登录 API 接口.

    Args:
        user_in: 用户登录信息.

    Returns:
        访问令牌和刷新令牌.

    Raises:
        CustomException: 如果用户名或密码错误，则抛出 HTTP 401 错误.
    """
    user = await get_user_by_username(user_in.username)
    if not user or not user.verify_password(user_in.password):
        raise CustomException(
            msg="用户名或密码错误",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    new_access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        subject=user.username, expires_delta=refresh_token_expires
    )

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str = Body(...)):
    """
    刷新令牌 API 接口.

    Args:
        refresh_token: 刷新令牌.

    Returns:
        新的访问令牌和刷新令牌.

    Raises:
        CustomException: 如果刷新令牌无效，则抛出 HTTP 401 错误.
    """
    try:
        payload = decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.type != "refresh":
            raise CustomException(
                msg="令牌类型错误",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        # 获取用户信息
        user = await get_user_by_username(username=token_data.sub)
    except (PyJWTError, ValidationError):
        raise CustomException(
            msg="令牌无效",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    new_access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        subject=user.username, expires_delta=refresh_token_expires
    )

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
