from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.model.models import PublicTender
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.public_tender_dto import PublicTenderDTO
from src.models_responses.public_tender_response import PublicTenderResponse
from src.repositories.public_tender.repository_public_tender_interface import PublicTenderRepositoryInterface


class PublicTenderRepository(PublicTenderRepositoryInterface):
    async def public_tender_create(self, public_tender: PublicTenderDTO) -> PublicTenderResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                public_tender_orm = PublicTender(**public_tender.model_dump())
                session.add(public_tender_orm)
                await session.commit()
                await session.refresh(public_tender_orm)
            return await PublicTenderResponse.model_validate(public_tender_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def public_tender_patch(self, public_tender: PublicTenderDTO, public_tender_id: int) -> PublicTenderResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(PublicTender).filter(
                        and_(
                            PublicTender.public_tender_id == public_tender_id,
                            not PublicTender.deleted
                        )
                    )
                )

                public_tender_orm = response.scalar_one_or_none()

                if not public_tender_orm:
                    raise DatabaseException("public tender not found", 404)

                for key, value in public_tender.model_dump().items():
                    setattr(public_tender_orm, key, value)

                await session.commit()
                await session.refresh(public_tender_orm)
            return await PublicTenderResponse.model_validate(public_tender_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def public_tender_list(self, user_id: int) -> List[PublicTenderResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(PublicTender).filter(
                        and_(
                            PublicTender.user_id == user_id,
                            not PublicTender.deleted
                        )
                    )
                )

                public_tenders = response.scalars().all()

                if not public_tenders:
                    raise DatabaseException("any public tender found by user", 404)

            return [
                await PublicTenderResponse.model_validate(p_tender)
                for p_tender in public_tenders
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def public_tender_institute_list(self, institute: str, user_id: int) -> List[PublicTenderResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(PublicTender).filter(
                        and_(
                            PublicTender.institute == institute,
                            PublicTender.user_id == user_id,
                            not PublicTender.deleted
                        )
                    )
                )

                public_tenders = response.scalars().all()

                if not public_tenders:
                    raise DatabaseException("any public tender found by institute", 404)

            return [
                await PublicTenderResponse.model_validate(p_tender)
                for p_tender in public_tenders
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def public_tender_board_list(self, tender_board: str, user_id: int) -> List[PublicTenderResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(PublicTender).filter(
                        and_(
                            PublicTender.tender_board == tender_board,
                            PublicTender.user_id == user_id,
                            not PublicTender.deleted
                        )
                    )
                )

                public_tenders = response.scalars().all()

                if not public_tenders:
                    raise DatabaseException("any public tender found by tender board", 404)

            return [
                await PublicTenderResponse.model_validate(p_tender)
                for p_tender in public_tenders
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)

    async def public_tender_delete(self, public_tender_id: int) -> PublicTenderResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(PublicTender).filter(
                        and_(
                            PublicTender.public_tender_id == public_tender_id,
                            not PublicTender.deleted
                        )
                    )
                )

                public_tender = response.scalar_one_or_none()

                public_tender.deleted = True

                await session.commit()
                await session.refresh(public_tender)
            return await PublicTenderResponse.model_validate(public_tender)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", 500)
