from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class RateLogDTO(BaseModel):
    user_id: int
    rate: Decimal
    subject: Optional[bool] = False
    topic: Optional[bool] = False
    note_subject: Optional[bool] = False
    note_topic: Optional[bool] = False
