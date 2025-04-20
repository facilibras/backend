from typing import Sequence

from sqlalchemy import select

from facilibras.dependencias.db import T_Session
from facilibras.modelos import Usuario


class ExercicioDAO:
    """
    Substituir por Tarefas, está Usuário somente para testar
    """
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def listar(self) -> Sequence[Usuario]:
        return self.session.scalars(select(Usuario)).all()

    def listar_por_categoria(self, categoria: str, usuario: str) -> Sequence[Usuario]:
        ...

    def listar_categorias(self) -> Sequence[Usuario]:
        ...
