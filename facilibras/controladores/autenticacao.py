from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import HTTPException
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash

from facilibras.config.env import get_variavel_ambiente
from facilibras.dependencias.autenticacao import T_Token
from facilibras.dependencias.dal import T_UsuarioDAO
from facilibras.modelos import Usuario
from facilibras.schemas import CriarUsuario, LoginSchema, Token

CHAVE = get_variavel_ambiente("CHAVE", str)
EXPIRACAO_MINUTOS = get_variavel_ambiente("EXPIRACAO_TOKEN", int)
hasher = PasswordHash.recommended()


def usuario_autenticado(token: T_Token):
    """Retorna o usuário autenticado através do token"""

    return AutenticacaoControle.decodificar_token(token)


def super_usuario(usuario: dict):
    """Checa se o usuário é super usuário"""


class AutenticacaoControle:
    def __init__(self, dao: T_UsuarioDAO) -> None:
        self.dao = dao

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

    def registrar_usuario(self, dados_usuario: CriarUsuario) -> Usuario:
        # Checa se o usuário já está cadastrado
        usuario = self.dao.buscar_por_email(dados_usuario.email)
        if usuario:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Usuário já registrado, utilize outro email",
            )

        # Criar hash da senha
        hash_senha = self.gerar_hash_senha(dados_usuario.senha)

        # Registra usuário no banco de dados
        novo_usuario = Usuario(
            nome=dados_usuario.nome, email=dados_usuario.email, hash_senha=hash_senha
        )
        return self.dao.criar(novo_usuario)

    def autenticar_usuario(self, dados_login: LoginSchema) -> Token:
        usuario = self.dao.buscar_por_email(dados_login.nome)

        if not usuario or not self.validar_senha(dados_login.senha, usuario.hash_senha):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Email e/ou senha inválido[s].",
            )

        dados = {
            "nome_usuario": usuario.nome,
            "id_usuario": usuario.id_usuario,
            "super_usuario": True,
        }

        return Token(token=self.criar_token(dados), tipo="Bearer")

    def gerar_hash_senha(self, senha_pura: str) -> str:
        return hasher.hash(senha_pura)

    def validar_senha(self, senha_pura: str, senha_hash: str) -> bool:
        return hasher.verify(senha_pura, senha_hash)
