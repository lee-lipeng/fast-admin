from typing import TypeVar, Generic
from pydantic import BaseModel
from fastapi import Query
from tortoise.queryset import QuerySet

ModelType = TypeVar("ModelType")


class Pagination(BaseModel, Generic[ModelType]):
    """分页结果模型"""
    items: list[ModelType]
    total: int
    page: int
    page_size: int


async def paginate(
        query: QuerySet[ModelType],
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
) -> Pagination[ModelType]:
    """
    对查询结果进行分页

    Args:
        query: Tortoise-ORM 查询集
        page: 页码
        page_size: 每页数量

    Returns:
        Pagination 对象，包含分页后的结果
    """
    total: int = await query.count()
    items: list = await query.offset((page - 1) * page_size).limit(page_size)

    return Pagination(items=items, total=total, page=page, page_size=page_size)
