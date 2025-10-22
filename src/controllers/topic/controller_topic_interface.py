from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class TopicControllerInterface(ABC):
    @abstractmethod
    async def create_topic(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_topic(self, request: Request, topic_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def get_topics(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def get_topic_by_name(self, request: Request, name: str) -> JSONResponse:
        pass

    @abstractmethod
    async def get_topic_by_status(self, request: Request, status: str) -> JSONResponse:
        pass

    @abstractmethod
    async def finish_topic(self, request: Request, topic_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_topic(self, request: Request, topic_id: int) -> JSONResponse:
        pass
