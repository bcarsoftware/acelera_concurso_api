from enum import Enum


class Regex(Enum):
    EMAIL = r"^[a-z][a-z0-9._-]{1,254}[a-z0-9]@[a-z0-9]{1,16}(.[a-z]{2,3}){1,2}$"
    USERNAME = r"^[a-z][a-z-_0-9]{1,255}$"
    STRING_64 = r".{1,64}"
    STRING_128 = r".{1,128}"
    STRING_255 = r".{1,255}"
    STRING_281 = r".{1,281}"
    STRING_1024 = r".{1,1024}"
