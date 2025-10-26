from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class NoteSubjectDTO(BaseModel):
    subject_id: int
    name: str
    description: str
    finish: bool = False
    rate_success: Optional[Decimal] = None
    deleted: bool = False
