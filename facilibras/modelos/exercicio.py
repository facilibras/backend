from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import PalavraExercicio, ProgressoUsuario, Secao


@registro_tabelas.mapped_as_dataclass
class Exercicio:
    __tablename__ = "tb_exercicios"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    secao_id: Mapped[int] = mapped_column(ForeignKey("tb_secoes.id"), init=False)
    prox_exercicio_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tb_exercicios.id"), init=False, default=None
    )

    titulo: Mapped[str]
    descricao: Mapped[str]
    eh_variacao: Mapped[bool]
    nome_variacao: Mapped[str]

    # Acesso reverso
    prox_exercicio: Mapped[Optional["Exercicio"]] = relationship(
        remote_side=[id], init=False, default=None
    )
    secao: Mapped["Secao"] = relationship(back_populates="exercicios")
    progressos_usuarios: Mapped[list["ProgressoUsuario"]] = relationship(
        back_populates="exercicio",
        default_factory=list,
        cascade="all, delete-orphan",
    )
    palavras: Mapped[list["PalavraExercicio"]] = relationship(
        back_populates="exercicio", default_factory=list, cascade="all, delete-orphan"
    )
