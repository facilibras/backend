from datetime import datetime

from sqlalchemy import func, select

from facilibras.dependencias.db import T_Session
from facilibras.modelos import (
    Conquista,
    ExercicioStatus,
    Perfil,
    ProgressoUsuario,
    Usuario,
)


class UsuarioDAO:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def criar(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.session.query(Usuario).filter_by(email=email).one_or_none()

    def buscar_por_id(self, id_usuario: int) -> Usuario | None:
        return self.session.query(Usuario).filter_by(id=id_usuario).one_or_none()

    def buscar_por_username(self, nome_usuario) -> Usuario | None:
        return (
            self.session.query(Usuario)
            .filter_by(nome_usuario=nome_usuario)
            .one_or_none()
        )

    def buscar_perfil_usuario(self, id_usuario: int) -> Perfil | None:
        return self.session.query(Perfil).filter_by(usuario_id=id_usuario).one_or_none()

    def listar_conquistas_usuario(self, id_usuario: int) -> list[Conquista]:
        return self.session.query(Conquista).filter_by(perfil_id=id_usuario).all()

    def atualizar_progresso(
        self, perfil, nivel, pontos_nivel, pontos_total, qtd_sinais
    ):
        perfil.qtd_ex_completos = qtd_sinais
        perfil.nivel = nivel
        perfil.pontos_total = pontos_total
        perfil.pontos_nivel = pontos_nivel

        self.session.commit()

    def alterar_perfil_usuario(self, perfil) -> Perfil: ...

    def ranking_com_perfil(self, inicio: datetime | None = None):
        stmt = (
            select(
                Usuario.id.label("usuario_id"),
                Perfil.apelido,
                Perfil.url_img_perfil,
                Perfil.qtd_ex_completos,
                Perfil.pontos_total,
            )
            .join(ProgressoUsuario, ProgressoUsuario.usuario_id == Usuario.id)
            .join(Perfil, Perfil.id == Usuario.id)
            .where(ProgressoUsuario.status == ExercicioStatus.COMPLETO)
        )

        if inicio:
            stmt = stmt.where(ProgressoUsuario.criado_em >= inicio)

        stmt = stmt.group_by(Usuario.id, Perfil.id)
        stmt = stmt.order_by(func.count(ProgressoUsuario.exercicio_id).desc())

        return self.session.execute(stmt).all()
