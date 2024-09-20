from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Query, Depends

from fast_admin.core.pagination import paginate, Pagination
from fast_admin.models.logs import Log
from fast_admin.schemas.logs import LogOut
from fast_admin.core.dependencies import permission_required

router = APIRouter()


@router.get("/", response_model=Pagination[LogOut], dependencies=[Depends(permission_required(permission_code="log:read"))])
async def get_logs(
        level: Optional[str] = Query(None, description="日志级别"),
        process: Optional[str] = Query(None, description="进程信息"),
        thread: Optional[str] = Query(None, description="线程信息"),
        logger_name: Optional[str] = Query(None, description="记录器名称"),
        module: Optional[str] = Query(None, description="模块名称"),
        function_name: Optional[str] = Query(None, description="函数名称"),
        message: Optional[str] = Query(None, description="日志消息"),
        exception: Optional[str] = Query(None, description="异常信息"),
        start_time: Optional[datetime] = Query(None, description="起始时间"),
        end_time: Optional[datetime] = Query(None, description="结束时间"),
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
        order_by: Optional[str] = Query(None, description="排序字段 (例如：timestamp, level)"),
        order: Optional[str] = Query("asc", description="排序方式 (asc 或 desc)")
):
    """
    获取日志列表。

    支持筛选和排序，并提供分页功能。
    """
    query = Log.all()

    filters = {
        "level": level,
        "process": process,
        "thread": thread,
        "logger_name": logger_name,
        "module": module,
        "function_name": function_name
    }
    # 精确搜索
    for field, value in filters.items():
        if value is not None:
            query = query.filter(**{field: value})

    # 模糊搜索
    if message:
        query = query.filter(message__icontains=message)
    if exception:
        query = query.filter(exception__icontains=exception)

    # 时间范围过滤
    if start_time:
        query = query.filter(timestamp__gte=start_time)
    if end_time:
        query = query.filter(timestamp__lte=end_time)

    # 排序
    if order_by:
        order_by_field = f"-{order_by}" if order.lower() == "desc" else order_by
        query = query.order_by(order_by_field)

    # 分页
    return await paginate(query, page, page_size)
