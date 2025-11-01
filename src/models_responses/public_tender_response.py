from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class PublicTenderResponse(BaseModel):
    public_tender_id: int
    user_id: int
    tender_name: str
    tender_board: str
    work_tile: str
    institute: str
    notice_link: Optional[str] = None
    tender_date: Optional[date] = None
    deleted: bool = False
    create_at: datetime
    update_at: Optional[datetime] = None
