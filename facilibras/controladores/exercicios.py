import os
import random
import shutil
import uuid
from collections import defaultdict
from http import HTTPStatus
from typing import Sequence

from fastapi import HTTPException, UploadFile

from facilibras.controladores.pontuacao import PONTOS_PRIMEIRA_VEZ, pontos_para_subir
from facilibras.controladores.reconhecimento import reconhecer_video
from facilibras.dependencias.dal import T_ExercicioDAO, T_SecaoDAO, T_UsuarioDAO
from facilibras.modelos import Exercicio, ExercicioStatus, Secao
from facilibras.modelos.sinais import get_sinal
from facilibras.schemas import (
    ExercicioSchema,
    FeedbackExercicioSchema,
    PalavraSchema,
    SecaoSchema,
)

TEMP_DIR = "videos"


class ExercicioControle:
    def __init__(
        self,
        exercicio_dao: T_ExercicioDAO,
        secao_dao: T_SecaoDAO,
        usuario_dao: T_UsuarioDAO,
    ) -> None:
        self.exercicio_dao = exercicio_dao
        self.secao_dao = secao_dao
        self.usuario_dao = usuario_dao

    def listar_secoes(self) -> list[SecaoSchema]:
        secoes = self.secao_dao.listar_todas_com_quantidade()
        return converter_secao_para_schema(secoes)

    def listar_exercicios(self, id_usuario: int | None) -> Sequence[ExercicioSchema]:
        status = {}
        exs = self.exercicio_dao.listar_todos()
        if id_usuario:
            status = self.exercicio_dao.listar_status_exercicios(exs, id_usuario)

        exs_schema = converter_exercicios_para_schema(exs, status)
        return distribuir_exercicios(exs_schema)

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

        return converter_exercicios_para_schema(exs, status)[0]

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
        exs = self.exercicio_dao.listar_por_secao(secao.id)
        if id_usuario:
            status = self.exercicio_dao.listar_status_exercicios(exs, id_usuario)

        return converter_exercicios_para_schema(exs, status)

    def completar_exercicio(self, exercicio: Exercicio, id_usuario: int):
        usuario = self.usuario_dao.buscar_por_id(id_usuario)
        if usuario:
            primeira_vez = self.exercicio_dao.completar_exercicio(exercicio, usuario)
            print(primeira_vez)
            if primeira_vez:
                if not usuario.perfil:
                    return

                nova_qtd_sinais = usuario.perfil.qtd_ex_completos + 1
                novo_pontos_total = usuario.perfil.pontos_total + PONTOS_PRIMEIRA_VEZ
                if (
                    pontos_para_subir(usuario.perfil.nivel, usuario.perfil.pontos_nivel)
                    <= PONTOS_PRIMEIRA_VEZ
                ):
                    novo_nivel = usuario.perfil.nivel + 1
                    novo_pontos_nivel = 0
                else:
                    novo_nivel = usuario.perfil.nivel
                    novo_pontos_nivel = (
                        usuario.perfil.pontos_nivel + PONTOS_PRIMEIRA_VEZ
                    )

                self.usuario_dao.atualizar_progresso(
                    perfil=usuario.perfil,
                    nivel=novo_nivel,
                    pontos_nivel=novo_pontos_nivel,
                    pontos_total=novo_pontos_total,
                    qtd_sinais=nova_qtd_sinais,
                )

    def tentativa_exercicio(self, exercicio: Exercicio, id_usuario: int):
        usuario = self.usuario_dao.buscar_por_id(id_usuario)
        if usuario:
            self.exercicio_dao.tentativa_exercicio(exercicio, usuario)

    def reconhecer_exercicio(
        self, nome_exercicio: str, video: UploadFile, usuario: int | None
    ) -> FeedbackExercicioSchema:
        # Checa se realmente é um vídeo
        if not video.content_type or not video.content_type.startswith("video/"):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="O arquivo enviado não parece ser um vídeo.",
            )

        # Checa se o exercício existe
        exercicio = self.exercicio_dao.listar_por_nome(nome_exercicio)
        if not exercicio:
            exc_msg = f"Exercício com nome {nome_exercicio} não encontrado"
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=exc_msg,
            )

        # Checa se os sinais do exercício existe
        try:
            nome_sinal = exercicio[0].palavras[0].palavra.nome
            sinal = get_sinal(nome_sinal)
        except ValueError:
            exc_msg = f"Sinal com nome {nome_sinal} não encontrado"
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=exc_msg,
            ) from None

        # Salva o vídeo temporariamente para reconhecer
        os.makedirs(TEMP_DIR, exist_ok=True)
        if video.filename:
            extensao = os.path.splitext(video.filename)[1]
            nome_arquivo_temp = f"{uuid.uuid4().hex}{extensao}"
            caminho_arquivo_temp = os.path.join(TEMP_DIR, nome_arquivo_temp)
            with open(caminho_arquivo_temp, "wb") as buffer:
                shutil.copyfileobj(video.file, buffer)

        # Usa o video para reconhecer
        sucesso, feedback = reconhecer_video(sinal, caminho_arquivo_temp)

        # Apaga o arquivo temporário
        os.remove(caminho_arquivo_temp)

        if sucesso:
            msg = "Parabéns! Você realizou o sinal corretamente"
            if usuario is not None:
                self.completar_exercicio(exercicio[0], usuario)
        else:
            msg = feedback
            if usuario is not None:
                self.tentativa_exercicio(exercicio[0], usuario)

        return FeedbackExercicioSchema(
            sucesso=sucesso,
            mensagem=msg,
        )


def distribuir_exercicios(
    exercicios: Sequence[ExercicioSchema],
) -> list[ExercicioSchema]:
    grupos = defaultdict(list)
    for ex in exercicios:
        grupos[ex.secao].append(ex)

    for lista in grupos.values():
        random.shuffle(lista)

    secoes = list(grupos.keys())
    random.shuffle(secoes)

    resultado = []
    while any(grupos.values()):
        for secao in secoes:
            if grupos[secao]:
                resultado.append(grupos[secao].pop())  # noqa: PERF401

    return resultado


def converter_exercicios_para_schema(
    exercicios: Sequence[Exercicio],
    status_por_exercicio: dict[int, ExercicioStatus] | dict[int, None],
) -> Sequence[ExercicioSchema]:
    exercicio_schemas = []
    for exercicio in exercicios:
        palavras = [
            PalavraSchema(palavra=ex_pa.palavra.nome, video=ex_pa.palavra.url_video)
            for ex_pa in exercicio.palavras
            if ex_pa.palavra is not None
        ]

        if exercicio.prox_exercicio:
            prox_tarefa_titulo = exercicio.prox_exercicio.titulo
        else:
            prox_tarefa_titulo = None

        variacao_titulo = exercicio.nome_variacao or None

        status_enum = status_por_exercicio.get(exercicio.id)
        status_str = status_enum if status_enum is not None else None

        schema = ExercicioSchema(
            titulo=exercicio.titulo,
            secao=exercicio.secao.nome,
            descricao=exercicio.descricao,
            eh_variacao=exercicio.eh_variacao,
            variacao=variacao_titulo,
            prox_tarefa=prox_tarefa_titulo,
            palavras=palavras,
            status=status_str,
        )
        exercicio_schemas.append(schema)

    return exercicio_schemas


def converter_secao_para_schema(secoes: list[tuple[Secao, int]]) -> list[SecaoSchema]:
    return [SecaoSchema(nome=secao.nome, qtd_ex=qtd_ex) for secao, qtd_ex in secoes]
