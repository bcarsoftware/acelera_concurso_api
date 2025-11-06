from http import HTTPStatus

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

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
                user.password = ""
            return UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

    async def recover_user(self, recovery_dto: LoginDTO) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter(
                        and_(
                            User.email == recovery_dto.username,
                            not User.deleted
                        )
                    )
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", HTTPStatus.NOT_FOUND)

                user.password = recovery_dto.password
                await session.commit()
                await session.refresh(user)
                user.password = ""
            return UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

    async def update_user(self, user_dto: UserDTO, user_id: int) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter(
                        and_(
                            User.user_id == user_id,
                            not User.deleted
                        )
                    )
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", HTTPStatus.NOT_FOUND)

                user_dto.password = user.password
                user_dto.deleted = False

                for key, value in user_dto.model_dump().items():
                    setattr(user, key, value)

                await session.commit()
                await session.refresh(user)
                user.password = ""
            return UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

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
                    raise DatabaseException("user not found", HTTPStatus.NOT_FOUND)

                if user.deleted:
                    user.deleted = False
                    await session.commit()
                    await session.refresh(user)

                success = await PasswordUtil.verify(login_dto.password, user.password)

                if not success:
                    raise DatabaseException("password not correct", HTTPStatus.FORBIDDEN)
                user.password = ""
            return UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

    async def update_user_password(self, user_dto: LoginDTO, user_id: int) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter(
                        and_(
                            User.user_id == user_id,
                            not User.deleted
                        )
                    )
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", HTTPStatus.NOT_FOUND)

                user.password = user_dto.password

                await session.commit()
                await session.refresh(user)
                user.password = ""
            return UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

    async def delete_user(self, user_id: int) -> UserResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(User).filter(
                        and_(
                            User.user_id == user_id,
                            not User.deleted
                        )
                    )
                )

                user = response.scalar_one_or_none()

                if not user:
                    raise DatabaseException("user not found", HTTPStatus.NOT_FOUND)

                user.deleted = True

                await session.commit()
                await session.refresh(user)
                user.password = ""
            return UserResponse.model_validate(user)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)
