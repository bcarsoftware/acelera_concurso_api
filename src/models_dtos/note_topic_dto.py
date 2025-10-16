from decimal import Decimal

from pydantic import BaseModel


class NoteTopicDTO(BaseModel):
    topic_id: int
    description: str
    finish: bool = False
    rate_success: Decimal
    deleted: bool = False
