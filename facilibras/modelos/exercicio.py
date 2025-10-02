from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Secao, ProgressoUsuario, Palavra

@registro_tabelas.mapped_as_dataclass
class Exercicio:
    __tablename__ = "tb_exercicios"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        init=False)
    
    secao_id: Mapped[int] = mapped_column(ForeignKey("tb_secoes.id"))
    
    titulo: Mapped[str]
    
    descricao: Mapped[str]
    
    prox_exercicio: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tb_exercicios.id"),
        nullable=True)

    # Acesso reverso
    proximo: Mapped["Exercicio"] = relationship()
    progressos_usuarios: Mapped[list["ProgressoUsuario"]] = relationship(back_populates="exercicio")
    secao: Mapped["Secao"] = relationship(back_populates="exercicios")
    palavras: Mapped[list["Palavra"]] = relationship(
        secondary="tb_palavras_exercicios",
        back_populates="exercicios")