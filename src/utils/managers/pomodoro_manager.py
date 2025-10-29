from re import match
from typing import Any, Dict

from src.core.constraints import HttpStatus
from src.exceptions.pomodoro_exception import PomodoroException
from src.models_dtos.pomodoro_dto import PomodoroDTO
from src.utils.payload_dto import payload_dto
from src.utils.regex import Regex


class PomodoroManager:
    @classmethod
    async def convert_payload_to_pomodoro_dto(cls, data_body: Dict[str, Any]) -> PomodoroDTO:
        note_subject_exception = PomodoroException(
            "invalid payload for pomodoro",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        note_subject = await payload_dto(data_body, PomodoroDTO, note_subject_exception)

        return PomodoroDTO(**note_subject)

    @classmethod
    async def make_validation(cls, pomodoro_dto: PomodoroDTO) -> None:
        await cls._check_pomodoro_strings_length_(pomodoro_dto)
        await cls._check_breaking_times_(pomodoro_dto)

        await cls._check_pomodoro_minutes_(pomodoro_dto.focus_minutes)
        await cls._check_pomodoro_seconds_(pomodoro_dto.focus_seconds)
        await cls._check_pomodoro_rounds_(pomodoro_dto.rounds)
        await cls._check_pomodoro_break_short_(pomodoro_dto.break_short)
        await cls._check_pomodoro_break_long_(pomodoro_dto.break_long)

    @classmethod
    async def _check_pomodoro_strings_length_(cls, pomodoro_dto: PomodoroDTO) -> None:
        if not match(Regex.STRING_128.value, pomodoro_dto.pomodoro_name):
            raise PomodoroException(
                "pomodoro name doesn't match between 1 util 128 characters",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_breaking_times_(cls, pomodoro_dto: PomodoroDTO) -> None:
        if pomodoro_dto.break_short == pomodoro_dto.break_long:
            raise PomodoroException(
                "pomodoro breaking times can't be the same",
                HttpStatus.BAD_REQUEST
            )
        if pomodoro_dto.break_long < pomodoro_dto.break_short:
            raise PomodoroException(
                "pomodoro breaking long time can't be smaller than pomodoro short",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_pomodoro_minutes_(cls, pomodoro_minutes: int) -> None:
        if not 0 < pomodoro_minutes < 241:
            raise PomodoroException(
                "pomodoro focus minutes doesn't match between 1 util 240 minutes",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_pomodoro_seconds_(cls, pomodoro_seconds: int) -> None:
        if not -1 < pomodoro_seconds < 60:
            raise PomodoroException(
                "pomodoro focus seconds doesn't match between 1 util 59 seconds",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_pomodoro_rounds_(cls, pomodoro_rounds: int) -> None:
        if not 0 < pomodoro_rounds < 11:
            raise PomodoroException(
                "pomodoro rounds doesn't match between 1 util 10 rounds",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_pomodoro_break_short_(cls, break_short: int) -> None:
        if not 0 < break_short < 31:
            raise PomodoroException(
                "pomodoro breaking short doesn't match between 1 util 30 minutes",
                HttpStatus.BAD_REQUEST
            )

    @classmethod
    async def _check_pomodoro_break_long_(cls, break_long: int) -> None:
        if not 0 < break_long < 61:
            raise PomodoroException(
                "pomodoro breaking long doesn't match between 1 util 60 minutes",
                HttpStatus.BAD_REQUEST
            )
