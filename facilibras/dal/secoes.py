from sqlalchemy import func, select

from facilibras.dependencias.db import T_Session
from facilibras.modelos import Exercicio, Secao


class SecaoDAO:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    def listar_por_nome(self, nome: str) -> Secao | None:
        return self.session.scalar(select(Secao).where(Secao.titulo == nome))

    def listar_todas_com_quantidade(self) -> list[tuple[Secao, int]]:
        stmt = (
            select(Secao, func.count(Exercicio.id_exercicio).label("qtd"))
            .select_from(Secao)
            .outerjoin(Exercicio, Secao.id_secao == Exercicio.id_secao)
            .group_by(Secao.id_secao)
            .order_by(Secao.titulo)
        )

        resultados = self.session.execute(stmt).all()
        return [(col.Secao, col.qtd) for col in resultados]
