from fastapi import APIRouter, File, UploadFile

from facilibras.dependencias.controladores import T_ExercicioControle
from facilibras.dependencias.usuario import T_UsuarioOpcional
from facilibras.schemas import ExercicioSchema, FeedbackExercicioSchema

router = APIRouter(prefix="/exercicios", tags=["exercícios"])


@router.get("/test")
def test(usuario: T_UsuarioOpcional):
    if usuario:
        return {"mensagem": f"Olá, {usuario['nome']}! Você está autenticado."}
    return {"mensagem": "Olá, visitante! Você não está autenticado."}


@router.get("/secoes")
def listar_secoes(controle: T_ExercicioControle):
    return controle.listar_secoes()


@router.get("/secoes/{secao}", response_model=list[ExercicioSchema])
def listar_por_secao(
    secao: str, controle: T_ExercicioControle, usuario: T_UsuarioOpcional
):
    usuario_id = usuario["id"] if usuario else None
    return controle.listar_exercicios_por_secao(secao, usuario_id)


@router.get("/", response_model=list[ExercicioSchema])
def listar_exercicios(controle: T_ExercicioControle, usuario: T_UsuarioOpcional):
    usuario_id = usuario["id"] if usuario else None
    return controle.listar_exercicios(usuario_id)


@router.get("/{exercicio}")
def pagina_exercicio(
    exercicio: str, controle: T_ExercicioControle, usuario: T_UsuarioOpcional,
):
    usuario_id = usuario["id"] if usuario else None
    return controle.listar_exercicio_por_nome(exercicio, usuario_id)


@router.post("/{exercicio}/reconhecer", response_model=FeedbackExercicioSchema)
def reconhecer_exercicio(
    exercicio: str,
    controle: T_ExercicioControle,
    usuario: T_UsuarioOpcional,
    video: UploadFile = File(...),
):
    usuario_id = usuario["id"] if usuario else None
    return controle.reconhecer_exercicio(exercicio, video, usuario_id)
