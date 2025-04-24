from facilibras.controladores.reconhecimento.validadores import (
    Resultado,
    registrar_validador,
)
from facilibras.modelos.mao import Inclinacao, Mao

T_Dedos = dict[int, tuple[float, float, float]]


@registrar_validador(Inclinacao.DENTRO_45)
def validar_inclinacao_dentro_45(dedos: T_Dedos, mao: Mao) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Inclinacao.DENTRO_90)
def validar_inclinacao_dentro_90(dedos: T_Dedos, mao: Mao) -> Resultado:
    raise NotImplementedError()
