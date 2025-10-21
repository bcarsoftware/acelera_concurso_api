from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class NoteSubjectControllerInterface(ABC):
    @abstractmethod
    async def create_note_subject(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_note_subject(self, request: Request, note_subject_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def find_note_subject_by_subject_id(self, request: Request, subject_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def finish_note_subject(self, request: Request, note_subject_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_note_subject(self, request:  Request, note_subject_id: int) -> JSONResponse:
        pass
