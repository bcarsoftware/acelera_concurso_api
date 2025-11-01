from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine
from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_admin_dto import UserAdminDTO
from src.models_responses.user_admin_response import UserAdminResponse


class UserAdminRepositoryInterface(ABC):
    @abstractmethod
    async def create_user_admin(self, user_admin_dto: UserAdminDTO) -> UserAdminResponse:
        pass

    @abstractmethod
    async def login_user_admin(self, user_admin_dto: LoginDTO) -> UserAdminResponse:
        pass

    @abstractmethod
    async def update_user_admin(self, user_admin_dto: UserAdminDTO, user_admin_id: int) -> UserAdminResponse:
        pass

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
