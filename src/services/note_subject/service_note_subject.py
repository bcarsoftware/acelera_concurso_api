from decimal import Decimal
from typing import List, Optional

from src.models_dtos.note_subject_dto import NoteSubjectDTO
from src.models_responses.note_subject_response import NoteSubjectResponse
from src.repositories.note_subject.repository_note_subject import NoteSubjectRepository
from src.repositories.note_subject.repository_note_subject_interface import NoteSubjectRepositoryInterface
from src.services.note_subject.service_note_subject_interface import ServiceNoteSubjectInterface
from src.utils.managers.note_subject_manager import NoteSubjectManager


class ServiceNoteSubject(ServiceNoteSubjectInterface):
    def __init__(self) -> None:
        self.note_subject_repository: NoteSubjectRepositoryInterface = NoteSubjectRepository()

    async def create_note_subject(self, note_subject: NoteSubjectDTO) -> NoteSubjectResponse:
        await NoteSubjectManager.make_validation(note_subject)

        return await self.note_subject_repository.create_note_subject(note_subject)

    async def update_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        await NoteSubjectManager.make_validation(note_subject)

        return await self.note_subject_repository.update_note_subject(note_subject, note_subject_id)

    async def update_note_subject_rate_success(self, rate_success: Optional[Decimal], note_subject_id: int, user_id: int) -> NoteSubjectResponse:
        await NoteSubjectManager.verify_rate_success_none(rate_success)

        new_rate_success = rate_success or Decimal("0")

        return await self.note_subject_repository.update_note_subject_rate_success(new_rate_success, note_subject_id, user_id)

    async def find_note_subject_by_subject_id(self, subject_id: int) -> List[NoteSubjectResponse]:
        return await self.note_subject_repository.find_note_subject_by_subject_id(subject_id)

    async def finish_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        return await self.note_subject_repository.finish_note_subject(note_subject_id)

    async def delete_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        return await self.note_subject_repository.delete_note_subject(note_subject_id)
