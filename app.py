import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes.email_code_routes import email_code_route
from src.routes.note_subject_routes import note_subject_route
from src.routes.note_topic_routes import note_topic_route
from src.routes.public_tender_routes import public_tender_route
from src.routes.subject_routes import subject_route
from src.routes.topic_routes import topic_route
from src.routes.user_routes import user_rote


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_code_route)
app.include_router(note_subject_route)
app.include_router(note_topic_route)
app.include_router(public_tender_route)
app.include_router(subject_route)
app.include_router(topic_route)
app.include_router(user_rote)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
