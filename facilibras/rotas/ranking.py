from fastapi import APIRouter, Query

from facilibras.dependencias.controladores import T_RankingControle
from facilibras.schemas import Periodo, RankingSchema

router = APIRouter(tags=["ranking"])


@router.get("/ranking", response_model=RankingSchema)
def get_ranking(
    controle: T_RankingControle, periodo: Periodo = Query(default=Periodo.all)
):
    return controle.listar_ranking(periodo)
