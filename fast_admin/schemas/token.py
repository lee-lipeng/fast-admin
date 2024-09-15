from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    """
    令牌数据模型.

    Attributes:
        access_token: 访问令牌.
        refresh_token: 刷新令牌.
        token_type: 令牌类型.
    """
    access_token: str
    refresh_token: str
    token_type: str


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
