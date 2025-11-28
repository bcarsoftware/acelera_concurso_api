from starlette.requests import Request
from starlette.responses import JSONResponse

from src.controllers.rate_log.controller_rate_log_interface import RateLogControllerInterface
from src.core.constraints import HttpStatus
from src.core.response_factory import response_factory
from src.services.rate_log.service_rate_log import ServiceRateLog
from src.services.rate_log.service_rate_log_interface import ServiceRateLogInterface
from src.utils.managers.rate_log_manager import RateLogManager


class RateLogController(RateLogControllerInterface):
    def __init__(self) -> None:
        self.service_rate_log: ServiceRateLogInterface = ServiceRateLog()

    async def find_rate_logs_entry(self, request: Request) -> JSONResponse:
        payload = await request.json()

        rate_log_dto = await RateLogManager.convert_payload_to_rate_log_dto(payload)

        responses = await self.service_rate_log.find_rate_logs_entry(rate_log_dto)
        responses = [response.model_dump(mode="json") for response in responses]

        return await response_factory(
            data=responses,
            message="study_tip created successfully",
            status_code=HttpStatus.OK
        )
