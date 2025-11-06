from typing import List

from src.models_dtos.public_tender_board_dto import PublicTenderBoardDTO
from src.models_responses.public_tender_board_response import PublicTenderBoardResponse
from src.repositories.public_tender_board.repository_public_tender_board_interface import (
    PublicTenderBoardRepositoryInterface
)
from src.repositories.public_tender_board.repository_public_tender_board import PublicTenderBoardRepository
from src.services.public_tender_board.service_public_tender_board_interface import ServicePublicTenderBoardInterface
from src.utils.managers.public_tender_board_manager import PublicTenderBoardManager


class ServicePublicTenderBoard(ServicePublicTenderBoardInterface):
    def __init__(self) -> None:
        self.repository_public_tender_board: PublicTenderBoardRepositoryInterface = PublicTenderBoardRepository()

    async def create_public_tender_board(
        self,
        public_tender_board_dto: PublicTenderBoardDTO
    ) -> PublicTenderBoardResponse:
        await PublicTenderBoardManager.make_validation(public_tender_board_dto)

        return await self.repository_public_tender_board.create_public_tender_board(
            public_tender_board_dto
        )

    async def update_public_tender_board(
        self,
        public_tender_board_dto: PublicTenderBoardDTO,
        public_tender_board_id: int
    ) -> PublicTenderBoardResponse:
        await PublicTenderBoardManager.make_validation(public_tender_board_dto)

        return await self.repository_public_tender_board.update_public_tender_board(
            public_tender_board_dto,
            public_tender_board_id
        )

    async def find_all_public_tender_boards(self) -> List[PublicTenderBoardResponse]:
        return await self.repository_public_tender_board.find_all_public_tender_boards()

    async def delete_public_tender_board(self, public_tender_board_id: int) -> PublicTenderBoardResponse:
        return await self.repository_public_tender_board.delete_public_tender_board(public_tender_board_id)