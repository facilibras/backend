from facilibras.schemas.base_schema import BaseSchema as BaseSchema  # noqa: I001

from facilibras.schemas.autenticacao import Token as Token

from facilibras.schemas.exercicios import (
    ExercicioSchema as ExercicioSchema,
)
from facilibras.schemas.exercicios import (
    FeedbackExercicioSchema as FeedbackExercicioSchema,
)
from facilibras.schemas.exercicios import (
    PalavraSchema as PalavraSchema,
)
from facilibras.schemas.exercicios import (
    SecaoSchema as SecaoSchema,
)
from facilibras.schemas.generico import MensagemSchema as MensagemSchema

from facilibras.schemas.usuario import CriarUsuario as CriarUsuario
from facilibras.schemas.usuario import LoginSchema as LoginSchema
from facilibras.schemas.usuario import UsuarioSchema as UsuarioSchema
from facilibras.schemas.perfil import AtualizarPerfilSchema as AtualizarPerfilSchema
from facilibras.schemas.ranking import Periodo as Periodo
from facilibras.schemas.ranking import RankingSchema as RankingSchema
