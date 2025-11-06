from pydantic import BaseModel


class PublicTenderBoardDTO(BaseModel):
    user_admin_id: int
    sail: str
    name: str
