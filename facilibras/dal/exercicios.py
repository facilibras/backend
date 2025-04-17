from sqlalchemy import select

from facilibras.dependencias.db import T_Session
from facilibras.modelos import Usuario


class ExercicioDAO:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def listar(self):
        return self.session.scalars(select(Usuario)).all()
