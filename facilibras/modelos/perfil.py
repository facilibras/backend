from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Sequence, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Usuario


@registro_tabelas.mapped_as_dataclass
class Perfil:
    __tablename__ = "tb_perfis"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=func.next_value(Sequence("sq_perfis"))
    )

    usuario_id: Mapped[int] = mapped_column(ForeignKey("tb_usuarios.id"), init=False)
    apelido: Mapped[str] = mapped_column()
    url_img_perfil: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    url_img_fundo: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)

    criado_em: Mapped[datetime] = mapped_column(
        TIMESTAMP, init=False, default=func.now()
    )

    qtd_ex_completos: Mapped[int] = mapped_column(default=0)

    usuario: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="perfil", init=False
    )
