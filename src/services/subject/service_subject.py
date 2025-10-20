from typing import List

from src.models_dtos.subject_dto import SubjectDTO
from src.models_responses.subject_response import SubjectResponse
from src.services.subject.service_subject_interface import ServiceSubjectInterface
from src.utils.managers.subject_manager import SubjectManager


class ServiceSubject(ServiceSubjectInterface):
    async def create_subject(self, subject_dto: SubjectDTO) -> SubjectResponse:
        await SubjectManager.make_validation(subject_dto)
        pass

    async def update_subject(self, subject_dto: SubjectDTO, subject_id: int) -> SubjectResponse:
        await SubjectManager.make_validation(subject_dto)
        pass

    async def get_subjects(self, tender_id: int) -> List[SubjectResponse]:
        pass

    async def get_subject_by_name(self, tender_id: int, name: str) -> List[SubjectResponse]:
        pass

    async def delete_subject(self, subject_id: int) -> SubjectResponse:
        pass
