from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP, VARCHAR

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Exercicio, Usuario


class ExercicioStatus(str, Enum):
    INCOMPLETO = "I"
    COMPLETO = "C"


@registro_tabelas.mapped_as_dataclass
class ProgressoUsuario:
    __tablename__ = "tb_progresso_usuarios"

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("tb_usuarios.id"), primary_key=True, init=False
    )

    exercicio_id: Mapped[int] = mapped_column(
        ForeignKey("tb_exercicios.id"), primary_key=True, init=False
    )

    # Acesso Reverso
    usuario: Mapped["Usuario"] = relationship(back_populates="progressos_exercicios")
    exercicio: Mapped["Exercicio"] = relationship(back_populates="progressos_usuarios")

    qtd_ex_completos: Mapped[int] = mapped_column(default=0, init=False)
    criado_em: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), init=False
    )

    status: Mapped[ExercicioStatus] = mapped_column(
        VARCHAR, default=ExercicioStatus.INCOMPLETO
    )
