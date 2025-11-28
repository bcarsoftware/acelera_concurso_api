import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes.email_code_routes import email_code_route
from src.routes.note_subject_routes import note_subject_route
from src.routes.note_topic_routes import note_topic_route
from src.routes.pomodoro_routes import pomodoro_route
from src.routes.public_tender_board_routes import public_tender_board_route
from src.routes.public_tender_routes import public_tender_route
from src.routes.rate_log_routes import rate_log_route
from src.routes.study_tips_routes import study_tips_route
from src.routes.subject_routes import subject_route
from src.routes.topic_routes import topic_route
from src.routes.user_admin_routes import user_admin_route
from src.routes.user_routes import user_rote


with open("cors_origins.txt", "r") as reader:
    origins = reader.readlines()
    origins = [origin.strip() for origin in origins]


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Principal"])
async def root() -> dict:
    return { "message": "Hello World! I'm The Acelera Concurso API!" }

app.include_router(email_code_route)
app.include_router(note_subject_route)
app.include_router(note_topic_route)
app.include_router(public_tender_route)
app.include_router(subject_route)
app.include_router(study_tips_route)
app.include_router(topic_route)
app.include_router(user_rote)
app.include_router(pomodoro_route)
app.include_router(rate_log_route)
app.include_router(user_admin_route)
app.include_router(public_tender_board_route)


if __name__ == '__main__':
    uvicorn.run("app:app", host='localhost', port=8000, reload=True)
