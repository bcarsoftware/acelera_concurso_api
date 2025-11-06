from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.enums.enum_gender import EnumGender


class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    date_born: date
    gender: EnumGender
    username: str
    email: str
    points: int = 0
    deleted: bool = False
    create_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
