from fastapi import status as http_status
from fastapi.responses import ORJSONResponse
from typing import Any, Optional

from pydantic import BaseModel


def success_response(
        data: Any = None,
        message: str = "Success",
        code: int = http_status.HTTP_200_OK,
        http_status_code: int = http_status.HTTP_200_OK
):
    """
    成功响应的封装，用于返回成功结果。

    :param data: 返回的实际数据
    :param message: 成功消息，默认值为 'Success'
    :param code: 自定义响应码，默认值为 HTTP 200
    :param http_status_code: HTTP 状态码，默认值为 HTTP 200
    :return: 统一格式的成功响应
    """
    return ORJSONResponse(
        status_code=http_status_code,
        content={
            'code': code,
            'message': message,
            'data': data,
        }
    )


def error_response(
        message: str = "Error",
        code: int = http_status.HTTP_400_BAD_REQUEST,
        data: Optional[Any] = None,
        http_status_code: int = http_status.HTTP_200_OK
):
    """
    错误响应的封装，用于返回错误结果。

    :param message: 错误消息，默认值为 'Error'
    :param code: 自定义响应码，默认值为 HTTP 400
    :param data: 可选的返回数据，默认为 None
    :param http_status_code: HTTP 状态码，默认值为 HTTP 200
    :return: 统一格式的错误响应
    """
    return ORJSONResponse(
        status_code=http_status_code,
        content={
            'code': code,
            'message': message,
            'data': data,
        }
    )
