from typing import Annotated

from fastapi import Depends

from facilibras.controladores import AutenticacaoControle, ExercicioControle

T_AutenticacaoControle = Annotated[AutenticacaoControle, Depends(AutenticacaoControle)]
T_ExercicioControle = Annotated[ExercicioControle, Depends(ExercicioControle)]
