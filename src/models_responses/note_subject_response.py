from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class NoteSubjectResponse(BaseModel):
    note_subject_id: int
    subject_id: int
    description: str
    finish: bool = False
    rate_success: Decimal
    deleted: bool = False
    create_at: datetime
    update_at: datetime
