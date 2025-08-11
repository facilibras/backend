from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import PalavraExercicio


@registro_tabelas.mapped_as_dataclass
class Palavra:
    __tablename__ = "tb_palavras"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    url_video: Mapped[str]

    palavra_exercicio: Mapped[list["PalavraExercicio"]] = relationship(back_populates="palavra")