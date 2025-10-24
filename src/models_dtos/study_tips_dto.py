from typing import Optional

from pydantic import BaseModel


class StudyTipsDTO(BaseModel):
    user_id: int
    name: str
    ai_generate: bool
    description: Optional[str] = None
    deleted: bool = False
