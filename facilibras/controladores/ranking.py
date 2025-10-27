from datetime import datetime, timedelta

from facilibras.dependencias.dal import T_UsuarioDAO
from facilibras.schemas.ranking import Periodo, RankingSchema, UsuarioRanking


class RankingControle:
    def __init__(self, usuario_dao: T_UsuarioDAO) -> None:
        self.usuario_dao = usuario_dao

    def listar_ranking(self, periodo: Periodo) -> RankingSchema:
        agora = datetime.now()  # noqa: DTZ005
        hoje_inicio = datetime(agora.year, agora.month, agora.day)  # noqa: DTZ001
        semana_inicio = hoje_inicio - timedelta(days=7)
        mes_inicio = hoje_inicio - timedelta(days=30)
        if periodo == Periodo.all:
            ranking = self.usuario_dao.ranking_com_perfil(inicio=None)
        elif periodo == Periodo.semanal:
            ranking = self.usuario_dao.ranking_com_perfil(inicio=semana_inicio)
        elif periodo == Periodo.hoje:
            ranking = self.usuario_dao.ranking_com_perfil(inicio=hoje_inicio)
        elif periodo == Periodo.mensal:
            ranking = self.usuario_dao.ranking_com_perfil(inicio=mes_inicio)

        return converter_ranking_para_schema(periodo, ranking)


def converter_ranking_para_schema(periodo: Periodo, ranking) -> RankingSchema:
    usuarios = []
    for coluna in ranking:
        perfil = "/perfil/" + str(coluna.usuario_id)
        usuarios.append(
            UsuarioRanking(
                nome_ou_apelido=coluna.apelido,
                imagem_perfil=perfil + "/foto",
                sinais_periodo=coluna.qtd_ex_completos,
                total_sinais=coluna.qtd_ex_completos,
                link_perfil=perfil,
                pontos=coluna.pontos_total,
            )
        )

    return RankingSchema(periodo=periodo, ranking=usuarios)
