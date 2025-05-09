from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from facilibras.dependencias.db import T_Session
from facilibras.modelos import (
    Exercicio,
    ExercicioStatus,
    ExercicioUsuario,
    PalavraExercicio,
    Usuario,
)

opt = (
    selectinload(Exercicio.secao),
    selectinload(Exercicio.palavras).selectinload(PalavraExercicio.palavra),
    selectinload(Exercicio.prox_exercicio),
)


class ExercicioDAO:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def listar_todos(self) -> Sequence[Exercicio]:
        stmt = select(Exercicio).options(*opt)

        return self.session.scalars(stmt).all()

    def listar_por_secao(self, secao: int) -> Sequence[Exercicio]:
        stmt = (
            select(Exercicio)
            .where(Exercicio.id_secao == secao)
            .options(*opt)
            .order_by(Exercicio.id_exercicio)
        )

        return self.session.scalars(stmt).all()

    def listar_por_nome(self, nome: str) -> Sequence[Exercicio]:
        stmt = select(Exercicio).where(Exercicio.titulo == nome).options(*opt)

        return self.session.scalars(stmt).all()

    def listar_status_exercicios(
        self, exercicios: Sequence[Exercicio], id_usuario: int
    ) -> dict[int, ExercicioStatus]:
        exercicio_ids = [e.id_exercicio for e in exercicios]

        if exercicio_ids:
            stmt = select(ExercicioUsuario.id_exercicio, ExercicioUsuario.status).where(
                ExercicioUsuario.id_usuario == id_usuario,
                ExercicioUsuario.id_exercicio.in_(exercicio_ids),
            )

            resultados_status = self.session.execute(stmt).all()
            status = {col.id_exercicio: col.status for col in resultados_status}

        return status

    def listar_exercicio_usuario(
        self, exercicio: Exercicio, usuario: int
    ) -> ExercicioUsuario | None:
        stmt = select(ExercicioUsuario).where(
            ExercicioUsuario.id_usuario == usuario,
            ExercicioUsuario.exercicio == exercicio,
        )

        return self.session.scalar(stmt)

    def alterar_exercicio_usuario(
        self, progresso: ExercicioUsuario, status: ExercicioStatus
    ):
        progresso.status = status
        self.session.add(progresso)
        self.session.commit()

    def criar_exercicio_usuario(
        self, exercicio: Exercicio, usuario: Usuario, status: ExercicioStatus
    ) -> ExercicioUsuario:
        progresso = ExercicioUsuario(status, usuario, exercicio)
        self.session.add(progresso)
        self.session.commit()

        return progresso

    def tentativa_exercicio(self, exercicio: Exercicio, usuario: Usuario):
        progresso_usuario = self.listar_exercicio_usuario(exercicio, usuario.id_usuario)
        if progresso_usuario:
            if progresso_usuario.status not in (
                ExercicioStatus.COMPLETO,
                ExercicioStatus.ABERTO,
            ):
                self.alterar_exercicio_usuario(
                    progresso_usuario, ExercicioStatus.ABERTO
                )
        else:
            self.criar_exercicio_usuario(exercicio, usuario, ExercicioStatus.ABERTO)

    def completar_exercicio(self, exercicio: Exercicio, usuario: Usuario):
        progresso_usuario = self.listar_exercicio_usuario(exercicio, usuario.id_usuario)
        if progresso_usuario:
            if progresso_usuario.status != ExercicioStatus.COMPLETO:
                self.alterar_exercicio_usuario(
                    progresso_usuario, ExercicioStatus.COMPLETO
                )
        else:
            self.criar_exercicio_usuario(exercicio, usuario, ExercicioStatus.COMPLETO)
