from datetime import datetime

from facilibras.schemas import BaseSchema

class UsuarioSchema(BaseSchema):
    nome_usuario: str
    criado_em: datetime


class CriarUsuario(BaseSchema):
    nome_usuario: str
    email: str
    senha: str



class LoginSchema(BaseSchema):
    nome: str
    senha: str
