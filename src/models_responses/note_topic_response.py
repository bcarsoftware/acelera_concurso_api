from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class NoteTopicResponse(BaseModel):
    note_topic_id: int
    topic_id: int
    description: str
    finish: bool = False
    rate_success: Decimal
    deleted: bool = False
    create_at: datetime
    update_at: datetime
