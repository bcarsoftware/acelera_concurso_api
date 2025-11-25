from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.enums.enum_status import EnumStatus


class TopicDTO(BaseModel):
    subject_id: int
    name: str
    description: Optional[str] = None
    fulfillment: Optional[Decimal] = None
    status: EnumStatus
    law_link: Optional[str] = None
    deleted: bool = False
