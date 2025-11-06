from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.public_tender_board.controller_public_tender_board_interface import (
    PublicTenderBoardControllerInterface
)
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.services.public_tender_board.service_public_tender_board import ServicePublicTenderBoard
from src.services.public_tender_board.service_public_tender_board_interface import ServicePublicTenderBoardInterface
from src.utils.managers.public_tender_board_manager import PublicTenderBoardManager


class PublicTenderBoardController(PublicTenderBoardControllerInterface):
    def __init__(self) -> None:
        self.service_public_tender_board: ServicePublicTenderBoardInterface = ServicePublicTenderBoard()

    async def create_public_tender_board(self, request: Request) -> JSONResponse:
        payload = await request.json()

        public_tender_board_dto = await PublicTenderBoardManager.convert_payload_to_public_tender_board_dto(payload)

        response = await self.service_public_tender_board.create_public_tender_board(public_tender_board_dto)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="public tender board created successfully",
            status_code=HttpStatus.CREATED
        )

    async def update_public_tender_board(self, request: Request, public_tender_board_id: int) -> JSONResponse:
        payload = await request.json()

        public_tender_board_dto = await PublicTenderBoardManager.convert_payload_to_public_tender_board_dto(payload)

        response = await self.service_public_tender_board.update_public_tender_board(
            public_tender_board_dto,
            public_tender_board_id
        )

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="public tender board updated successfully",
            status_code=HttpStatus.OK
        )

    async def find_all_public_tender_boards(self, request: Request) -> JSONResponse:
        responses = await self.service_public_tender_board.find_all_public_tender_boards()
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="public tender boards found successfully",
            status_code=HttpStatus.OK
        )

    async def find_all_public_tender_boards_user(self, request: Request) -> JSONResponse:
        responses = await self.service_public_tender_board.find_all_public_tender_boards_user()

        return await response_factory(
            data=responses,
            message="public tender boards found successfully",
            status_code=HttpStatus.OK
        )

    async def delete_public_tender_board(self, request: Request, public_tender_board_id: int) -> JSONResponse:
        response = await self.service_public_tender_board.delete_public_tender_board(public_tender_board_id)

        return await response_factory(
            data=response.model_dump(mode="json"),
            message="public tender boards deleted successfully",
            status_code=HttpStatus.OK
        )
