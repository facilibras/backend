from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from facilibras.config.env import get_variavel_ambiente
from facilibras.modelos import Usuario
from facilibras.schemas import CriarUsuario, LoginSchema, Token

CHAVE = get_variavel_ambiente("CHAVE", str)
EXPIRACAO_MINUTOS = get_variavel_ambiente("EXPIRACAO_TOKEN", int)
hasher = PasswordHash.recommended()

# Injeção de dependência do JWT
T_Token = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]


def usuario_autenticado(token: T_Token):
    """Retorna o usuário autenticado através do token"""

    return AutenticacaoControle.decodificar_token(token)


def super_usuario(usuario: dict):
    """Checa se o usuário é super usuário"""


class AutenticacaoControle:
    def criar_token(self, dados: dict) -> str:
        """Cria o JWT baseados nos dados junto com a expiração"""

        copia_dados = dados.copy()
        expiracao = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACAO_MINUTOS)
        copia_dados.update({"exp": expiracao})
        return encode(copia_dados, CHAVE)

    @staticmethod
    def decodificar_token(token: T_Token) -> dict:
        """Decodifica o JWT e checa se ele ainda está válido"""

        exc_invalido = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

        try:
            # Decodificada os dados do token
            payload = decode(token.credentials, CHAVE, algorithms=["HS256"])
            nome = payload.get("sub")
            id_usuario = payload.get("id_usuario")
            super_usuario = payload.get("super")

            # Se não encontrar quer dizer que o token está em formato inválido
            if not nome or not super_usuario or not id_usuario:
                raise exc_invalido

        except DecodeError as err:
            raise exc_invalido from err

        return {"id": id_usuario, "nome": nome, "super": super}

    def registrar_usuario(self, usuario: CriarUsuario, session: Session) -> Usuario:
        # Checa se o usuário já está cadastrado
        mesmo_nome = session.scalar(select(Usuario).where(Usuario.nome == usuario.nome))
        if mesmo_nome:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Usuário já registrado, utilize outro nome",
            )

        # Criar hash da senha
        hash_senha = self._gerar_hash_senha(usuario.senha)

        # Registra usuário no banco de dados
        novo_usuario = Usuario(nome=usuario.nome, senha=hash_senha)
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)

        return novo_usuario

    def _gerar_hash_senha(self, senha_pura: str) -> str:
        return hasher.hash(senha_pura)

    def _validar_senha(self, senha_pura: str, senha_hash: str) -> bool:
        return hasher.verify(senha_pura, senha_hash)

    def autenticar_usuario(self, dados_login: LoginSchema, session: Session) -> Token:
        exc = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Nome e/ou senha inválidos."
        )
        usuario = session.scalar(
            select(Usuario).where((Usuario.nome == dados_login.nome))
        )

        if not usuario or not self._validar_senha(dados_login.senha, usuario.senha):
            raise exc

        dados = {
            "nome_usuario": usuario.nome,
            "id_usuario": usuario.id_usuario,
            "super_usuario": True,
        }

        return Token(token=self.criar_token(dados), tipo="Bearer")
