from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from facilibras.dependencias.db import T_Session
from facilibras.modelos import (
    Exercicio,
    PalavraExercicio,
    ExercicioStatus,
    ExercicioUsuario,
)


class ExercicioDAO:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def listar_todos(self) -> Sequence[Exercicio]:
        stmt = select(Exercicio).options(
            selectinload(Exercicio.secao),
            selectinload(Exercicio.palavras).selectinload(PalavraExercicio.palavra),
        )

        return self.session.scalars(stmt).all()

    def listar_todos_com_status_usuario(
        self, usuario_id: int
    ) -> tuple[Sequence[Exercicio], dict[int, ExercicioStatus]]:
        stmt_exercicios = select(Exercicio).options(
            selectinload(Exercicio.secao),
            selectinload(Exercicio.palavras).selectinload(PalavraExercicio.palavra),
        )

        exercicios = self.session.scalars(stmt_exercicios).all()

        stmt_status_usuario = select(
            ExercicioUsuario.id_exercicio, ExercicioUsuario.status
        ).where(ExercicioUsuario.id_usuario == usuario_id)

        resultados_status = self.session.execute(stmt_status_usuario).all()
        status_por_exercicio = {
            col.id_exercicio: col.status for col in resultados_status
        }

        return exercicios, status_por_exercicio

    def listar_por_secao(
        self, secao: int, usuario_id: int | None
    ) -> Sequence[Exercicio]:
        # TODO: Retornar com o progresso do usuário
        return self.session.scalars(
            select(Exercicio).where(Exercicio.id_secao == secao)
        ).all()

    def listar_por_nome(self, nome: str, usuario_id: int | None) -> Exercicio | None:
        # TODO: Retornar com o progresso do usuário
        return self.session.scalar(select(Exercicio).where(Exercicio.titulo == nome))
