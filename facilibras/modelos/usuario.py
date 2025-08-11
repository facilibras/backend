from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP, TEXT

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Perfil, ProgressoUsuario, Exercicio


@registro_tabelas.mapped_as_dataclass
class Usuario:
    __tablename__ = "tb_usuarios"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome_usuario: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    salt: Mapped[str]
    criado_em: Mapped[TIMESTAMP]
    ultimo_login: Mapped[TIMESTAMP]
    ativo: Mapped[bool]

    # Acesso Reverso
    perfil: Mapped["Perfil"] = relationship(
        back_populates="usuario")
    
    exercicios: Mapped[list["ProgressoUsuario"]] = relationship(
        back_populates="usuario", 
        default_factory=list, 
        cascade="all, delete-orphan")
    
    def __init__(self, nome_usuario: str, email: str, senha: str):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha
