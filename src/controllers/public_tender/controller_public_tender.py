from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.public_tender.controller_public_tender_interface import PublicTenderControllerInterface
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.utils.managers.public_tender_manager import PublicTenderManager


class PublicTenderController(PublicTenderControllerInterface):
    async def public_tender_create(self, request: Request) -> JSONResponse:
        payload = await request.json()

        public_tender_dto = await PublicTenderManager.convert_payload_to_public_tender_dto(payload)

        return await response_factory(
            data={},
            message="public tender created successfully",
            status_code=HttpStatus.CREATED
        )

    async def public_tender_patch(self, request: Request, user_id: int) -> JSONResponse:
        payload = await request.json()

        public_tender_dto = await PublicTenderManager.convert_payload_to_public_tender_dto(payload)

        return await response_factory(
            data={},
            message="public tender created successfully",
            status_code=HttpStatus.CREATED
        )

    async def public_tender_list(self, request: Request) -> JSONResponse:
        return await response_factory(
            data=[],
            message="public tender created successfully",
            status_code=HttpStatus.CREATED
        )

    async def public_tender_institute_list(self, request: Request, institute: str) -> JSONResponse:
        return await response_factory(
            data=[],
            message="public tender created successfully",
            status_code=HttpStatus.CREATED
        )

    async def public_tender_board_list(self, request: Request, tender_board: str) -> JSONResponse:
        return await response_factory(
            data=[],
            message="public tender created successfully",
            status_code=HttpStatus.CREATED
        )

    async def public_tender_delete(self, request: Request, user_id: int) -> JSONResponse:
        return await response_factory(
            data={},
            message="public tender created successfully",
            status_code=HttpStatus.CREATED
        )