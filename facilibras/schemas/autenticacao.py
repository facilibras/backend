from facilibras.schemas import BaseSchema


class Token(BaseSchema):
    """Formato do JWT retornado no /login"""

    token: str
    tipo: str
