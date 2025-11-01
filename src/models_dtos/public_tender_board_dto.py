from pydantic import BaseModel


class PublicTenderBoardDTO(BaseModel):
    sail: str
    name: str
