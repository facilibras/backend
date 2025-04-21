from fastapi import APIRouter, File, UploadFile

from facilibras.dependencias.controladores import T_ExercicioControle
from facilibras.schemas import FeedbackExercicioSchema, ExercicioSchema

router = APIRouter(prefix="/exercicios", tags=["exercícios"])


@router.get("/", response_model=list[ExercicioSchema])
def listar_exercicios(controle: T_ExercicioControle):
    return controle.listar_exercicios(None)


@router.get("/{exercicio}")
def pagina_exercicio(exercicio: str, controle: T_ExercicioControle):
    return controle.listar_exercicio_por_nome(exercicio, None)


@router.post("/{exercicio}/reconhecer", response_model=FeedbackExercicioSchema)
def reconhecer_exercicio(
    exercicio: str,
    controle: T_ExercicioControle,
    video: UploadFile = File(...),
):
    return controle.reconhecer_exercicio(exercicio, video, None)


@router.get("/secoes")
def listar_secoes(controle: T_ExercicioControle):
    return controle.listar_secoes()


@router.get("/secoes/{secao}")
def listar_por_secao(secao: str, controle: T_ExercicioControle):
    return controle.listar_exercicios_por_secao(secao, None)
