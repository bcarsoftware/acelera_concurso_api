from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.core.db_base import get_engine
from src.models_dtos.note_subject_dto import NoteSubjectDTO
from src.models_responses.note_subject_response import NoteSubjectResponse


class NoteSubjectRepositoryInterface(ABC):
    @abstractmethod
    async def create_note_subject(self, note_subject: NoteSubjectDTO) -> NoteSubjectResponse:
        pass

    @abstractmethod
    async def update_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        pass

    @abstractmethod
    async def find_note_subject_by_subject_id(self, subject_id: int) -> List[NoteSubjectResponse]:
        pass

    @abstractmethod
    async def finish_note_subject(self, note_subject: NoteSubjectDTO, note_subject_id: int) -> NoteSubjectResponse:
        pass

    @abstractmethod
    async def delete_note_subject(self, note_subject_id: int) -> NoteSubjectResponse:
        pass

    @property
    def _engine_(self) -> AsyncEngine:
        eng = get_engine()
        return next(eng)
