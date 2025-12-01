from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class RateLogDTO(BaseModel):
    user_id: int
    rate: Decimal
    public_tender_id: int
    subject: Optional[bool] = False
    topic: Optional[bool] = False
    note_subject: Optional[bool] = False
    note_topic: Optional[bool] = False
