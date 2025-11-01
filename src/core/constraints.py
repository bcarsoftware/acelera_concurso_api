from dataclasses import dataclass
from http import HTTPStatus
from os import environ


@dataclass
class Constraints:
    ENCODING_UTF_8 = "utf-8"
    SECRET_KEY = environ.get("SECRET_KEY", None)
    ALGORITHM = environ.get("ALGORITHM", None)
    EXPIRE_CODE_TIME = environ.get("EXPIRE_CODE_TIME", None)
    EXPIRE_TOKEN_SESSION = environ.get("EXPIRE_TOKEN_SESSION", None)
    EMAIL_ADDRESS = environ.get("EMAIL_ADDRESS", None)
    EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD", None)
    DB_URL = environ.get("DB_URL", None)
    EXPIRE_ADMIN_TOKEN_SESSION = environ.get("EXPIRE_ADMIN_TOKEN_SESSION", None)


@dataclass
class HttpStatus:
    UNPROCESSABLE_ENTITY = HTTPStatus.UNPROCESSABLE_ENTITY
    NOT_AUTHORIZED = HTTPStatus.UNAUTHORIZED
    FORBIDDEN = HTTPStatus.FORBIDDEN
    OK = HTTPStatus.OK
    NOT_FOUND = HTTPStatus.NOT_FOUND
    INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR
    CREATED = HTTPStatus.CREATED
    BAD_REQUEST = HTTPStatus.BAD_REQUEST


@dataclass
class ParamNames:
    USER_ID = "UserID"
    TENDER_ID = "TenderID"
    SUBJECT_ID = "SubjectID"


@dataclass
class Points:
    SUBJECT_POINTS = int(environ.get("SUBJECT_POINTS"))
    TOPICS_POINTS = int(environ.get("TOPICS_POINTS"))
    NOTE_POINTS = int(environ.get("NOTE_POINTS"))
