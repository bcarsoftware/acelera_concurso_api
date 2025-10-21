from typing import List

from src.models_dtos.note_subject_dto import NoteSubjectDTO
from src.models_responses.note_subject_response import NoteSubjectResponse
from src.services.note_subject.service_note_subject_interface import ServiceNoteSubjectInterface
from src.utils.managers.note_subject_manager import NoteSubjectManager


class ServiceNoteSubject(ServiceNoteSubjectInterface):
    async def create_note_subject(self, note_subject: NoteSubjectDTO) -> NoteSubjectResponse:
        await NoteSubjectManager.make_validation(note_subject)
        pass

    async def update_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        await NoteSubjectManager.make_validation(note_subject)
        pass

    async def find_note_subject_by_subject_id(self, subject_id: int) -> List[NoteSubjectResponse]:
        pass

    async def finish_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        await NoteSubjectManager.make_validation(note_subject)
        await NoteSubjectManager.rate_success_seventh_percent(note_subject)
        pass

    async def delete_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        pass
