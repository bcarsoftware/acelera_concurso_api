from typing import Optional

from pydantic import BaseModel


class UserAdminDTO(BaseModel):
    full_name: str
    username: str
    password: str
    new_password: Optional[str] = None
