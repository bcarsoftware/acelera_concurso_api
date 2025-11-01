from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_admin_dto import UserAdminDTO
from src.models_responses.user_admin_response import UserAdminResponse
from src.repositories.user_admin.repository_user_admin import UserAdminRepository
from src.repositories.user_admin.repository_user_admin_interface import UserAdminRepositoryInterface
from src.services.user_admin.service_user_admin_interface import ServiceUserAdminInterface
from src.utils.managers.user_admin_manager import UserAdminManager
from src.utils.password_util import PasswordUtil


class ServiceUserAdmin(ServiceUserAdminInterface):
    repository_user_admin: UserAdminRepositoryInterface

    def __init__(self) -> None:
        self.repository_user_admin = UserAdminRepository()

    async def create_user_admin(self, user_admin_dto: UserAdminDTO) -> UserAdminResponse:
        await UserAdminManager.make_validation(user_admin_dto)

        user_admin_dto.password = await PasswordUtil.encrypt(user_admin_dto.password)

        return await self.repository_user_admin.create_user_admin(user_admin_dto)

    async def login_user_admin(self, user_admin_dto: LoginDTO) -> UserAdminResponse:
        user_admin = await self.repository_user_admin.login_user_admin(user_admin_dto)

        user_admin.password = ""

        return user_admin

    async def update_user_admin(self, user_admin_dto: UserAdminDTO, user_admin_id: int) -> UserAdminResponse:
        if user_admin_dto.new_password:
            user_admin_dto.password = user_admin_dto.new_password
            await UserAdminManager.make_validation(user_admin_dto)
            user_admin_dto.password = await PasswordUtil.encrypt(user_admin_dto.password)
        else:
            await UserAdminManager.make_validation(user_admin_dto)

        user_admin = await self.repository_user_admin.update_user_admin(user_admin_dto, user_admin_id)

        user_admin.password = ""

        return user_admin
