from http import HTTPStatus

from fastapi import HTTPException

from facilibras.dependencias.dal import T_ExercicioDAO, T_UsuarioDAO
from facilibras.modelos import Perfil
from facilibras.schemas.perfil import (
    AtividadeSchema,
    ConquistaSchema,
    PerfilSchema,
    ProgressoSchema,
)


class PerfilControle:
    def __init__(
        self, exercicio_dao: T_ExercicioDAO, usuario_dao: T_UsuarioDAO
    ) -> None:
        self.usuario_dao = usuario_dao
        self.exercicio_dao = exercicio_dao

    def listar_perfil(self, id_usuario: int) -> PerfilSchema:
        perfil = self.usuario_dao.buscar_perfil_usuario(id_usuario)
        if not perfil:
            exc_msg = f"Perfil não encontrado para usuário {id_usuario}"
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc_msg)

        exs = self.exercicio_dao.listar_atividade(id_usuario)

        return converter_perfil_para_schema(perfil, exs)


def converter_perfil_para_schema(perfil: Perfil, exs) -> PerfilSchema:
    p = ProgressoSchema(
        qtd_sinais_aprendidos=perfil.qtd_ex_completos,
        nivel=perfil.nivel,
        pontos_total=perfil.pontos_total,
        pontos_nivel=perfil.pontos_nivel,
        pontos_para_subir=1000,
        msg_progresso="TODO",
    )

    a = []
    for ex in exs:
        sinal = ex["titulo"].replace("_", " ").title()
        data = ex["criado_em"]
        atividade = f"Realizou o sinal {sinal} com sucesso!"
        a.append((atividade, data))

    c = []
    for conq in perfil.conquistas:
        c.append(
            ConquistaSchema(
                id=conq.id, nome=conq.nome.value, descricao=conq.descricao or ""
            )
        )
        atividade = f"Conquista '{conq.nome.value}' obtida!"
        data = conq.data_conquista
        a.append((atividade, data))

    a.sort(key=lambda x: x[1], reverse=True)
    atividades = [
        AtividadeSchema(atividade=ati[0], data=ati[1].strftime("%d/%m/%Y %H:%M:%S"))
        for ati in a
    ]

    return PerfilSchema(
        nome_ou_apelido=perfil.apelido,
        imagem_fundo=perfil.url_img_fundo or "",
        imagem_perfil=perfil.url_img_perfil or "https://placehold.co/50x50",
        aprendendo_desde=perfil.criado_em.strftime("%d/%m/%Y"),
        progresso=p,
        conquistas=c,
        atividade_recente=atividades,
    )
