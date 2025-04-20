from datetime import datetime

from typing import Optional

from enum import Enum

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facilibras.config.db import registro_tabelas

class ExercicioStatus(str, Enum):
    aberto = "A"
    completo = "C"


@registro_tabelas.mapped_as_dataclass
class Usuarios:
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    apelido:  Mapped[Optional[str]] = mapped_column(unique=True)

    img_url_perfil: Mapped[Optional[str]]
    img_url_fundo:  Mapped[Optional[str]]

    hash_senha: Mapped[str]

    email: Mapped[str]
    # email_confirmado: Mapped[bool]
    # email_token: Mapped[str]

    registro_em: Mapped[datetime] = mapped_column(
        init=False, 
        server_default=func.now()
    )

    atualizado_em: Mapped[Optional[datetime]]
    inativo_em: Mapped[Optional[datetime]]
    ultimo_login: Mapped[Optional[datetime]]


@registro_tabelas.mapped_as_dataclass
class Secoes:
    __tablename__ = "secoes"

    id_secao: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str]
    descricao: Mapped[str]


@registro_tabelas.mapped_as_dataclass
class Palavras:
    __tablename__ = "palavras"

    id_palavra: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    url_video: Mapped[str]

@registro_tabelas.mapped_as_dataclass
class Exercicios:
    __tablename__ = "exercicios"

    id_exercicio: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_secao: Mapped[int] = mapped_column(ForeignKey("secoes.id_secao"))
    titulo: Mapped[str]
    descricao: Mapped[str]
    id_prox_tarefa: Mapped[Optional[int]] = mapped_column(init=False, default=None)


@registro_tabelas.mapped_as_dataclass
class PalavrasExercicios:
    __tablename__ = "palavras_exercicios"

    id_palavra: Mapped[int] = mapped_column(ForeignKey("palavras.id_palavra"), init=False, primary_key=True)
    id_exercicio: Mapped[int] = mapped_column(ForeignKey("exercicios.id_exercicio"), init=False, primary_key=True)

    palavras: Mapped[list["Palavras"]] = relationship(back_populates="palavras")
    exercicios: Mapped[list["Exercicios"]] = relationship(back_populates="exercicios")


@registro_tabelas.mapped_as_dataclass
class ExerciciosUsuario:
    __tablename__ = "exercicios_usuarios"

    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), init=False, primary_key=True)
    id_exercicio: Mapped[int] = mapped_column(ForeignKey("exercicio.id_exercicio"), init=False, primary_key=True)
    status: Mapped[ExercicioStatus]

    usuario: Mapped["Usuario"] = relationship(back_populates="usuarios")
    exercicios: Mapped[list["Exercicios"]] = relationship(back_populates="exercicios")