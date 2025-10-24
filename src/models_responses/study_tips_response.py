from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StudyTipsResponse(BaseModel):
    study_tip_id: int
    user_id: int
    name: str
    ai_generate: bool
    description: Optional[str] = None
    deleted: bool = False
    create_at: datetime
    update_at: datetime
