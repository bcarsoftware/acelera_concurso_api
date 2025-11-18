from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.note_subject.controller_note_subject import NoteSubjectController
from src.controllers.note_subject.controller_note_subject_interface import NoteSubjectControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

note_subject_route = APIRouter(prefix="/note-subject", tags=["Note Subject"])

controller_note_subject: NoteSubjectControllerInterface = NoteSubjectController()


@exception_handler
@note_subject_route.post("")
@authenticated
async def create_note_subject(request: Request) -> JSONResponse:
    return await controller_note_subject.create_note_subject(request)


@exception_handler
@note_subject_route.patch("/{note_subject_id}")
@authenticated
async def update_note_subject(request: Request, note_subject_id: int) -> JSONResponse:
    return await controller_note_subject.update_note_subject(request, note_subject_id)


@exception_handler
@note_subject_route.get("/{subject_id}/subject")
@authenticated
async def find_note_subject_by_subject_id(request: Request, subject_id: int) -> JSONResponse:
    return await controller_note_subject.find_note_subject_by_subject_id(request, subject_id)


@exception_handler
@note_subject_route.patch("/{note_subject_id}/finish")
@authenticated
async def finish_note_subject(request: Request, note_subject_id: int) -> JSONResponse:
    return await controller_note_subject.finish_note_subject(request, note_subject_id)


@exception_handler
@note_subject_route.delete("/{note_subject_id}")
@authenticated
async def delete_note_subject(request: Request, note_subject_id: int) -> JSONResponse:
    return await controller_note_subject.delete_note_subject(request, note_subject_id)
