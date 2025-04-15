from pydantic import BaseModel


class Token(BaseModel):
    """Formato do JWT retornado no /login"""

    token: str
    tipo: str
