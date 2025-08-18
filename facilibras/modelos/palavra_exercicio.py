from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Palavra, Exercicio


@registro_tabelas.mapped_as_dataclass
class PalavraExercicio:
    __tablename__ = "tb_palavras_exercicios"

    palavra_id: Mapped[int] = mapped_column(
        ForeignKey("tb_palavras.id"), 
        primary_key=True)
    
    exercicio_id: Mapped[int] = mapped_column(
        ForeignKey("tb_exercicios.id"), 
        primary_key=True)

    # Acesso reverso
    # palavra: Mapped["Palavra"] = relationship(back_populates="palavra_exercicio")
    # exercicio: Mapped["Exercicio"] = relationship(back_populates="palavra_exercicio")