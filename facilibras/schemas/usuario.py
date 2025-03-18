from datetime import datetime

from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    nome: str
    data_registro: datetime


class CriarUsuario(BaseModel):
    nome: str
    senha: str
