from enum import Enum

from facilibras.schemas import BaseSchema


class Periodo(str, Enum):
    all = "all"
    mensal = "mensal"
    semanal = "semanal"
    hoje = "hoje"


class UsuarioRanking(BaseSchema):
    nome_ou_apelido: str
    imagem_perfil: str
    sinais_periodo: int
    pontos: int
    total_sinais: int
    link_perfil: str


class RankingSchema(BaseSchema):
    periodo: Periodo
    ranking: list[UsuarioRanking]
