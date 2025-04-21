from datetime import datetime

from pydantic import BaseModel


class FeedbackExercicioSchema(BaseModel):
    sucesso: bool
    mensagem: str


class ExercicioSchema(BaseModel):
    titulo: str
    secao: str
    descricao: str
    palavras: list
    prox_tarefa: str | None = None
    status: str | None = None

    class Config:
        from_attributes = True


class SecaoSchema(BaseModel):
    nome: str
    registro_em: datetime
