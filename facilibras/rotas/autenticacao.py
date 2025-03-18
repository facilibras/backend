from fastapi import APIRouter

from facilibras.schemas.usuario import Usuario

router = APIRouter(tags=["autenticação"])


@router.post("/login")
def login(): ...


@router.post("/registrar")
def registrar(usuario: Usuario):
    return {"message": "Registrado"}
