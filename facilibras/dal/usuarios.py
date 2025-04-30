from sqlalchemy import select

from facilibras.dependencias.db import T_Session
from facilibras.modelos import Usuario


class UsuarioDAO:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def criar(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.session.scalar(select(Usuario).where(Usuario.email == email))

    def buscar_por_id(self, id_usuario: int) -> Usuario | None:
        return self.session.scalar(
            select(Usuario).where(Usuario.id_usuario == id_usuario)
        )
