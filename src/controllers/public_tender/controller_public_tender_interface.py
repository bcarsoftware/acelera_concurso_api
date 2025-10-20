from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class PublicTenderControllerInterface(ABC):
    @abstractmethod
    async def public_tender_create(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def public_tender_patch(self, request: Request, user_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def public_tender_list(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def public_tender_institute_list(self, request: Request, institute: str) -> JSONResponse:
        pass

    @abstractmethod
    async def public_tender_board_list(self, request: Request, tender_board: str) -> JSONResponse:
        pass

    @abstractmethod
    async def public_tender_delete(self, request: Request, user_id: int) -> JSONResponse:
        pass
