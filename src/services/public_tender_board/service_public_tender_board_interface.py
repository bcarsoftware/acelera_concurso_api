from abc import ABC, abstractmethod
from typing import List

from src.models_dtos.public_tender_board_dto import PublicTenderBoardDTO
from src.models_responses.public_tender_board_response import PublicTenderBoardResponse


class ServicePublicTenderBoardInterface(ABC):
    @abstractmethod
    async def create_public_tender_board(
        self,
        public_tender_board_dto: PublicTenderBoardDTO
    ) -> PublicTenderBoardResponse:
        pass

    @abstractmethod
    async def update_public_tender_board(
        self,
        public_tender_board_dto: PublicTenderBoardDTO,
        public_tender_board_id: int
    ) -> PublicTenderBoardResponse:
        pass

    @abstractmethod
    async def find_all_public_tender_boards(self) -> List[PublicTenderBoardResponse]:
        pass

    @abstractmethod
    async def delete_public_tender_board(self, public_tender_board_id: int) -> PublicTenderBoardResponse:
        pass
