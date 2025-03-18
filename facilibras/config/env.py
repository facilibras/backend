from os import environ

from dotenv import load_dotenv

load_dotenv()


def get_variavel_ambiente(var: str) -> str:
    return environ.get(var, "")
