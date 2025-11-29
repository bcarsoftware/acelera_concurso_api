from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

from src.models_dtos.note_subject_dto import NoteSubjectDTO
from src.models_responses.note_subject_response import NoteSubjectResponse


class ServiceNoteSubjectInterface(ABC):
    @abstractmethod
    async def create_note_subject(self, note_subject: NoteSubjectDTO) -> NoteSubjectResponse:
        pass

    @abstractmethod
    async def update_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        pass

    async def update_note_subject_rate_success(self, rate_success: Optional[Decimal], note_subject_id: int, user_id: int) -> NoteSubjectResponse:
        pass

    @abstractmethod
    async def find_note_subject_by_subject_id(self, subject_id: int) -> List[NoteSubjectResponse]:
        pass

    @abstractmethod
    async def finish_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        pass

    @abstractmethod
    async def delete_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        pass
