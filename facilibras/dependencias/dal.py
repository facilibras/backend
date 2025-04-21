from typing import Annotated

from fastapi import Depends

from facilibras.dal import ExercicioDAO, SecaoDAO, UsuarioDAO

T_ExercicioDAO = Annotated[ExercicioDAO, Depends(ExercicioDAO)]
T_SecaoDAO = Annotated[SecaoDAO, Depends(SecaoDAO)]
T_UsuarioDAO = Annotated[UsuarioDAO, Depends(UsuarioDAO)]
