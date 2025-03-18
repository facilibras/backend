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
