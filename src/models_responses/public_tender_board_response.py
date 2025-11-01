from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PublicTenderBoardResponse(BaseModel):
    public_tender_board_id: int
    sail: str
    name: str
    create_at: datetime
    update_at: Optional[datetime] = None
