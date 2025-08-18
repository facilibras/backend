from typing import TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import ForeignKey, func, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP, INTEGER, VARCHAR

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Usuario


@registro_tabelas.mapped_as_dataclass
class Perfil:
    __tablename__ = "tb_perfis"

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
        default=func.next_value(Sequence("sq_perfis")))

    usuario_id: Mapped[int] = mapped_column(ForeignKey("tb_usuarios.id"))
    
    apelido: Mapped[str]

    url_img_perfil: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    url_img_fundo: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    criado_em: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        default=func.now(),
        init=False)

    # Acesso Reverso
    usuario: Mapped["Usuario"] = relationship(back_populates="perfil")