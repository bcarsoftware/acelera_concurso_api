from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine
from src.models_dtos.rate_log_dto import RateLogDTO
from src.models_responses.rate_log_response import RateLogResponse


class RateLogRepositoryInterface(ABC):
    @abstractmethod
    async def find_rate_logs_entry(self, rate_log_dto: RateLogDTO) -> List[RateLogResponse]:
        pass

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
