from abc import ABC, abstractmethod

from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_dto import UserDTO
from src.models_responses.user_response import UserResponse


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def add_user(self, user_dto: UserDTO) -> UserResponse:
        pass

    @abstractmethod
    async def recover_user(self, recovery_dto: LoginDTO) -> UserResponse:
        pass

    @abstractmethod
    async def update_user(self, user_dto: UserDTO, user_id: str) -> UserResponse:
        pass

    @abstractmethod
    async def login_user(self, login_dto: LoginDTO) -> UserResponse:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> UserResponse:
        pass
