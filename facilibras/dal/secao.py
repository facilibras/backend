from sqlalchemy import and_, func, select

from facilibras.dependencias.db import T_Session
from facilibras.modelos import Exercicio, Secao


class SecaoDAO:
    """Classe de acesso de dados no contexto de seções."""

    def __init__(self, session: T_Session) -> None:
        self.session = session

    def listar_por_nome(self, nome: str) -> Secao | None:
        """Buscar exercício pelo nome."""

        return self.session.scalar(select(Secao).where(Secao.nome == nome))

    def listar_todas_com_quantidade(self) -> list[tuple[Secao, int]]:
        """Listar seções."""

        stmt = (
            select(Secao, func.count(Exercicio.id).label("qtd"))
            .select_from(Secao)
            .outerjoin(
                Exercicio,
                and_(
                    Secao.id == Exercicio.secao_id,
                    Exercicio.eh_variacao.is_(False),
                ),
            )
            .group_by(Secao.id)
            .order_by(Secao.nome)
        )

        resultados = self.session.execute(stmt).all()
        return [(col.Secao, col.qtd) for col in resultados]
