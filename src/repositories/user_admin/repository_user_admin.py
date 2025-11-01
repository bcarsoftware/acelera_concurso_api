from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constraints import HttpStatus
from src.db.model.models import UserAdmin
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_admin_dto import UserAdminDTO
from src.models_responses.user_admin_response import UserAdminResponse
from src.repositories.user_admin.repository_user_admin_interface import UserAdminRepositoryInterface
from src.utils.password_util import PasswordUtil


class UserAdminRepository(UserAdminRepositoryInterface):
    async def create_user_admin(self, user_admin_dto: UserAdminDTO) -> UserAdminResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                user_admin = UserAdmin(**user_admin_dto.model_dump())
                session.add(user_admin)
                await session.commit()
                await session.refresh(user_admin)
                user_admin.password = ""
            return await UserAdminResponse.model_validate(user_admin)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)
            if isinstance(e, IntegrityError):
                raise DatabaseException("forbidden", HttpStatus.FORBIDDEN)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

    async def login_user_admin(self, user_admin_dto: LoginDTO) -> UserAdminResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(UserAdmin).filter(UserAdmin.username == user_admin_dto.username)
                )

                user_admin = response.scalar_one_or_none()

                if not user_admin:
                    raise DatabaseException("user admin not found", HTTPStatus.NOT_FOUND)

                logged = await PasswordUtil.verify(user_admin_dto.password, user_admin.password)

                if not logged:
                    raise DatabaseException("user admin login failed", HTTPStatus.BAD_REQUEST)
                user_admin.password = ""
            return await UserAdminResponse.model_validate(user_admin)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

    async def update_user_admin(self, user_admin_dto: UserAdminDTO, user_admin_id: int) -> UserAdminResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(UserAdmin).filter(UserAdmin.user_admin_id == user_admin_id)
                )

                user_admin = response.scalar_one_or_none()

                if not user_admin:
                    raise DatabaseException("user admin not found", HTTPStatus.NOT_FOUND)

                user_admin.full_name = user_admin_dto.full_name
                user_admin.username = user_admin_dto.username

                if user_admin_dto.new_password:
                    user_admin.password = user_admin_dto.password

                await session.commit()
                await session.refresh(user_admin)
                user_admin.password = ""
            return await UserAdminResponse.model_validate(user_admin)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)
