from os import environ
from typing import Callable, TypeVar

from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T")


def get_variavel_ambiente(var: str, type_: Callable[[str], T] = str) -> T:
    return type_(environ.get(var, ""))
