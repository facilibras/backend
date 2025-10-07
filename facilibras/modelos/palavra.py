from typing import TYPE_CHECKING

from sqlalchemy import Sequence, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import PalavraExercicio


@registro_tabelas.mapped_as_dataclass
class Palavra:
    __tablename__ = "tb_palavras"

    id: Mapped[int] = mapped_column(
        primary_key=True, default=func.next_value(Sequence("sq_palavras")), init=False
    )
    nome: Mapped[str]
    instrucoes: Mapped[str]
    url_video: Mapped[str]

    exercicios: Mapped[list["PalavraExercicio"]] = relationship(
        back_populates="palavra", default_factory=list, cascade="all, delete-orphan"
    )
