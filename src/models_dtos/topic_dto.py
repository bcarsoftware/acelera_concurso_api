from decimal import Decimal

from pydantic import BaseModel

from src.enums.enum_status import EnumStatus


class TopicDTO(BaseModel):
    subject_id: int
    name: str
    fulfillment: Decimal
    status: EnumStatus
    deleted: bool = False
