from abc import ABC, abstractmethod
from typing import List

from src.models_dtos.rate_log_dto import RateLogDTO
from src.models_responses.rate_log_response import RateLogResponse


class ServiceRateLogInterface(ABC):
    @abstractmethod
    async def find_rate_logs_entry(self, rate_log_dto: RateLogDTO) -> List[RateLogResponse]:
        pass
