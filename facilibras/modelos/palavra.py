from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column

from facilibras.config.db import registro_tabelas

@registro_tabelas.mapped_as_dataclass
class Palavra:
    __tablename__ = "tb_palavras"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    url_video: Mapped[str]