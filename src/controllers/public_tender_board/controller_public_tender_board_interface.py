from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class PublicTenderBoardControllerInterface(ABC):
    @abstractmethod
    async def create_public_tender_board(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_public_tender_board(self, request: Request, public_tender_board_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def find_all_public_tender_boards(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_public_tender_board(self, request: Request, public_tender_board_id: int) -> JSONResponse:
        pass
