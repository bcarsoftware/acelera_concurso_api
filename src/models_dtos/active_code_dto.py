from typing import Optional

from pydantic import BaseModel


class ActiveCodeDTO(BaseModel):
    secure_code: str
    token: str
    code: Optional[str] = None
