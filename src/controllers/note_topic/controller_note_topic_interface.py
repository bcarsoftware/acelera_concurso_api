from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class NoteTopicControllerInterface(ABC):
    @abstractmethod
    async def create_note_topic(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_note_topic(self, request: Request, note_topic_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def update_note_topic_rate_success(self, request: Request, note_topic_id: int, user_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def find_note_topic_by_topic_id(self, request: Request, topic_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def finish_note_topic(self, request: Request, note_topic_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_note_topic(self, request: Request, note_topic_id: int) -> JSONResponse:
        pass
