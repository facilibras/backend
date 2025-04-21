from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import ExercicioUsuario


@registro_tabelas.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hash_senha: Mapped[str]

    # Perfil
    apelido: Mapped[Optional[str]] = mapped_column(unique=True, default=None)
    img_url_perfil: Mapped[Optional[str]] = mapped_column(default=None)
    img_url_fundo: Mapped[Optional[str]] = mapped_column(default=None)

    # Controle
    registro_em: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    atualizado_em: Mapped[Optional[datetime]] = mapped_column(default=None)
    inativo_em: Mapped[Optional[datetime]] = mapped_column(default=None)
    ultimo_login: Mapped[Optional[datetime]] = mapped_column(default=None)

    # Acesso Reverso
    exercicio_progressos: Mapped[list["ExercicioUsuario"]] = relationship(
        back_populates="usuario", default_factory=list, cascade="all, delete-orphan"
    )
