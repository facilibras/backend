from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Usuario


@registro_tabelas.mapped_as_dataclass
class Secao:
    __tablename__ = "secoes"

    id_secao: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str]
    descricao: Mapped[str]

    exercicios: Mapped[list["Exercicio"]] = relationship(
        init=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


@registro_tabelas.mapped_as_dataclass
class Palavra:
    __tablename__ = "palavras"

    id_palavra: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    url_video: Mapped[str]

    # Acesso reverso
    exercicios: Mapped[list["PalavraExercicio"]] = relationship(
        back_populates="palavra", default_factory=list, cascade="all, delete-orphan"
    )


@registro_tabelas.mapped_as_dataclass
class Exercicio:
    __tablename__ = "exercicios"

    id_exercicio: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_secao: Mapped[int] = mapped_column(ForeignKey("secoes.id_secao"), init=False)
    id_prox_exercicio: Mapped[Optional[int]] = mapped_column(
        ForeignKey("exercicios.id_exercicio"), init=False, default=None
    )

    titulo: Mapped[str]
    descricao: Mapped[str]

    # Acesso reverso
    prox_exercicio: Mapped[Optional["Exercicio"]] = relationship(
        remote_side=[id_exercicio], init=False, default=None
    )
    secao: Mapped["Secao"] = relationship(back_populates="exercicios")
    palavras: Mapped[list["PalavraExercicio"]] = relationship(
        back_populates="exercicio", default_factory=list, cascade="all, delete-orphan"
    )
    usuario_progressos: Mapped[list["ExercicioUsuario"]] = relationship(
        back_populates="exercicio", default_factory=list, cascade="all, delete-orphan"
    )


@registro_tabelas.mapped_as_dataclass
class PalavraExercicio:
    __tablename__ = "palavras_exercicios"

    id_palavra: Mapped[int] = mapped_column(
        ForeignKey("palavras.id_palavra"), init=False, primary_key=True
    )
    id_exercicio: Mapped[int] = mapped_column(
        ForeignKey("exercicios.id_exercicio"), init=False, primary_key=True
    )

    palavra: Mapped["Palavra"] = relationship(back_populates="exercicios")
    exercicio: Mapped["Exercicio"] = relationship(back_populates="palavras")

    @property
    def nome_palavra(self) -> str:
        return self.palavra.nome


class ExercicioStatus(str, Enum):
    ABERTO = "A"
    COMPLETO = "C"


@registro_tabelas.mapped_as_dataclass
class ExercicioUsuario:
    __tablename__ = "exercicios_usuarios"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"), init=False, primary_key=True
    )
    id_exercicio: Mapped[int] = mapped_column(
        ForeignKey("exercicios.id_exercicio"), init=False, primary_key=True
    )
    status: Mapped[ExercicioStatus]

    # Acesso Reverso
    usuario: Mapped["Usuario"] = relationship(back_populates="exercicio_progressos")
    exercicio: Mapped["Exercicio"] = relationship(back_populates="usuario_progressos")
