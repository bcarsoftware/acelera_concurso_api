from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class NoteTopicDTO(BaseModel):
    topic_id: int
    description: str
    finish: bool = False
    rate_success: Optional[Decimal] = None
    deleted: bool = False
