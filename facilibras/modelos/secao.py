from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos.exercicio import Exercicio


@registro_tabelas.mapped_as_dataclass
class Secao:
    __tablename__ = "tb_secoes"

    id: Mapped[int] = mapped_column(
        init=False, 
        primary_key=True)
    
    nome: Mapped[str]

    descricao: Mapped[Optional[str]]

    # exercicios: Mapped[list["Exercicio"]] = relationship(back_populates="exercicio")