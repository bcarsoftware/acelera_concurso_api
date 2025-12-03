from re import compile
from enum import Enum


class Regex(Enum):
    EMAIL = compile(r"^[a-z][a-z0-9._-]{1,254}[a-z0-9]@[a-z0-9]{1,16}(.[a-z]{2,3}){1,2}$")
    USERNAME = compile(r"^[a-z][a-z-_0-9]{1,255}$")
    STRING_4_32 = compile(r".{4,32}")
    STRING_2_32 = compile(r".{2,32}")
    STRING_64 = compile(r".{1,64}")
    STRING_128 = compile(r".{1,128}")
    STRING_255 = compile(r".{1,255}")
    STRING_281 = compile(r".{1,281}")
    STRING_1024 = compile(r".{1,1024}")
