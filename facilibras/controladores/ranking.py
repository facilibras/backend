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

        # for row in ranking:
        #     print(
        #         row.usuario_id,
        #         row.apelido,
        #         row.url_img_perfil,
        #         row.qtd_ex_completos,
        #         row.pontos_total,
        #     )
        #
        # return RankingSchema(periodo=periodo, ranking=dados_temporarios())

        return converter_ranking_para_schema(periodo, ranking)


def converter_ranking_para_schema(periodo: Periodo, ranking) -> RankingSchema:
    usuarios = []
    for coluna in ranking:
        perfil = "/perfil/" + str(coluna.usuario_id)
        usuarios.append(
            UsuarioRanking(
                nome_ou_apelido=coluna.apelido,
                imagem_perfil=coluna.url_img_perfil,
                sinais_periodo=coluna.qtd_ex_completos,
                total_sinais=coluna.qtd_ex_completos,
                link_perfil=perfil,
                pontos=coluna.pontos_total,
            )
        )

    return RankingSchema(periodo=periodo, ranking=usuarios)


def dados_temporarios():
    return [
        UsuarioRanking(
            nome_ou_apelido="João",
            imagem_perfil="https://placehold.co/50x50?text=J",
            sinais_periodo=5,
            pontos=50,
            total_sinais=8,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Ana",
            imagem_perfil="https://placehold.co/50x50?text=A",
            sinais_periodo=3,
            pontos=40,
            total_sinais=6,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Maria",
            imagem_perfil="https://placehold.co/50x50?text=M",
            sinais_periodo=2,
            pontos=30,
            total_sinais=5,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Felipe",
            imagem_perfil="https://placehold.co/50x50?text=F",
            sinais_periodo=1,
            pontos=10,
            total_sinais=2,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Marcos",
            imagem_perfil="https://placehold.co/50x50?text=M",
            sinais_periodo=1,
            pontos=10,
            total_sinais=2,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Josué",
            imagem_perfil="https://placehold.co/50x50?text=J",
            sinais_periodo=1,
            pontos=10,
            total_sinais=2,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Lucas",
            imagem_perfil="https://placehold.co/50x50?text=L",
            sinais_periodo=1,
            pontos=10,
            total_sinais=2,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Samuel",
            imagem_perfil="https://placehold.co/50x50?text=S",
            sinais_periodo=1,
            pontos=5,
            total_sinais=1,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Vinicius",
            imagem_perfil="https://placehold.co/50x50?text=V",
            sinais_periodo=1,
            pontos=5,
            total_sinais=1,
            link_perfil="/perfil/1",
        ),
        UsuarioRanking(
            nome_ou_apelido="Raul",
            imagem_perfil="https://placehold.co/50x50?text=R",
            sinais_periodo=1,
            pontos=3,
            total_sinais=2,
            link_perfil="/perfil/1",
        ),
    ]
