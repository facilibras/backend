from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Usuario, Palavra

@registro_tabelas.mapped_as_dataclass
class Exercicio:
    __tablename__ = "tb_exercicios"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    secao_id: Mapped[int] = mapped_column(ForeignKey("tb_secoes.id"))
    titulo: Mapped[str]
    prox_exercicio: Mapped[int] = mapped_column(ForeignKey("tb_exercicios.id"))

    # Acesso reverso
    usuarios: Mapped[list["Usuario"]]
    palavras: Mapped[list["Palavra"]]