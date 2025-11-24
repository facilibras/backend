from os import environ
from typing import Any, Callable, TypeVar

from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T")


def get_variavel_ambiente(
    var: str, type_: Callable[[str], T] = str, default: Any = ""
) -> T:
    return type_(environ.get(var, default))


def get_variavel_ambiente_atual(
    var: str, type_: Callable[[str], T] = str, default: Any = ""
) -> T:
    load_dotenv(override=True)
    return get_variavel_ambiente(var, type_, default)
