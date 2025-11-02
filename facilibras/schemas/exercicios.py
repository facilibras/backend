from pydantic import Field

from facilibras.schemas import BaseSchema


class Feedback(BaseSchema):
    correto: bool
    mensagem: str


class FeedbackSchema(BaseSchema):
    sucesso: bool
    feedback: list[Feedback] = Field(default_factory=list)


class PalavraSchema(BaseSchema):
    palavra: str
    video: str


class ExercicioSchema(BaseSchema):
    titulo: str
    secao: str
    descricao: str
    palavras: list
    eh_variacao: bool = False
    variacao: str | None = None
    prox_tarefa: str | None = None
    status: str | None = None

    class Config:
        from_attributes = True


class SecaoSchema(BaseSchema):
    nome: str
    qtd_ex: int
