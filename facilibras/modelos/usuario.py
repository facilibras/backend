from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from facilibras.config.db import registro_tabelas


@registro_tabelas.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    data_registro: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

@registro_tabelas.mapped_as_dataclass
class Tarefas:
    __tablename__ = "tarefas"

    id_tareafa: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_secao: Mapped[int]
    titulo: Mapped[str]
    descricao: Mapped[str]
    id_prox_tarefa: Mapped[int] = mapped_column(init=False, default=None)

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

@registro_tabelas.mapped_as_dataclass
class Acoes:
    __tablename__ = "acoes"

    id_acao: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_palavra: Mapped[int]
    nome: Mapped[str]
    funcoes: Mapped[str]

@registro_tabelas.mapped_as_dataclass
class AcoesPalavras:
    __tablename__ = "acoes_palavras"

    id_acao_palavra: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_acao: Mapped[int]
    id_palavra: Mapped[int]

@registro_tabelas.mapped_as_dataclass
class PalavrasTarefas:
    __tablename__ = "palavras_tarefas"

    id_palavra_tarefa: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_palavra: Mapped[int]
    id_tarefa: Mapped[int]

@registro_tabelas.mapped_as_dataclass
class TarefasUsuario:
    __tablename__ = "tarefas_usuarios"

    id_tarefa_usuario: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_usuario: Mapped[int]
    id_tarefa: Mapped[int]
    status: Mapped[str]