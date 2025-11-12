from fastapi.routing import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.public_tender.controller_public_tender import PublicTenderController
from src.controllers.public_tender.controller_public_tender_interface import PublicTenderControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

public_tender_route = APIRouter(prefix="/public-tender", tags=["Public Tender"])

controller_public_tender: PublicTenderControllerInterface = PublicTenderController()


@exception_handler
@public_tender_route.post("")
@authenticated
async def public_tender_create(request: Request) -> JSONResponse:
    return await controller_public_tender.public_tender_create(request)


@exception_handler
@public_tender_route.patch("/{public_tender_id}")
@authenticated
async def public_tender_patch(request: Request, public_tender_id: int) -> JSONResponse:
    return await controller_public_tender.public_tender_patch(request=request, public_tender_id=public_tender_id)


@exception_handler
@public_tender_route.get("")
@authenticated
async def public_tender_list(request: Request) -> JSONResponse:
    return await controller_public_tender.public_tender_list(request)


@exception_handler
@public_tender_route.get("/{institute}/institute")
@authenticated
async def public_tender_institute_list(request: Request, institute: str) -> JSONResponse:
    return await controller_public_tender.public_tender_institute_list(request=request, institute=institute)


@exception_handler
@public_tender_route.get("/{tender_board}/tender-board")
@authenticated
async def public_tender_board_list(request: Request, tender_board: str) -> JSONResponse:
    return await controller_public_tender.public_tender_board_list(request=request, tender_board=tender_board)


@exception_handler
@public_tender_route.delete("/{public_tender_id}")
@authenticated
async def public_tender_delete(request: Request, public_tender_id: int) -> JSONResponse:
    return await controller_public_tender.public_tender_delete(request=request, public_tender_id=public_tender_id)
