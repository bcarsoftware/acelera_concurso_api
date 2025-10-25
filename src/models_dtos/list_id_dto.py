from typing import List

from pydantic import BaseModel


class ListIDDTO(BaseModel):
    ids: List[int] = []
