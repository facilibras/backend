from facilibras.schemas import BaseSchema


class MensagemSchema(BaseSchema):
    """Mensagem retornada p/ informar sucesso ou falha em várias rotas"""

    mensagem: str
