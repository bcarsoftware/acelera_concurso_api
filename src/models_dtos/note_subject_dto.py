from decimal import Decimal

from pydantic import BaseModel


class NoteSubjectDto(BaseModel):
    subject_id: int
    description: str
    finish: bool = False
    rate_success: Decimal
    deleted: bool = False
