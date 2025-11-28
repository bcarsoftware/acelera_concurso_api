from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.enums.enum_category import EnumCategory
from src.enums.enum_status import EnumStatus


class SubjectDTO(BaseModel):
    public_tender_id: int
    name: str
    category: EnumCategory
    fulfillment: Optional[Decimal] = None
    status: EnumStatus = EnumStatus.INCOMPLETE
    deleted: bool = False
