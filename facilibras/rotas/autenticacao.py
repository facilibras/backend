from fastapi import APIRouter

from facilibras.dependencias.autenticacao import T_OAuth2
from facilibras.dependencias.controladores import T_AutenticacaoControle
from facilibras.schemas import CriarUsuario, LoginSchema, Token, UsuarioSchema

router = APIRouter(tags=["autenticação"])


@router.post("/login", response_model=Token)
def login(dados: T_OAuth2, controlador: T_AutenticacaoControle):
    dados_login = LoginSchema(nome=dados.username, senha=dados.password)
    return controlador.autenticar_usuario(dados_login)


@router.post("/registrar", response_model=UsuarioSchema)
def registrar(usuario: CriarUsuario, controlador: T_AutenticacaoControle):
    return controlador.registrar_usuario(usuario)
