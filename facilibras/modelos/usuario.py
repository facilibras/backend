from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas


class ExercicioStatus(str, Enum):
    aberto = "A"
    completo = "C"


@registro_tabelas.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(init=False, primary_key=True)

    # Login
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hash_senha: Mapped[str]

    # Perfil
    apelido: Mapped[Optional[str]] = mapped_column(unique=True, default=None)
    img_url_perfil: Mapped[Optional[str]] = mapped_column(default=None)
    img_url_fundo: Mapped[Optional[str]] = mapped_column(default=None)

    # Controle
    registro_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[Optional[datetime]] = mapped_column(default=None)
    inativo_em: Mapped[Optional[datetime]] = mapped_column(default=None)
    ultimo_login: Mapped[Optional[datetime]] = mapped_column(default=None)


@registro_tabelas.mapped_as_dataclass
class Secao:
    __tablename__ = "secoes"

    id_secao: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str]
    descricao: Mapped[str]


@registro_tabelas.mapped_as_dataclass
class Palavra:
    __tablename__ = "palavras"

    id_palavra: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    url_video: Mapped[str]


@registro_tabelas.mapped_as_dataclass
class Exercicio:
    __tablename__ = "exercicios"

    id_exercicio: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_secao: Mapped[int] = mapped_column(ForeignKey("secoes.id_secao"))
    titulo: Mapped[str]
    descricao: Mapped[str]
    id_prox_tarefa: Mapped[Optional[int]] = mapped_column(init=False, default=None)


@registro_tabelas.mapped_as_dataclass
class PalavraExercicio:
    __tablename__ = "palavras_exercicios"

    id_palavra: Mapped[int] = mapped_column(
        ForeignKey("palavras.id_palavra"), init=False, primary_key=True
    )
    id_exercicio: Mapped[int] = mapped_column(
        ForeignKey("exercicios.id_exercicio"), init=False, primary_key=True
    )

    palavras: Mapped[list[Palavra]] = relationship(back_populates="palavras")
    exercicios: Mapped[list[Exercicio]] = relationship(back_populates="exercicios")


@registro_tabelas.mapped_as_dataclass
class ExercicioUsuario:
    __tablename__ = "exercicios_usuarios"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"), init=False, primary_key=True
    )
    id_exercicio: Mapped[int] = mapped_column(
        ForeignKey("exercicio.id_exercicio"), init=False, primary_key=True
    )
    status: Mapped[ExercicioStatus]

    usuario: Mapped[Usuario] = relationship(back_populates="usuarios")
    exercicios: Mapped[list[Exercicio]] = relationship(back_populates="exercicios")
