from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.public_tender.controller_public_tender_interface import PublicTenderControllerInterface
from src.core.constraints import HttpStatus, ParamNames
from src.core.response_factory import response_factory
from src.services.public_tender.service_public_tender import ServicePublicTender
from src.services.public_tender.service_public_tender_interface import ServicePublicTenderInterface
from src.utils.header_param import get_header_param_by_name
from src.utils.managers.public_tender_manager import PublicTenderManager


class PublicTenderController(PublicTenderControllerInterface):
    service_public_tender: ServicePublicTenderInterface

    def __init__(self) -> None:
        self.service_public_tender = ServicePublicTender()

    async def public_tender_create(self, request: Request) -> JSONResponse:
        payload = await request.json()

        public_tender_dto = await PublicTenderManager.convert_payload_to_public_tender_dto(payload)

        public_tender = await self.service_public_tender.public_tender_create(public_tender_dto)

        return await response_factory(
            data=public_tender,
            message="public tender created successfully",
            status_code=HttpStatus.CREATED
        )

    async def public_tender_patch(self, request: Request, public_tender_id: int) -> JSONResponse:
        payload = await request.json()

        public_tender_dto = await PublicTenderManager.convert_payload_to_public_tender_dto(payload)

        public_tender = await self.service_public_tender.public_tender_patch(public_tender_dto, public_tender_id)

        return await response_factory(
            data=public_tender,
            message="public tender updated successfully",
            status_code=HttpStatus.OK
        )

    async def public_tender_list(self, request: Request) -> JSONResponse:
        user_id = await get_header_param_by_name(request, ParamNames.USER_ID)

        public_tenders = await self.service_public_tender.public_tender_list(user_id)

        return await response_factory(
            data=public_tenders,
            message="public tender find successfully",
            status_code=HttpStatus.OK
        )

    async def public_tender_institute_list(self, request: Request, institute: str) -> JSONResponse:
        user_id = await get_header_param_by_name(request, ParamNames.USER_ID)

        public_tenders = await self.service_public_tender.public_tender_institute_list(institute, user_id)

        return await response_factory(
            data=public_tenders,
            message="public tender find successfully",
            status_code=HttpStatus.OK
        )

    async def public_tender_board_list(self, request: Request, tender_board: str) -> JSONResponse:
        user_id = await get_header_param_by_name(request, ParamNames.USER_ID)

        public_tenders = await self.service_public_tender.public_tender_board_list(tender_board, user_id)

        return await response_factory(
            data=public_tenders,
            message="public tender find successfully",
            status_code=HttpStatus.OK
        )

    async def public_tender_delete(self, request: Request, public_tender_id: int) -> JSONResponse:
        public_tender = await self.service_public_tender.public_tender_delete(public_tender_id)

        return await response_factory(
            data=public_tender,
            message="public tender deleted successfully",
            status_code=HttpStatus.OK
        )
