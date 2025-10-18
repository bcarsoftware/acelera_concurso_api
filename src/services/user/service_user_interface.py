from abc import ABC, abstractmethod
from typing import Any

from fastapi import Request

from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_dto import UserDTO


class ServiceUserInterface(ABC):
    @abstractmethod
    async def add_user(self, user_dto: UserDTO) -> Any:
        pass

    @abstractmethod
    async def recover_user(self, request: Request) -> Any:
        pass

    @abstractmethod
    async def update_user(self, user_dto: UserDTO, user_id: str) -> Any:
        pass

    @abstractmethod
    async def login_user(self, login_dto: LoginDTO) -> Any:
        pass

    @abstractmethod
    async def logout_user(self, request: Request) -> Any:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> Any:
        pass
