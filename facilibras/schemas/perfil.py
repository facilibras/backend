from facilibras.schemas import BaseSchema


class ProgressoSchema(BaseSchema):
    qtd_sinais_aprendidos: int
    nivel: int
    pontos_total: int
    pontos_nivel: int
    pontos_para_subir: int
    msg_progresso: str  # porcentagem


class AtividadeSchema(BaseSchema):
    atividade: str
    data: str


class ConquistaSchema(BaseSchema):
    id: int
    nome: str
    descricao: str


class PerfilSchema(BaseSchema):
    nome_ou_apelido: str
    imagem_fundo: str
    imagem_perfil: str
    aprendendo_desde: str

    progresso: ProgressoSchema

    atividade_recente: list[AtividadeSchema]
    conquistas: list[ConquistaSchema]


class AtualizarPerfilSchema(BaseSchema):
    apelido: str | None = None
    cor_img_fundo: str | None = None
