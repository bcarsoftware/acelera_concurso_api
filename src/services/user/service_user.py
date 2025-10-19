from starlette.requests import Request

from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_dto import UserDTO
from src.models_responses.user_response import UserResponse
from src.services.user.service_user_interface import ServiceUserInterface
from src.utils.managers.user_manager import UserManager
from src.utils.password_util import PasswordUtil


class ServiceUser(ServiceUserInterface):
    async def add_user(self, user_dto: UserDTO) -> UserResponse:
        await UserManager.make_validation(user_dto)

        user_dto.password = await PasswordUtil.encrypt(user_dto.password)
        pass

    async def recover_user(self, recovery_dto: LoginDTO) -> UserResponse:
        recovery_dto.password = await PasswordUtil.encrypt(recovery_dto.password)
        pass

    async def update_user(self, user_dto: UserDTO, user_id: str) -> UserResponse:
        await UserManager.make_validation(user_dto)
        pass

    async def login_user(self, login_dto: LoginDTO) -> UserResponse:
        pass

    async def logout_user(self, request: Request) -> UserResponse:
        pass

    async def delete_user(self, user_id: int) -> UserResponse:
        pass
