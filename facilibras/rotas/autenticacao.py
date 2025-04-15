from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from facilibras.config.db import get_db_session
from facilibras.controladores import AutenticacaoControle
from facilibras.schemas import CriarUsuario, LoginSchema, Token, UsuarioSchema

router = APIRouter(tags=["autenticação"])


OAuth2 = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]
T_AutenticacaoControle = Annotated[AutenticacaoControle, Depends(AutenticacaoControle)]
T_Session = Annotated[Session, Depends(get_db_session)]


@router.post("/login", response_model=Token)
def login(
    dados: OAuth2,
    controlador: T_AutenticacaoControle,
    session: T_Session,
):
    dados_login = LoginSchema(nome=dados.username, senha=dados.password)
    return controlador.autenticar_usuario(dados_login, session)


@router.post("/registrar", response_model=UsuarioSchema)
def registrar(
    usuario: CriarUsuario, controlador: T_AutenticacaoControle, session: T_Session
):
    return controlador.registrar_usuario(usuario, session)
