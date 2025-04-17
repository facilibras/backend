from typing import Annotated

from fastapi import Depends

from facilibras.dal import ExercicioDAO as ExercicioDAO
from facilibras.dal import UsuarioDAO as UsuarioDAO

T_ExercicioDAO = Annotated[ExercicioDAO, Depends(ExercicioDAO)]
T_UsuarioDAO = Annotated[UsuarioDAO, Depends(UsuarioDAO)]
