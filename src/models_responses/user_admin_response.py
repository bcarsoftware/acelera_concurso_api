from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserAdminResponse(BaseModel):
    user_admin_id: int
    full_name: str
    username: str
    password: str
    create_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
