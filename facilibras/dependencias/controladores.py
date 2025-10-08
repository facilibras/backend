from typing import Annotated

from fastapi import Depends

from facilibras.controladores import (
    AutenticacaoControle,
    ExercicioControle,
    PerfilControle,
    RankingControle,
)

T_AutenticacaoControle = Annotated[AutenticacaoControle, Depends(AutenticacaoControle)]
T_ExercicioControle = Annotated[ExercicioControle, Depends(ExercicioControle)]
T_RankingControle = Annotated[RankingControle, Depends(RankingControle)]
T_PerfilControle = Annotated[PerfilControle, Depends(PerfilControle)]
