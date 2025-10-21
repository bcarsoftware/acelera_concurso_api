from starlette.requests import Request

from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_dto import UserDTO
from src.models_responses.user_response import UserResponse
from src.repositories.user.repository_user import UserRepository
from src.repositories.user.repository_user_interface import UserRepositoryInterface
from src.services.user.service_user_interface import ServiceUserInterface
from src.utils.managers.user_manager import UserManager
from src.utils.password_util import PasswordUtil


class ServiceUser(ServiceUserInterface):
    user_repository: UserRepositoryInterface

    def __init__(self) -> None:
        self.user_repository = UserRepository()

    async def add_user(self, user_dto: UserDTO) -> UserResponse:
        await UserManager.make_validation(user_dto)

        user_dto.password = await PasswordUtil.encrypt(user_dto.password)

        return await self.user_repository.add_user(user_dto)

    async def recover_user(self, recovery_dto: LoginDTO) -> UserResponse:
        await UserManager.make_email_verification(recovery_dto.email)

        recovery_dto.password = await PasswordUtil.encrypt(recovery_dto.password)

        return await self.user_repository.recover_user(recovery_dto)

    async def update_user(self, user_dto: UserDTO, user_id: str) -> UserResponse:
        await UserManager.make_validation(user_dto)

        return await self.user_repository.update_user(user_dto, user_id)

    async def login_user(self, login_dto: LoginDTO) -> UserResponse:
        return await self.user_repository.login_user(login_dto)

    async def logout_user(self, request: Request) -> UserResponse:
        pass

    async def delete_user(self, user_id: int) -> UserResponse:
        return await self.user_repository.delete_user(user_id)
