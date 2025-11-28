from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.controllers.subject.controller_subject import SubjectController
from src.controllers.subject.controller_subject_interface import SubjectControllerInterface
from src.core.authentication import authenticated
from src.core.exception_handler import exception_handler

subject_route = APIRouter(prefix="/subject", tags=["Subject"])

controller_subject: SubjectControllerInterface = SubjectController()


@exception_handler
@subject_route.post("")
@authenticated
async def create_subject(request: Request) -> JSONResponse:
    return await controller_subject.create_subject(request)


@exception_handler
@subject_route.patch("/{subject_id}")
@authenticated
async def update_subject(request: Request, subject_id: int) -> JSONResponse:
    return await controller_subject.update_subject(request, subject_id)


@exception_handler
@subject_route.patch("/{subject_id}/fulfillment/{user_id}/user")
@authenticated
async def update_subject_fulfillment(request: Request, subject_id: int, user_id: int) -> JSONResponse:
    return await controller_subject.update_subject_fulfillment(request, subject_id, user_id)


@exception_handler
@subject_route.get("")
@authenticated
async def get_subjects(request: Request) -> JSONResponse:
    return await controller_subject.get_subjects(request)


@exception_handler
@subject_route.patch("/{subject_id}/finish")
@authenticated
async def finish_subject(request: Request, subject_id: int) -> JSONResponse:
    return await controller_subject.finish_subject(request, subject_id)


@exception_handler
@subject_route.delete("/{subject_id}")
@authenticated
async def delete_subject(request: Request, subject_id: int) -> JSONResponse:
    return await controller_subject.delete_subject(request, subject_id)
