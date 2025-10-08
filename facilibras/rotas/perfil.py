from fastapi import APIRouter

from facilibras.dependencias.controladores import T_PerfilControle

router = APIRouter(tags=["perfil"])


@router.get("/perfil/{id_usuario}")
def listar_perfil(id_usuario: int, controle: T_PerfilControle):
    return controle.listar_perfil(id_usuario)
