from fastapi import APIRouter, File, Form, UploadFile

from facilibras.dependencias.controladores import T_PerfilControle
from facilibras.schemas import AtualizarPerfilSchema

router = APIRouter(tags=["perfil"])


@router.get("/perfil/{id_usuario}")
def listar_perfil(id_usuario: int, controle: T_PerfilControle):
    return controle.listar_perfil(id_usuario)


@router.put("/perfil/{id_usuario}")
def atualizar_perfil(
    id_usuario: int,
    controle: T_PerfilControle,
    apelido: str = Form(None),
    cor_img_fundo: str = Form(None),
    arquivo: UploadFile | str | None = File(default=None),
):
    dados = AtualizarPerfilSchema(apelido=apelido, cor_img_fundo=cor_img_fundo)
    return controle.atualizar_perfil(id_usuario, dados, arquivo)


@router.get("/perfil/{id_usuario}/foto")
def foto_do_usuario(id_usuario: int, controle: T_PerfilControle):
    return controle.foto_perfil_usuario(id_usuario)
