from dataclasses import dataclass
from os import environ


@dataclass
class Constraints:
    ENCODING_UTF_8 = "utf-8"
    SECRET_KEY = environ.get("SECRET_KEY", None)
    ALGORITHM = environ.get("ALGORITHM", None)
    EXPIRE_CODE_TIME = environ.get("EXPIRE_CODE_TIME", None)
    EMAIL_ADDRESS = environ.get("EMAIL_ADDRESS", None)
    EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD", None)
    DB_URL = environ.get("DB_URL", None)
