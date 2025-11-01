from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine
from src.models_dtos.public_tender_dto import PublicTenderDTO
from src.models_responses.public_tender_response import PublicTenderResponse


class PublicTenderRepositoryInterface(ABC):
    @abstractmethod
    async def public_tender_create(self, public_tender: PublicTenderDTO) -> PublicTenderResponse:
        pass

    @abstractmethod
    async def public_tender_patch(self, public_tender: PublicTenderDTO, public_tender_id: int) -> PublicTenderResponse:
        pass

    @abstractmethod
    async def public_tender_list(self, user_id: int) -> List[PublicTenderResponse]:
        pass

    @abstractmethod
    async def public_tender_institute_list(self, institute: str, user_id: int) -> List[PublicTenderResponse]:
        pass

    @abstractmethod
    async def public_tender_board_list(self, tender_board: str, user_id: int) -> List[PublicTenderResponse]:
        pass

    @abstractmethod
    async def public_tender_delete(self, public_tender_id: int) -> PublicTenderResponse:
        pass

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
