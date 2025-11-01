from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.user_admin.controller_user_admin_interface import UserAdminControllerInterface
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.services.user_admin.service_user_admin import ServiceUserAdmin
from src.services.user_admin.service_user_admin_interface import ServiceUserAdminInterface
from src.utils.managers.user_admin_manager import UserAdminManager
from src.utils.managers.user_manager import UserManager


class UserAdminController(UserAdminControllerInterface):
    service_user_admin: ServiceUserAdminInterface

    def __init__(self):
        self.service_user_admin = ServiceUserAdmin()

    async def create_user_admin(self, request: Request) -> JSONResponse:
        payload = await request.json()

        user_admin_dto = await UserAdminManager.convert_payload_to_user_admin_dto(payload)

        user_admin = self.service_user_admin.create_user_admin(user_admin_dto)

        return await response_factory(
            data=user_admin,
            message="user created successfully",
            status_code=HttpStatus.CREATED,
        )

    async def login_user_admin(self, request: Request) -> JSONResponse:
        payload = await request.json()

        user_admin_dto = await UserManager.convert_payload_to_login_dto(payload)

        user_admin = self.service_user_admin.login_user_admin(user_admin_dto)

        return await response_factory(
            data=user_admin,
            message="user logged successfully",
            status_code=HttpStatus.OK,
        )

    async def update_user_admin(self, request: Request, user_admin_id: int) -> JSONResponse:
        payload = await request.json()

        user_admin_dto = await UserAdminManager.convert_payload_to_user_admin_dto(payload)

        user_admin = self.service_user_admin.update_user_admin(user_admin_dto, user_admin_id)

        return await response_factory(
            data=user_admin,
            message="user admin updated successfully",
            status_code=HttpStatus.OK,
        )
