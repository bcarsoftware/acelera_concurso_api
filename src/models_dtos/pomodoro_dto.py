from pydantic import BaseModel


class PomodoroDTO(BaseModel):
    pomodoro_name: str
    focus_minutes: int
    focus_seconds: int
    break_short: int
    break_long: int
    rounds: int
