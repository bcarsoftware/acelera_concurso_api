from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.enums.enum_status import EnumStatus


class TopicResponse(BaseModel):
    topic_id: int
    subject_id: int
    name: str
    description: Optional[str] = None
    status: EnumStatus
    fulfillment: Optional[Decimal] = None
    deleted: bool = False
    create_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
