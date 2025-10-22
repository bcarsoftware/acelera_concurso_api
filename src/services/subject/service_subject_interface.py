from abc import ABC, abstractmethod
from typing import List

from src.models_dtos.subject_dto import SubjectDTO
from src.models_responses.subject_response import SubjectResponse


class ServiceSubjectInterface(ABC):
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
    async def get_subject_by_name(self, tender_id: int, name: str) -> List[SubjectResponse]:
        pass

    @abstractmethod
    async def finish_subject(self, subject_id: int) -> SubjectResponse:
        pass

    @abstractmethod
    async def delete_subject(self, subject_id: int) -> SubjectResponse:
        pass
