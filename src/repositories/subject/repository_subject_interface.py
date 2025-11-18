from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine
from src.models_dtos.subject_dto import SubjectDTO
from src.models_responses.subject_response import SubjectResponse


class SubjectRepositoryInterface(ABC):
    @abstractmethod
    async def create_subject(self, subject_dto: SubjectDTO) -> SubjectResponse:
        pass

    @abstractmethod
    async def update_subject(self, subject_dto: SubjectDTO, subject_id: int) -> SubjectResponse:
        pass

    @abstractmethod
    async def get_subjects(self, tender_id: int) -> List[SubjectResponse]:
        pass

    @abstractmethod
    async def delete_subject(self, subject_id: int, points: int) -> SubjectResponse:
        pass

    @abstractmethod
    async def finish_subject(self, subject_id: int) -> SubjectResponse:
        pass

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
