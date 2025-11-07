from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.enums.enum_level import EnumLevel


class PublicTenderResponse(BaseModel):
    public_tender_id: int
    user_id: int
    tender_name: str
    tender_board: str
    tender_level: EnumLevel
    institute: str
    work_title: str
    notice_link: Optional[str] = None
    tender_date: Optional[date] = None
    deleted: bool = False
    create_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
