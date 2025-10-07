from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from facilibras.dependencias.db import T_Session
from facilibras.modelos import (
    Exercicio,
    ExercicioStatus,
    PalavraExercicio,
    ProgressoUsuario,
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
            .where(Exercicio.secao_id == secao)
            .options(*opt)
            .order_by(Exercicio.id)
        )

        return self.session.scalars(stmt).all()

    def listar_por_nome(self, nome: str) -> Sequence[Exercicio]:
        stmt = select(Exercicio).where(Exercicio.titulo == nome).options(*opt)

        return self.session.scalars(stmt).all()

    def listar_status_exercicios(
        self, exercicios: Sequence[Exercicio], id_usuario: int
    ) -> dict[int, ExercicioStatus]:
        exercicio_ids = [e.id for e in exercicios]

        if exercicio_ids:
            stmt = select(ProgressoUsuario).where(
                ProgressoUsuario.usuario_id == id_usuario,
                ProgressoUsuario.usuario_id.in_(exercicio_ids),
            )

            resultados_status = self.session.execute(stmt).all()
            status = {col.exercicio_id: col.status for col in resultados_status}

        return status

    def listar_exercicio_usuario(
        self, exercicio: Exercicio, usuario: int
    ) -> ProgressoUsuario | None:
        stmt = select(ProgressoUsuario).where(
            ProgressoUsuario.usuario_id == usuario,
            ProgressoUsuario.exercicio == exercicio,
        )

        return self.session.scalar(stmt)

    def alterar_exercicio_usuario(
        self, progresso: ProgressoUsuario, status: ExercicioStatus
    ):
        progresso.status = status
        self.session.add(progresso)
        self.session.commit()

    def criar_exercicio_usuario(
        self, exercicio: Exercicio, usuario: Usuario, status: ExercicioStatus
    ) -> ProgressoUsuario:
        progresso = ProgressoUsuario(
            status=status, usuario=usuario, exercicio=exercicio
        )

        self.session.add(progresso)
        self.session.commit()

        return progresso

    def tentativa_exercicio(self, exercicio: Exercicio, usuario: Usuario):
        progresso_usuario = self.listar_exercicio_usuario(exercicio, usuario.id)
        if progresso_usuario:
            if progresso_usuario.status not in (
                ExercicioStatus.COMPLETO,
                ExercicioStatus.INCOMPLETO,
            ):
                self.alterar_exercicio_usuario(
                    progresso_usuario, ExercicioStatus.INCOMPLETO
                )
        else:
            self.criar_exercicio_usuario(exercicio, usuario, ExercicioStatus.INCOMPLETO)

    def completar_exercicio(self, exercicio: Exercicio, usuario: Usuario):
        progresso_usuario = self.listar_exercicio_usuario(exercicio, usuario.id)
        if progresso_usuario:
            if progresso_usuario.status != ExercicioStatus.COMPLETO:
                self.alterar_exercicio_usuario(
                    progresso_usuario, ExercicioStatus.COMPLETO
                )
        else:
            self.criar_exercicio_usuario(exercicio, usuario, ExercicioStatus.COMPLETO)
