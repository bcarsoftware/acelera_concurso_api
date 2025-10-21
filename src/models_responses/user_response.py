from datetime import date, datetime

from pydantic import BaseModel

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
    update_at: datetime
