from bcrypt import hashpw, checkpw, gensalt

from base64 import b64encode, b64decode

from src.core.constraints import Constraints


class PasswordUtil:
    @classmethod
    async def encrypt(cls, password: str) -> str:
        my_salt = gensalt()

        bytes_password = password.encode(Constraints.ENCODING_UTF_8)

        hash_bytes = hashpw(bytes_password, my_salt)

        return b64encode(hash_bytes).decode(Constraints.ENCODING_UTF_8)

    @classmethod
    async def verify(cls, password: str, hashed_password: str) -> bool:
        bytes_password = password.encode(Constraints.ENCODING_UTF_8)

        bytes_hashed = b64decode(hashed_password.encode(Constraints.ENCODING_UTF_8))

        return checkpw(bytes_password, bytes_hashed)
