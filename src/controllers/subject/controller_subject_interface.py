from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import JSONResponse


class SubjectControllerInterface(ABC):
    @abstractmethod
    async def create_subject(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def update_subject(self, request: Request, subject_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def get_subjects(self, request: Request) -> JSONResponse:
        pass

    @abstractmethod
    async def get_subject_by_name(self, request: Request, name: str) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_subject(self, request: Request, subject_id: int) -> JSONResponse:
        pass
