from datetime import datetime, timedelta, timezone
from typing import Any, Union

from fastapi import status
from jwt import encode, decode, PyJWTError
from pydantic import ValidationError, BaseModel

from fast_admin.core.config import settings
from fast_admin.models.user import User, get_user_by_username
from fast_admin.core.exceptions import CustomException


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    创建访问令牌.

    Args:
        subject: 令牌主题，通常是用户名.
        expires_delta: 令牌过期时间，如果为 None，则使用默认过期时间.

    Returns:
        访问令牌.
    """
    if expires_delta:
        expire = datetime.now(timezone(settings.TIMEZONE)) + expires_delta
    else:
        expire = datetime.now(timezone(settings.TIMEZONE)) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    创建刷新令牌.

    Args:
        subject: 令牌主题，通常是用户名.
        expires_delta: 令牌过期时间，如果为 None，则使用默认过期时间.

    Returns:
        刷新令牌.
    """
    if expires_delta:
        expire = datetime.now(timezone(settings.TIMEZONE)) + expires_delta
    else:
        expire = datetime.now(timezone(settings.TIMEZONE)) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str) -> User:
    """
    获取当前用户.

    Args:
        token: 访问令牌.

    Returns:
        当前用户信息.

    Raises:
        CustomException: 如果令牌无效、用户不存在或令牌类型错误.
    """
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.type != "access":
            raise CustomException(
                msg="令牌类型错误",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    except (PyJWTError, ValidationError):
        raise CustomException(
            msg="令牌无效",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        user = await get_user_by_username(username=token_data.sub)
    except CustomException as e:
        raise e
    return user


class TokenPayload(BaseModel):
    """
    令牌负载数据模型.

    Attributes:
        exp: 令牌过期时间.
        sub: 令牌主题，通常是用户名.
        type: 令牌类型.
    """
    exp: datetime
    sub: str
    type: str
