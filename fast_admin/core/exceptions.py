from starlette import status
from starlette.exceptions import HTTPException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from fast_admin.core.logger import logger

"""
异常处理模块
此模块内容参考自Kinit项目: https://github.com/vvandk/kinit/blob/master/kinit-api/core/exception.py

此模块包含应用程序的全局异常处理逻辑，包括：

- 定义 CustomException 类，用于自定义异常。
- 定义 register_exception 函数，用于注册全局异常处理函数。
- 定义各种异常处理函数，用于处理不同类型的异常。

"""


class CustomException(Exception):
    """
    自定义异常类。

    此类继承自 Exception，用于自定义异常，包括：

    - msg: 异常消息。
    - status_code: HTTP 状态码。

    """

    def __init__(
            self,
            msg: str,
            status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.msg = msg
        self.status_code = status_code


def register_exception(app: FastAPI):
    """
    注册全局异常处理函数。

    此函数用于注册全局异常处理函数，包括：
    - custom_exception_handler：自定义异常处理函数。
    - http_exception_handler：HTTP 异常处理函数。
    - request_validation_exception_handler：请求验证异常处理函数。
    - value_exception_handler：值异常处理函数。
    - all_exception_handler：全部异常处理函数。
    """

    @app.exception_handler(CustomException)
    async def custom_exception_handler(_: Request, exc: CustomException):
        """
        自定义异常
        """
        logger.exception(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.msg}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        """
        HTTP 异常处理函数。

        此函数用于处理 HTTPException 类型的异常，例如 404 Not Found、403 Forbidden 等。
        """
        logger.exception(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(_: Request, exc: RequestValidationError):
        """
        请求验证异常处理函数。

        此函数用于处理 RequestValidationError 类型的异常，例如请求参数类型错误、缺少必填参数等。
        """
        logger.exception(exc)

        error_detail = exc.errors()[0]  # 获取第一个错误的详细信息
        loc = error_detail.get("loc")  # 获取错误参数的位置
        msg = error_detail.get("msg").lower()  # 将错误消息转换为小写
        error_type = error_detail.get("type")  # 错误类型
        field = '.'.join(str(x) for x in loc[1:]) if loc else ""

        # 根据不同的错误类型，生成自定义错误消息
        if error_type == "missing":
            msg = f"请求失败，缺少必填项: {field}！"
        else:
            msg = f"请求参数错误: {field} {msg}"

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": msg}
        )

    @app.exception_handler(ValueError)
    async def value_exception_handler(_: Request, exc: ValueError):
        """
        值异常处理函数。

        此函数用于处理 ValueError 类型的异常，例如数据类型转换错误等。
        """
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.__str__()}
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(_: Request, exc: Exception):
        """
        全部异常处理函数。

        此函数用于处理所有未捕获的异常。
        """
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "接口异常，请稍后重试!"}
        )
