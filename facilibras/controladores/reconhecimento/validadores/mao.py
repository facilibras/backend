from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

PROFUNDIDADE_BAIXO_CIMA = 0.02

x, y, z = range(3)


@registrar_validador(Dedo.POLEGAR_CIMA)
def validar_dedo_polegar_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    # TODO: Implementar os casos não utilizados na apresentação
    diff_polegar_indicador = abs(dedos[3][x] - dedos[5][x])
    diff_indicador_medio = abs(dedos[5][x] - dedos[9][x])
    if diff_polegar_indicador > diff_indicador_medio * 1.5:
        return Invalido()

    if orientacao == Orientacao.FRENTE:
        mao_direita = dedos[3][x] < dedos[9][x]
        if mao_direita:
            if dedos[4][x] > dedos[5][x]:
                return Invalido()
        elif dedos[4][x] < dedos[5][x]:
            return Invalido()

    return Valido()


@registrar_validador(Dedo.POLEGAR_CURVADO)
def validar_dedo_polegar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.POLEGAR_DENTRO)
def validar_dedo_polegar_dentro(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    # TODO: Implementar os casos não utilizados na apresentação
    if orientacao in (Orientacao.FRENTE, Orientacao.BAIXO):
        mao_direita = dedos[2] < dedos[17]
        if mao_direita:
            if dedos[4][x] > dedos[2][x]:
                return Valido()
        elif dedos[4][x] < dedos[2][x]:
            return Valido()

    elif orientacao == Orientacao.TRAS:
        mao_direita = dedos[2] > dedos[17]
        mao_direita = dedos[2] > dedos[17]
        if mao_direita:
            if dedos[4][x] < dedos[2][x]:
                return Valido()
        elif dedos[4][x] > dedos[2][x]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.POLEGAR_FORA)
def validar_dedo_polegar_fora(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    # TODO: Implementar os casos não utilizados na apresentação
    if orientacao in (Orientacao.FRENTE, Orientacao.BAIXO):
        mao_direita = dedos[2] < dedos[17]
        if mao_direita:
            if dedos[4][x] < dedos[2][x]:
                return Valido()
        elif dedos[4][x] > dedos[2][x]:
            return Valido()

    elif orientacao == Orientacao.TRAS:
        mao_direita = dedos[2] > dedos[17]
        if mao_direita:
            if dedos[4][x] > dedos[2][x]:
                return Valido()
        elif dedos[4][x] < dedos[2][x]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.INDICADOR_BAIXO)
def validar_dedo_indicador_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[8][y] > dedos[6][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        if dedos[5][y] < dedos[6][y]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.INDICADOR_CIMA)
def validar_dedo_indicador_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[8][y] < dedos[6][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        diff = abs(dedos[6][z] - dedos[5][z])
        if diff > 0.025:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.INDICADOR_CURVADO)
def validar_dedo_indicador_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.INDICADOR_DIST_MEDIO)
def validar_dedo_indicador_dist_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.INDICADOR_ENC_MEDIO)
def validar_dedo_indicador_enc_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.INDICADOR_ENC_POLEGAR)
def validar_dedo_indicador_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.INDICADOR_FLEXIONADO)
def validar_dedo_indicador_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.INDICADOR_FRENTE_90)
def validar_dedo_indicador_frente_90(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.INDICADOR_MEDIO_CRUZADO)
def validar_dedo_indicador_medio_cruzado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_BAIXO)
def validar_dedo_medio_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[12][y] > dedos[10][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        if dedos[9][y] < dedos[10][y]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.MEDIO_CIMA)
def validar_dedo_medio_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_CURVADO)
def validar_dedo_medio_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_DIST_ANELAR)
def validar_dedo_medio_dist_anelar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_ENC_POLEGAR)
def validar_dedo_medio_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_FLEXIONADO)
def validar_dedo_medio_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.ANELAR_BAIXO)
def validar_dedo_anelar_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[16][y] > dedos[14][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        if dedos[13][y] < dedos[14][y]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.ANELAR_CIMA)
def validar_dedo_anelar_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.ANELAR_CURVADO)
def validar_dedo_anelar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.ANELAR_ENC_POLEGAR)
def validar_dedo_anelar_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.ANELAR_FLEXIONADO)
def validar_dedo_anelar_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MINIMO_BAIXO)
def validar_dedo_minimo_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[20][y] > dedos[18][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        if dedos[17][y] < dedos[18][y]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.MINIMO_CIMA)
def validar_dedo_minimo_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[20][y] < dedos[18][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        diff = abs(dedos[18][z] - dedos[17][z])
        if diff > 0.025:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.MINIMO_CURVADO)
def validar_dedo_minimo_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MINIMO_FLEXIONADO)
def validar_dedo_minimo_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()
