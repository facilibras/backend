from facilibras.schemas import BaseSchema


class FeedbackExercicioSchema(BaseSchema):
    sucesso: bool
    mensagem: str


class PalavraSchema(BaseSchema):
    palavra: str
    video: str


class ExercicioSchema(BaseSchema):
    titulo: str
    secao: str
    descricao: str
    palavras: list
    prox_tarefa: str | None = None
    status: str | None = None

    class Config:
        from_attributes = True


class SecaoSchema(BaseSchema):
    nome: str
    qtd_ex: int
