from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.db.core.db_base import get_engine
from src.db.model.models import User
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.login_dto import LoginDTO
from src.models_dtos.user_dto import UserDTO
from src.models_responses.user_response import UserResponse
from src.repositories.user.repository_user_interface import UserRepositoryInterface
from src.utils.password_util import PasswordUtil


class UserRepository(UserRepositoryInterface):
    async def add_user(self, user_dto: UserDTO) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                user = User(**user_dto.model_dump())
                session.add(user)
                await session.commit()
                await session.refresh(user)
            return await UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def recover_user(self, recovery_dto: LoginDTO) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter_by(email=recovery_dto.username)
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", 404)

                user.password = recovery_dto.password
                await session.commit()
                await session.refresh(user)
            return await UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def update_user(self, user_dto: UserDTO, user_id: str) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter_by(user_id=user_id)
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", 404)

                original_password = user.password

                for key, value in user_dto.model_dump().items():
                    setattr(user, key, value)

                user.password = original_password

                await session.commit()
                await session.refresh(user)
            return await UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def login_user(self, login_dto: LoginDTO) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter(or_(
                        User.username == login_dto.username,
                        User.email == login_dto.username
                    ))
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", 404)

                if user.deleted:
                    user.deleted = False
                    await session.commit()
                    await session.refresh(user)

                success = await PasswordUtil.verify(login_dto.password, user.password)

                if not success:
                    raise DatabaseException("password not correct", 401)
            return await UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def delete_user(self, user_id: int) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter_by(user_id=user_id)
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", 404)

                user.deleted = True

                await session.commit()
                await session.refresh(user)
            return await UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
