from typing import List

from src.models_dtos.rate_log_dto import RateLogDTO
from src.models_responses.rate_log_response import RateLogResponse
from src.repositories.rate_log.repository_rate_log import RateLogRepository
from src.repositories.rate_log.repository_rate_log_interface import RateLogRepositoryInterface
from src.services.rate_log.service_rate_log_interface import ServiceRateLogInterface
from src.utils.managers.rate_log_manager import RateLogManager


class ServiceRateLog(ServiceRateLogInterface):
    def __init__(self) -> None:
        self.repository_rate_log: RateLogRepositoryInterface = RateLogRepository()

    async def create_rate_log_entry(self, rate_log_dto: RateLogDTO) -> RateLogResponse:
        await RateLogManager.make_validation(rate_log_dto)

        return await self.repository_rate_log.create_rate_log_entry(rate_log_dto)

    async def find_rate_logs_entry(self, rate_log_dto: RateLogDTO) -> List[RateLogResponse]:
        await RateLogManager.make_validation(rate_log_dto)

        return await self.repository_rate_log.find_rate_logs_entry(rate_log_dto)
