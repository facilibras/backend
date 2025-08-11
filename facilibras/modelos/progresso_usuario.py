from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP

from facilibras.config.db import registro_tabelas

if TYPE_CHECKING:
    from facilibras.modelos import Usuario, Exercicio

class ExercicioStatus(str, Enum):
    INCOMPLETO = "I"
    COMPLETO = "C"

@registro_tabelas.mapped_as_dataclass
class ProgressoUsuario:
    __tablename__ = "tb_progresso_usuarios"

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey('tb_usuarios.id'), 
        primary_key=True)
    
    exercicio_id: Mapped[int] = mapped_column(
        ForeignKey('tb_exercicios.id'), 
        primary_key=True)
    
    criado_em: Mapped[TIMESTAMP]
    
    status = Mapped[ExercicioStatus]

    # Acesso Reverso
    usuario: Mapped["Usuario"] = relationship(back_populates="exercicios")
    exercicio: Mapped["Exercicio"] = relationship(back_populates="usuarios")

    def __init__(self, status, usuario_id, exercicio_id):
        self.usuario_id = usuario_id
        self.exercicio_id = exercicio_id
        self.status = status