from datetime import date

from pydantic import BaseModel

from src.enums.enum_gender import EnumGender


class UserDTO(BaseModel):
    first_name: str
    last_name: str
    date_born: date
    gender: EnumGender
    username: str
    email: str
    password: str
    points: int = 0
    deleted: bool = False
