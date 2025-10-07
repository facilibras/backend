from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Exercicio, Palavra


@registro_tabelas.mapped_as_dataclass
class PalavraExercicio:
    __tablename__ = "tb_palavras_exercicios"

    palavra_id: Mapped[int] = mapped_column(
        ForeignKey("tb_palavras.id"), primary_key=True, init=False
    )

    exercicio_id: Mapped[int] = mapped_column(
        ForeignKey("tb_exercicios.id"), primary_key=True, init=False
    )

    palavra: Mapped["Palavra"] = relationship(back_populates="exercicios")
    exercicio: Mapped["Exercicio"] = relationship(back_populates="palavras")

    @property
    def nome_palavra(self) -> str:
        return self.palavra.nome
