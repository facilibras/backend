from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from facilibras.config.db import get_db_session
from facilibras.modelos import Usuario
from facilibras.schemas import CriarUsuario, UsuarioSchema

router = APIRouter(tags=["autenticação"])


T_Session = Annotated[Session, Depends(get_db_session)]


@router.post("/login")
def login(): ...


@router.post("/registrar", response_model=UsuarioSchema)
def registrar(usuario: CriarUsuario, session: T_Session): 
    # TODO: Mover para controlador e usar hash na senha
    # Checa se o usuário já está cadastrado
    mesmo_nome = session.scalar(select(Usuario).where(Usuario.nome == usuario.nome))
    if mesmo_nome:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Usuário já registrado, utilize outro nome',
        )
    
    # Registra usuário no banco de dados
    novo_usuario = Usuario(nome=usuario.nome, senha=usuario.senha)
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario
