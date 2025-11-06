from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NoteTopicResponse(BaseModel):
    note_topic_id: int
    topic_id: int
    name: str
    description: str
    finish: bool = False
    rate_success: Optional[Decimal] = None
    deleted: bool = False
    create_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
