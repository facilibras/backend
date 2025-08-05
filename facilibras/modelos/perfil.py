from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Usuario


@registro_tabelas.mapped_as_dataclass
class Perfil:
    __tablename__ = "tb_perfis"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("tb_usuarios.id"))
    apelido: Mapped[str]
    url_img_perfil: Mapped[str]
    url_img_fundo: Mapped[str]
    criado_em: Mapped[TIMESTAMP]

    # Acesso Reverso
    usuario: Mapped["Usuario"] = relationship(back_populates="perfil")