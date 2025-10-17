from facilibras.schemas.ranking import Periodo, RankingSchema, UsuarioRanking


class RankingControle:
    def __init__(self) -> None:
        pass

    def listar_ranking(self, periodo: Periodo):
        ranking = dados_temporarios()
        return RankingSchema(periodo=periodo, ranking=ranking)


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
