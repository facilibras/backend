from fastapi import APIRouter, Depends

from facilibras.controladores import ExercicioControle

router = APIRouter(tags=["exercícios"])


@router.post("/exercicios")
def listar_exercicios(controle: ExercicioControle = Depends()):
    return controle.listar_exercicios()
