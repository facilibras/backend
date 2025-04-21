from http import HTTPStatus
from random import randint
from typing import Sequence

from fastapi import HTTPException, UploadFile

from facilibras.dependencias.dal import T_ExercicioDAO, T_SecaoDAO
from facilibras.modelos import Exercicio, ExercicioStatus, Secao
from facilibras.schemas import ExercicioSchema, FeedbackExercicioSchema


class ExercicioControle:
    def __init__(self, exercicio_dao: T_ExercicioDAO, secao_dao: T_SecaoDAO) -> None:
        self.exercicio_dao = exercicio_dao
        self.secao_dao = secao_dao

    def listar_secoes(self) -> Sequence[Secao]:
        return self.secao_dao.listar_todas()

    def listar_exercicios(self, id_usuario: int | None) -> Sequence[ExercicioSchema]:
        status = {}
        exs = self.exercicio_dao.listar_todos()
        if id_usuario:
            status = self.exercicio_dao.listar_status_exercicios(exs, id_usuario)

        return converter_exercicos_para_schema(exs, status)

    def listar_exercicio_por_nome(
        self, nome: str, id_usuario: int | None
    ) -> ExercicioSchema | None:
        status = {}
        exs = self.exercicio_dao.listar_por_nome(nome)
        if id_usuario:
            status = self.exercicio_dao.listar_status_exercicios(exs, id_usuario)

        if not exs:
            exc_msg = f"Exercício com nome {nome} não encontrado"
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=exc_msg,
            )

        return converter_exercicos_para_schema(exs, status)[0]

    def listar_exercicios_por_secao(
        self, nome_secao: str, id_usuario: int | None
    ) -> Sequence[ExercicioSchema]:
        secao = self.secao_dao.listar_por_nome(nome_secao)
        if not secao:
            exc_msg = f"Seção com nome {nome_secao} não encontrado"
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=exc_msg,
            )

        status = {}
        exs = self.exercicio_dao.listar_por_secao(secao.id_secao)
        if id_usuario:
            status = self.exercicio_dao.listar_status_exercicios(exs, id_usuario)

        return converter_exercicos_para_schema(exs, status)

    def reconhecer_exercicio(
        self, nome_exercicio: str, video: UploadFile, usuario: int | None
    ) -> FeedbackExercicioSchema:
        if not video.content_type or not video.content_type.startswith("video/"):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="O arquivo enviado não parece ser um vídeo.",
            )

        exercicio = self.exercicio_dao.listar_por_nome(nome_exercicio)
        if not exercicio:
            exc_msg = f"Exercício com nome {nome_exercicio} não encontrado"
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=exc_msg,
            )

        # TODO: Reconhecer o sinal
        return FeedbackExercicioSchema(
            sucesso=bool(randint(0, 1)),
            mensagem=f"Vídeo p/ {exercicio[0].titulo} recebido com sucesso.",
        )


def converter_exercicos_para_schema(
    exercicios: Sequence[Exercicio],
    status_por_exercicio: dict[int, ExercicioStatus] | dict[int, None],
) -> Sequence[ExercicioSchema]:
    exercicio_schemas = []
    for exercicio in exercicios:
        palavras = [
            ex_pa.palavra.nome
            for ex_pa in exercicio.palavras
            if ex_pa.palavra is not None
        ]

        if exercicio.prox_exercicio:
            prox_tarefa_titulo = exercicio.prox_exercicio.titulo
        else:
            prox_tarefa_titulo = None

        status_enum = status_por_exercicio.get(exercicio.id_exercicio)
        status_str = status_enum.value if status_enum is not None else None

        schema = ExercicioSchema(
            titulo=exercicio.titulo,
            secao=exercicio.secao.titulo,
            descricao=exercicio.descricao,
            prox_tarefa=prox_tarefa_titulo,
            palavras=palavras,
            status=status_str,
        )
        exercicio_schemas.append(schema)

    return exercicio_schemas
