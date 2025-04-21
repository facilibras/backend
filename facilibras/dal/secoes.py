from typing import Sequence

from sqlalchemy import select

from facilibras.dependencias.db import T_Session
from facilibras.modelos import Secao


class SecaoDAO:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def listar_por_nome(self, nome: str) -> Secao | None:
        return self.session.scalar(select(Secao).where(Secao.titulo == nome))

    def listar_todas(self) -> Sequence[Secao]:
        return self.session.scalars(select(Secao)).all()
