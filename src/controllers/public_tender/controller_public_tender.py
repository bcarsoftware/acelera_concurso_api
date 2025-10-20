from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.public_tender.controller_public_tender_interface import PublicTenderControllerInterface


class PublicTenderController(PublicTenderControllerInterface):
    async def public_tender_create(self, request: Request) -> JSONResponse:
        pass

    async def public_tender_patch(self, request: Request, user_id: int) -> JSONResponse:
        pass

    async def public_tender_list(self, request: Request) -> JSONResponse:
        pass

    async def public_tender_institute_list(self, request: Request, institute: str) -> JSONResponse:
        pass

    async def public_tender_board_delete(self, request: Request, tender_board: str) -> JSONResponse:
        pass

    async def public_tender_delete(self, request: Request, user_id: int) -> JSONResponse:
        pass