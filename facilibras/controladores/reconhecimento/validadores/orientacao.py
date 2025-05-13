from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Mao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

LIMIAR_PROFUNDIDADE = 0.075
LIMIAR_ALTURA = 0.20
LIMIAR_LARGURA = 0.20

x, y, z = range(3)


@registrar_validador(Orientacao.BAIXO)
def validar_orientacao_baixo(dedos: T_Dedos, mao: Mao) -> Resultado:
    # TODO: Considerar inclinação

    # Frente / Tras
    diff_pulso = abs(dedos[9][z] - dedos[0][z])
    if diff_pulso < 0.05:
        return Invalido("Orientação inválida")

    # Lateral
    diff_altura = abs(dedos[5][z] - dedos[17][z])
    if diff_altura >= LIMIAR_PROFUNDIDADE:
        return Invalido("Orientação inválida")

    if mao == Mao.DIREITA:
        if dedos[5][x] < dedos[17][x]:
            return Valido()
    else:
        if dedos[5][x] > dedos[17][x]:
            return Valido()

    return Invalido("Orientação inválida")


@registrar_validador(Orientacao.FRENTE)
def validar_orientacao_frente(dedos: T_Dedos, mao: Mao) -> Resultado:
    # Checagem orientação incorreta (cima/baixo)

    if abs(dedos[9][z] - dedos[0][z]) >= 0.05:
        return Invalido("Orientação inválida")

    diff_altura = abs(dedos[5][y] - dedos[17][y])
    if diff_altura > LIMIAR_ALTURA:
        return Invalido("Orientação inválida")

    # Checagem orientação incorreta (lateral)
    diff_profundidade = abs(dedos[5][z] - dedos[17][z])
    if diff_profundidade > 0.04:
        return Invalido("Orientação inválida")

    # Checagem orientação correta
    if mao == Mao.DIREITA:
        if dedos[2][x] < dedos[17][x]:
            return Valido()
    elif dedos[2][x] > dedos[17][x]:
        return Valido()
    return Invalido("Orientação inválida")


@registrar_validador(Orientacao.LATERAL)
def validar_orientacao_lateral(dedos: T_Dedos, mao: Mao) -> Resultado:
    diff = abs(dedos[5][z] - dedos[17][z])
    if diff < LIMIAR_PROFUNDIDADE:
        return Invalido("Orientação inválida")

    # TODO: considerar orientação
    diff_altura = abs(dedos[0][y] - dedos[9][y])
    if diff_altura < LIMIAR_ALTURA:
        return Invalido("Orientação inválida")

    return Valido()


@registrar_validador(Orientacao.TRAS)
def validar_orientacao_tras(dedos: T_Dedos, mao: Mao) -> Resultado:
    # Checagem orientação incorreta (cima/baixo)
    diff_altura = abs(dedos[5][y] - dedos[17][y])
    if diff_altura > LIMIAR_ALTURA:
        return Invalido("Orientação inválida")

    # Checagem orientação incorreta (lateral)
    diff_profundidade = abs(dedos[5][z] - dedos[17][z])
    if diff_profundidade > LIMIAR_PROFUNDIDADE:
        return Invalido("Orientação inválida")

    # Checagem orientação correta
    if mao == Mao.DIREITA:
        if dedos[2][x] > dedos[17][x]:
            return Valido()
    elif dedos[2][x] < dedos[17][x]:
        return Valido()
    return Invalido("Orientação inválida")
