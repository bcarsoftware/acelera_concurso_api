from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.enums.enum_category import EnumCategory
from src.enums.enum_status import EnumStatus


class SubjectResponse(BaseModel):
    subject_id: int
    public_tender_id: int
    name: str
    category: EnumCategory
    status: EnumStatus = EnumStatus.INCOMPLETE
    deleted: bool = False
    create_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
