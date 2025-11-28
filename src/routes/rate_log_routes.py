from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.rate_log.controller_rate_log import RateLogController
from src.controllers.rate_log.controller_rate_log_interface import RateLogControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

rate_log_route = APIRouter(prefix="/rate_logs", tags=["Rate Logs"])

controller_rate_log: RateLogControllerInterface = RateLogController()


@exception_handler
@rate_log_route.post("/user")
@authenticated
async def find_rate_logs_entry(request: Request) -> JSONResponse:
    return await controller_rate_log.find_rate_logs_entry(request)
