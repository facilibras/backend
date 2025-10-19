from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Perfil


class NomeConquista(Enum):
    PRIMEIRO_SINAL = "Primeiro Sinal"
    ALFABETO = "Alfabeto"
    NUMEROS = "Números"
    OUTROS = "Outros"
    FRASES = "Frases"
    ALIMENTOS = "Alimentos"
    VERBOS = "Verbos"
    SAUDACOES = "Saudações"
    IDENTIDADE = "Identidade"


@registro_tabelas.mapped_as_dataclass
class Conquista:
    __tablename__ = "tb_conquistas"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    perfil_id: Mapped[int] = mapped_column(ForeignKey("tb_perfis.id"), init=False)
    nome: Mapped["NomeConquista"] = mapped_column(SQLEnum(NomeConquista))
    descricao: Mapped[Optional[str]] = mapped_column(nullable=True)
    data_conquista: Mapped[datetime] = mapped_column(default=func.now())

    perfil: Mapped["Perfil"] = relationship(
        "Perfil", back_populates="conquistas", init=False
    )
