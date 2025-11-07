from typing import List

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constraints import HttpStatus
from src.db.model.models import StudyTips
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.list_id_dto import ListIDDTO
from src.models_dtos.study_tips_dto import StudyTipsDTO
from src.models_responses.study_tips_response import StudyTipsResponse
from src.repositories.study_tips.repository_study_tips_interface import StudyTipsRepositoryInterface


class StudyTipsRepository(StudyTipsRepositoryInterface):
    async def create_study_tip(self, study_tip_dto: StudyTipsDTO) -> StudyTipsResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                study_tip = StudyTips(**study_tip_dto.model_dump())
                session.add(study_tip)
                await session.commit()
                await session.refresh(study_tip)
            return StudyTipsResponse.model_validate(study_tip)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_study_tip(self, study_tip_dto: StudyTipsDTO, study_tip_id: int, user_id: int) -> StudyTipsResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(StudyTips).filter(
                        and_(
                            StudyTips.user_id == user_id,
                            StudyTips.study_tip_id == study_tip_id,
                            StudyTips.deleted == False
                        )
                    )
                )

                study_tip = response.scalar_one_or_none()

                if not study_tip:
                    raise DatabaseException("study tip not found", HttpStatus.NOT_FOUND)

                study_tip_dto.deleted = False

                for key, value in study_tip_dto.model_dump().items():
                    setattr(study_tip, key, value)

                await session.commit()
                await session.refresh(study_tip)
            return StudyTipsResponse.model_validate(study_tip)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def find_study_tips_by_user_id(self, user_id: int) -> List[StudyTipsResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(StudyTips).filter(
                        and_(
                            StudyTips.user_id == user_id,
                            StudyTips.deleted == False
                        )
                    )
                )

                study_tips = response.scalars().all()

                if not study_tips:
                    raise DatabaseException("study tip not found", HttpStatus.NOT_FOUND)

            return [
                StudyTipsResponse.model_validate(study_tip)
                for study_tip in study_tips
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_one_or_more_study_tip(self, list_ids_dto: ListIDDTO, user_id: int) -> bool:
        try:
            async with AsyncSession(self._engine_) as session:
                update_stmt = update(StudyTips).where(
                    and_(
                        StudyTips.study_tip_id.in_(list_ids_dto.ids),  # Sintaxe `in_` correta
                        StudyTips.user_id == user_id,
                        StudyTips.deleted == False
                    )
                ).values(deleted=True).returning(StudyTips.study_tip_id)

                list_ids = await session.execute(update_stmt)

                response = list_ids.scalars().all()

                if not response:
                    raise DatabaseException("study tip not found", HttpStatus.NOT_FOUND)

                await session.commit()
            return True
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)