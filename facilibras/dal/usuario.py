from facilibras.dependencias.db import T_Session
from facilibras.modelos import Conquista, Perfil, Usuario


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

    def alterar_perfil_usuario(self, perfil) -> Perfil: ...
