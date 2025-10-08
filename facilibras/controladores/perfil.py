from facilibras.schemas.perfil import (
    AtividadeSchema,
    ConquistaSchema,
    PerfilSchema,
    ProgressoSchema,
)


class PerfilControle:
    def __init__(self) -> None:
        pass

    def listar_perfil(self, id_usuario: int) -> PerfilSchema:
        return dados_temporarios()


def dados_temporarios() -> PerfilSchema:
    p = ProgressoSchema(
        qtd_sinais_aprendidos=10,
        nivel=10,
        pontos_total=1000,
        pontos_nivel=10,
        pontos_para_subir=90,
        msg_progresso="10%",
    )
    c = [
        ConquistaSchema(
            id=1,
            nome="Alfabeto",
            descricao="Completou todos sinais da categoria Alfabeto",
        ),
        ConquistaSchema(
            id=2,
            nome="Números",
            descricao="Completou todos sinais da categoria Números",
        ),
    ]
    a = [
        AtividadeSchema(atividade="Realizou o sinal A com sucesso!", data="04/10/2020"),
        AtividadeSchema(atividade="Realizou o sinal J com sucesso!", data="04/10/2020"),
        AtividadeSchema(atividade="Conquista 'Alfabeto' obtida!", data="04/10/2020"),
    ]

    return PerfilSchema(
        nome_ou_apelido="Temp",
        imagem_fundo="",
        imagem_perfil="https://placehold.co/50x50?text=T",
        progresso=p,
        aprendendo_desde="01/01/2023",
        conquistas=c,
        atividade_recente=a,
    )
