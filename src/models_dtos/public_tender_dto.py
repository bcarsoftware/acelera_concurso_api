from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.enums.enum_level import EnumLevel


class PublicTenderDTO(BaseModel):
    user_id: int
    tender_name: str
    tender_board: str
    tender_level: EnumLevel
    institute: str
    work_title: str
    notice_link: Optional[str] = None
    tender_date: Optional[date] = None
    deleted: bool = False
