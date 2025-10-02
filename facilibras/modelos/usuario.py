from typing import TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, Sequence
from sqlalchemy.types import TEXT, TIMESTAMP

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Perfil, ProgressoUsuario, Exercicio


@registro_tabelas.mapped_as_dataclass
class Usuario:
    __tablename__ = "tb_usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        init=False,
        default=func.next_value(Sequence("sq_usuarios")))
    
    nome_usuario: Mapped[str] = mapped_column(unique=True)
    
    email: Mapped[str] = mapped_column(unique=True)
    
    senha: Mapped[str] = mapped_column(TEXT)
    
    salt: Mapped[str] = mapped_column(TEXT)
    
    criado_em: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        init=False, 
        default=func.now())
    
    ultimo_login: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, 
        nullable=True, 
        init=False)
    
    ativo: Mapped[bool] = mapped_column(
        init=False, 
        default=True)

    # Acesso Reverso
    perfil: Mapped["Perfil"] = relationship(
        back_populates="usuario",
        cascade="delete-orphan")
    
    progressos_exercicios: Mapped[list["ProgressoUsuario"]] = relationship(
        back_populates="usuario", 
        default_factory=list, 
        cascade="all, delete-orphan")