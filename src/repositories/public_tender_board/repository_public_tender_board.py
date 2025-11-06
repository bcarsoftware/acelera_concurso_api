from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constraints import HttpStatus
from src.db.model.models import PublicTenderBoard
from src.exceptions.database_exception import DatabaseException
from src.models_dtos.public_tender_board_dto import PublicTenderBoardDTO
from src.models_responses.public_tender_board_response import PublicTenderBoardResponse
from src.repositories.public_tender_board.repository_public_tender_board_interface import (
    PublicTenderBoardRepositoryInterface
)


class PublicTenderBoardRepository(PublicTenderBoardRepositoryInterface):
    async def create_public_tender_board(
        self,
        public_tender_board_dto: PublicTenderBoardDTO
    ) -> PublicTenderBoardResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                public_tender_board_orm = PublicTenderBoard(**public_tender_board_dto.model_dump())
                session.add(public_tender_board_orm)
                await session.commit()
                await session.refresh(public_tender_board_orm)
            return PublicTenderBoardResponse.model_validate(public_tender_board_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def update_public_tender_board(
        self, public_tender_board_dto: PublicTenderBoardDTO,
        public_tender_board_id: int
    ) -> PublicTenderBoardResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(PublicTenderBoard).filter(
                        PublicTenderBoard.public_tender_board_id == public_tender_board_id
                    )
                )

                public_tender_board_orm = response.scalar_one_or_none()

                if not public_tender_board_orm:
                    raise DatabaseException("public tender board not found", HttpStatus.NOT_FOUND)

                for key, value in public_tender_board_dto.model_dump().items():
                    setattr(public_tender_board_orm, key, value)

                await session.commit()
                await session.refresh(public_tender_board_orm)
            return PublicTenderBoardResponse.model_validate(public_tender_board_orm)
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def find_all_public_tender_boards(self) -> List[PublicTenderBoardResponse]:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(select(PublicTenderBoard).order_by(
                    PublicTenderBoard.public_tender_board_id.asc()))

                public_tender_boards = response.scalars().all()

                if not public_tender_boards:
                    raise DatabaseException("public tender board not found", HttpStatus.NOT_FOUND)

            return [
                PublicTenderBoardResponse.model_validate(public_tender_board)
                for public_tender_board in public_tender_boards
            ]
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)

    async def delete_public_tender_board(self, public_tender_board_id: int) -> PublicTenderBoardResponse:
        try:
            async with AsyncSession(self._engine_) as session:
                response = await session.execute(
                    select(PublicTenderBoard).filter_by(public_tender_board_id=public_tender_board_id)
                )

                public_tender_board = response.scalar_one_or_none()

                if not public_tender_board:
                    raise DatabaseException("public tender board not found", HttpStatus.NOT_FOUND)

                deleted_public_tender_board = PublicTenderBoardResponse.model_validate(public_tender_board)
                await session.delete(public_tender_board)
                await session.commit()
            return deleted_public_tender_board
        except Exception as e:
            print(str(e))
            if isinstance(e, DatabaseException):
                raise DatabaseException(e.message, e.code)

            raise DatabaseException("Internal Server Error", HttpStatus.INTERNAL_SERVER_ERROR)
