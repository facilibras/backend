import facilibras.controladores.reconhecimento.validadores.utils as utils
from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Expressao

T_Ponto = tuple[float, float, float]
T_Rosto = dict[int, T_Ponto]

x, y, z = range(3)

def boca_aberta(pontos: T_Rosto) -> bool:
    dist_labios = utils.distancia2(pontos[13][y] ,pontos[14][y])
    maior_labio = max(
        utils.distancia2(pontos[13][y] - pontos[0][y]),
        utils.distancia2(pontos[14][y] - pontos[17][y])
    )
    return dist_labios > maior_labio

@registrar_validador(Expressao.BOCA_ABERTA)
def validar_expressao_boca_aberta(
    rosto: T_Rosto
) -> Resultado:
    if boca_aberta(rosto):
        return Valido()
    return Invalido("A boca deve estar aberta")


@registrar_validador(Expressao.BOCA_FECHADA)
def validar_expressao_boca_fechada(
    rosto: T_Rosto
) -> Resultado:
    if boca_aberta(rosto):
        return Invalido("A boca deve estar fechada")
    return Valido()

@registrar_validador(Expressao.QUALQUER)
def validar_expressao_qualquer(
    rosto: T_Rosto
) -> Resultado:
    return Valido()
