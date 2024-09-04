from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LogOut(BaseModel):
    """日志输出模型"""

    id: int
    level: str
    message: str
    timestamp: datetime
    logger_name: Optional[str] = None
    module: Optional[str] = None
    line_no: Optional[int] = None
    function_name: Optional[str] = None
    exception: Optional[str] = None

    class Config:
        orm_mode = True
