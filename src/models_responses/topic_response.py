from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.enums.enum_status import EnumStatus


class TopicResponse(BaseModel):
    topic_id: int
    subject_id: int
    name: str
    fulfillment: Decimal
    status: EnumStatus
    deleted: bool = False
    create_at: datetime
    update_at: datetime
