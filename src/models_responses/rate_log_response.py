from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RateLogResponse(BaseModel):
    rate_log_id: int
    user_id: int
    rate: Decimal
    subject: Optional[bool] = False
    topic: Optional[bool] = False
    note_subject: Optional[bool] = False
    note_topic: Optional[bool] = False
    create_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
