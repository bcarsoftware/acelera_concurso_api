from datetime import date
from typing import Optional

from pydantic import BaseModel


class PublicTenderDTO(BaseModel):
    user_id: int
    tender_name: str
    tender_board: str
    work_tile: str
    institute: Optional[str] = None
    notice_link: Optional[str] = None
    tender_date: Optional[date] = None
    deleted: bool = False
