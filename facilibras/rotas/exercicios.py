from fastapi import APIRouter, File, UploadFile

from facilibras.dependencias.controladores import T_ExercicioControle

router = APIRouter(prefix="/exercicios", tags=["exercícios"])


@router.get("/")
def listar_exercicios(controle: T_ExercicioControle):
    return controle.listar_exercicios()


@router.get("/{exercicio}")
def pagina_exercicio(exercicio: str, controle: T_ExercicioControle):
    ...

@router.post("/{exercicio}/reconhecer")
def reconhecer_exercicio(
    exercicio: str,
    controle: T_ExercicioControle,
    video: UploadFile = File(...),
):
    if not video.content_type or not video.content_type.startswith('video/'):
        return "O arquivo enviado não parece ser um vídeo."
    return "Vídeo recebido com sucesso."

@router.get("/categorias")
def listar_categorias(controle: T_ExercicioControle):
    return ["Alfabeto", "Números"]


@router.get("/categorias/{categoria}")
def listar_por_categoria(categoria: str, controle: T_ExercicioControle):
    return [f"{categoria}_1", f"{categoria}_2", f"{categoria}_3"]
