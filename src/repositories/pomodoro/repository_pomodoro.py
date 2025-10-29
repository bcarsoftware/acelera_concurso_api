from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constraints import HttpStatus
from src.db.model.models import Pomodoro
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.pomodoro_dto import PomodoroDTO
from src.models_responses.pomodoro_response import PomodoroResponse
from src.repositories.pomodoro.repository_pomodoro_interface import PomodoroRepositoryInterface


class PomodoroRepository(PomodoroRepositoryInterface):
    async def create_pomodoro(self, pomodoro_dto: PomodoroDTO) -> PomodoroResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                pomodoro = Pomodoro(**pomodoro_dto.model_dump())
                session.add(pomodoro)
                await session.commit()
                await session.refresh(pomodoro)
            return PomodoroResponse.model_validate(pomodoro)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_pomodoro(self, pomodoro_dto: PomodoroDTO, pomodoro_id: int) -> PomodoroResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Pomodoro).filter(
                        and_(
                            Pomodoro.user_id == pomodoro_dto.user_id,
                            Pomodoro.pomodoro_id == pomodoro_id
                        )
                    )
                )

                pomodoro = response.scalar_one_or_none()

                if not pomodoro:
                    raise DatabaseException("pomodoro not found", HttpStatus.NOT_FOUND)

                for key, value in pomodoro_dto.model_dump().items():
                    setattr(pomodoro, key, value)

                await session.commit()
                await session.refresh(pomodoro)
            return PomodoroResponse.model_validate(pomodoro)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def get_all_pomodoros_by_user_id(self, user_id: int) -> List[PomodoroResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Pomodoro).filter_by(user_id=user_id)
                )

                pomodoros = response.scalars().all()

                if not pomodoros:
                    raise DatabaseException("pomodoro not found", HttpStatus.NOT_FOUND)

            return [
                await PomodoroResponse.model_validate(pomodoro)
                for pomodoro in pomodoros
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_pomodoro(self, user_id: int, pomodoro_id: int) -> PomodoroResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(Pomodoro).filter(
                        and_(
                            Pomodoro.user_id == user_id,
                            Pomodoro.pomodoro_id == pomodoro_id
                        )
                    )
                )

                pomodoro = response.scalar_one_or_none()

                if not pomodoro:
                    raise DatabaseException("pomodoro not found", HttpStatus.NOT_FOUND)

                pomodoro_deleted = PomodoroResponse.model_validate(pomodoro)
                await session.delete(pomodoro)
                await session.commit()
            return pomodoro_deleted
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
