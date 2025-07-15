"""
异常处理模块
此模块内容参考自Kinit项目: https://github.com/vvandk/kinit/blob/master/kinit-api/core/exception.py

此模块包含应用程序的全局异常处理逻辑，包括：

- 定义 CustomException 类，用于自定义异常。
- 定义 register_exception 函数，用于注册全局异常处理函数。
- 定义各种异常处理函数，用于处理不同类型的异常。
"""

from starlette import status
from starlette.exceptions import HTTPException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from tortoise.exceptions import DoesNotExist, IntegrityError, ValidationError as TortoiseValidationError

from fast_admin.core.logger import logger


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


def register_exception(app: FastAPI) -> None:
    """
    注册全局异常处理函数。

    此函数用于注册全局异常处理函数，包括：
    - custom_exception_handler：自定义异常处理函数。
    - http_exception_handler：HTTP 异常处理函数。
    - request_validation_exception_handler：请求验证异常处理函数。
    - tortoise_exception_handler：Tortoise-ORM 异常处理函数。
    - value_exception_handler：值异常处理函数。
    - all_exception_handler：全部异常处理函数。
    """

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException) -> ORJSONResponse:
        """
        自定义异常处理函数。
        """
        logger.error(
            f"请求 {request.method} {request.url} 发生自定义异常: {exc.msg}",
            extra={"状态码": exc.status_code}
        )

        content = {"message": exc.msg}

        return ORJSONResponse(
            status_code=exc.status_code,
            content=content
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> ORJSONResponse:
        """
        HTTP 异常处理函数。

        此函数用于处理 HTTPException 类型的异常，例如 404 Not Found、403 Forbidden 等。
        """
        logger.warning(
            f"请求 {request.method} {request.url} 发生 HTTP 异常: {exc.detail} (状态码: {exc.status_code})"
        )

        return ORJSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
        """
        请求验证异常处理函数。

        此函数用于处理 RequestValidationError 类型的异常，例如请求参数类型错误、缺少必填参数等。
        """
        logger.warning(
            f"请求 {request.method} {request.url} 参数验证失败: {exc.errors()}"
        )

        errors = []
        for error in exc.errors():
            loc = error.get("loc", [])
            msg = error.get("msg", "")
            error_type = error.get("type", "")
            field = '.'.join(str(x) for x in loc[1:]) if len(loc) > 1 else str(loc[0]) if loc else ""

            # 根据不同的错误类型，生成自定义错误消息
            if error_type == "missing":
                formatted_msg = f"缺少必填参数: {field}"
            elif error_type == "value_error":
                formatted_msg = f"参数值错误: {field} - {msg}"
            elif error_type == "type_error":
                formatted_msg = f"参数类型错误: {field} - {msg}"
            else:
                formatted_msg = f"参数错误: {field} - {msg}"

            errors.append(
                {
                    "field": field,
                    "message": formatted_msg,
                    "type": error_type
                }
            )

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "请求参数验证失败",
                "detail": {"errors": errors}
            }
        )

    @app.exception_handler(DoesNotExist)
    async def tortoise_does_not_exist_handler(request: Request, exc: DoesNotExist) -> ORJSONResponse:
        """
        Tortoise-ORM DoesNotExist 异常处理函数。
        """
        logger.warning(f"请求 {request.method} {request.url} 未找到资源: {str(exc)}")

        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "资源不存在"}
        )

    @app.exception_handler(IntegrityError)
    async def tortoise_integrity_error_handler(request: Request, exc: IntegrityError) -> ORJSONResponse:
        """
        Tortoise-ORM IntegrityError 异常处理函数。
        """
        logger.warning(f"请求 {request.method} {request.url} 数据库完整性错误: {str(exc)}")

        # 解析常见的完整性约束错误
        error_msg = str(exc).lower()
        if "unique" in error_msg:
            message = "数据已存在，违反唯一性约束"
        elif "foreign key" in error_msg:
            message = "外键约束错误，关联的数据不存在"
        elif "not null" in error_msg:
            message = "必填字段不能为空"
        else:
            message = "数据完整性错误"

        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": message}
        )

    @app.exception_handler(TortoiseValidationError)
    async def tortoise_validation_error_handler(request: Request, exc: TortoiseValidationError) -> ORJSONResponse:
        """
        Tortoise-ORM ValidationError 异常处理函数。
        """
        logger.warning(f"请求 {request.method} {request.url} 数据库验证错误: {str(exc)}")

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": f"数据验证失败: {str(exc)}"}
        )

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError) -> ORJSONResponse:
        """
        值异常处理函数。

        此函数用于处理 ValueError 类型的异常，例如数据类型转换错误等。
        """
        logger.warning(f"请求 {request.method} {request.url} 数据值错误: {str(exc)}")

        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"数据值错误: {str(exc)}"}
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
        """
        全部异常处理函数。

        此函数用于处理所有未捕获的异常。
        """
        logger.exception(
            f"请求 {request.method} {request.url} 发生未捕获异常: {str(exc)}",
            exc_info=exc
        )

        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "服务器内部错误，请稍后重试"}
        )
