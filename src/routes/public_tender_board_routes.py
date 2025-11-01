from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.controllers.public_tender_board.controller_public_tender_board import PublicTenderBoardController
from src.controllers.public_tender_board.controller_public_tender_board_interface import (
    PublicTenderBoardControllerInterface
)
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler


public_tender_board_route = APIRouter(prefix="/public_tender_board")

controller_public_tender_board: PublicTenderBoardControllerInterface = PublicTenderBoardController()


@exception_handler
@public_tender_board_route.post("")
@authenticated
async def create_public_tender_board(request: Request) -> JSONResponse:
    return await controller_public_tender_board.create_public_tender_board(request)


@exception_handler
@public_tender_board_route.patch("/{public_tender_board_id}")
@authenticated
async def update_public_tender_board(request: Request, public_tender_board_id: int) -> JSONResponse:
    return await controller_public_tender_board.update_public_tender_board(request, public_tender_board_id)


@exception_handler
@public_tender_board_route.get("")
@authenticated
async def find_all_public_tender_boards(request: Request) -> JSONResponse:
    return await controller_public_tender_board.find_all_public_tender_boards(request)


@exception_handler
@public_tender_board_route.delete("/{public_tender_board_id}/delete")
@authenticated
async def delete_public_tender_board(request: Request, public_tender_board_id: int) -> JSONResponse:
    return await controller_public_tender_board.delete_public_tender_board(request, public_tender_board_id)
