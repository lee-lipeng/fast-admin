from typing import TypeVar, Type, Dict, List, Optional
from pydantic import BaseModel
from fastapi import Query
from tortoise.queryset import QuerySet
from fastapi.encoders import jsonable_encoder

T = TypeVar('T', bound=BaseModel)


async def paginate(
        query: QuerySet,
        schema: Optional[Type[T]] = None,
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
) -> Dict[str, any]:
    """
    通用分页函数，支持Tortoise ORM查询集的分页和可选的Pydantic模型序列化。

    参数:
    - query: Tortoise ORM 查询集
    - schema: 可选的 Pydantic 模型类，用于数据序列化
    - page: 当前页码，默认为1
    - page_size: 每页项目数，默认为10

    返回:
    包含分页数据的字典，格式为:
    {
        "items": 序列化后的项目列表,
        "total": 总项目数,
        "page": 当前页码,
        "page_size": 每页项目数
    }
    """
    total: int = await query.count()
    items: List = await query.offset((page - 1) * page_size).limit(page_size)

    # 如果提供了schema，使用它来序列化项目
    if schema:
        items = [schema.model_validate(item) for item in items]

    # 使用jsonable_encoder确保所有数据都是JSON可序列化的
    serialized_items: List = jsonable_encoder(items)

    return {
        "items": serialized_items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }
