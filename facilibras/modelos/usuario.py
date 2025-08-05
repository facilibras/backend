from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP, TEXT

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Perfil, ProgressoUsuario


@registro_tabelas.mapped_as_dataclass
class Usuario:
    __tablename__ = "tb_usuarios"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[TEXT]
    salt: Mapped[TEXT]
    criado_em: Mapped[TIMESTAMP]
    ultimo_login: Mapped[TIMESTAMP]
    ativo: Mapped[bool]

    # Acesso Reverso
    perfil: Mapped["Perfil"] = relationship(back_populates="usuario")
   
    exercicios: Mapped[list["ProgressoUsuario"]] = relationship(
        back_populates="usuario", 
        default_factory=list, 
        cascade="all, delete-orphan"
    )
