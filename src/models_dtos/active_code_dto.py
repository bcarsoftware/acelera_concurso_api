from typing import Optional

from pydantic import BaseModel


class ActiveCodeDTO(BaseModel):
    secure_code: str
    token: Optional[str] = None
    code: Optional[str] = None
