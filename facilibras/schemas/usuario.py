from datetime import datetime

from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    nome: str
    registro_em: datetime


class CriarUsuario(BaseModel):
    nome_usuario: str
    email: str
    senha: str



class LoginSchema(BaseModel):
    nome: str
    senha: str
