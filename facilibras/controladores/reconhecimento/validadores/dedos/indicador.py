from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.controladores.reconhecimento.validadores.utils import (
    distancia,
    distancia3,
)
from facilibras.modelos.mao import Dedo, Inclinacao, Mao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

x, y, z = range(3)
mensagem = "Nenhum sinal cadastrado no momento deve chegar aqui"
exc = NotImplementedError(mensagem)


@registrar_validador(Dedo.INDICADOR_BAIXO)
def validar_dedo_indicador_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.BAIXO, Orientacao.TRAS):
        raise exc

    # Verifica se está para cima
    if orientacao in (Orientacao.FRENTE, Orientacao.BAIXO):
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido("Indicador")

    elif orientacao == Orientacao.TRAS:
        if inclinacao != Inclinacao.DENTRO_90:
            raise exc

        mao_direita = dedos[9][x] < dedos[0][x]
        if mao_direita:
            para_cima = dedos[8][x] < dedos[7][x]
        else:
            para_cima = dedos[8][x] > dedos[7][x]

        if para_cima:
            return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_CIMA)
def validar_dedo_indicador_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.TRAS, Orientacao.LATERAL):
        raise exc

    # Verifica se está para baixo
    if orientacao in (Orientacao.FRENTE, Orientacao.LATERAL):
        if dedos[8][y] > dedos[6][y]:
            return Invalido("Indicador")

    elif orientacao == Orientacao.TRAS:
        if inclinacao == Inclinacao.DENTRO_180:
            para_baixo = dedos[8][y] < dedos[6][y]
        elif inclinacao in (Inclinacao.RETA, Inclinacao.DENTRO_45):
            para_baixo = dedos[8][y] > dedos[6][y]

        if para_baixo:
            return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_CURVADO)
def validar_dedo_indicador_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.LATERAL):
        raise exc

    # Verifica se está para cima
    para_cima = dedos[8][y] < dedos[6][y]
    if para_cima:
        return Invalido("Indicador")

    # Verifica se está curvado demais (somente lateral)
    if orientacao == Orientacao.LATERAL:
        if inclinacao != Inclinacao.RETA:
            raise exc

        mao_direita = dedos[5][x] < dedos[0][x]
        if mao_direita:
            para_baixo = dedos[7][x] > dedos[5][x]
        else:
            para_baixo = dedos[7][x] < dedos[5][x]

        if para_baixo:
            return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_DIST_MEDIO)
def validar_dedo_indicador_dist_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.FRENTE or inclinacao != Inclinacao.RETA:
        raise exc

    # Checa se os dedos estão próximos
    dist_entre_pontas = distancia(dedos[8][x], dedos[12][x])
    dist_entre_origens = distancia(dedos[5][x], dedos[9][x])
    if dist_entre_pontas < dist_entre_origens:
        return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_ENC_MEDIO)
def validar_dedo_indicador_enc_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.FRENTE or inclinacao != Inclinacao.RETA:
        raise exc

    # Checa se os dedos estão distantes
    dist_entre_pontas = distancia(dedos[8][x], dedos[12][x])
    dist_entre_origens = distancia(dedos[5][x], dedos[9][x])
    if dist_entre_pontas > dist_entre_origens:
        return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_ENC_POLEGAR)
def validar_dedo_indicador_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.LATERAL or inclinacao != Inclinacao.RETA:
        raise exc

    # Checa se os dedos estão distantes
    dist_maxima = distancia3(dedos[8], dedos[7])
    dist_entre_pontas = distancia3(dedos[8], dedos[4])
    if dist_entre_pontas > dist_maxima:
        return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_FLEXIONADO)
def validar_dedo_indicador_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.BAIXO):
        raise exc

    if orientacao == Orientacao.FRENTE:
        # Verifica se está dobrado
        dobrado = dedos[8][y] > dedos[5][y]
        if dobrado:
            return Invalido("Indicador")

        # Verifica se está para cima
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido("Indicador")

    elif orientacao == Orientacao.BAIXO:
        flexionado = dedos[8][y] > dedos[5][y]
        if not flexionado:
            return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_FRENTE_45)
def validar_dedo_indicador_frente_45(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.LATERAL:
        raise exc

    # Verifica se está para baixo
    para_baixo = dedos[8][y] < dedos[5][y]
    if para_baixo:
        return Invalido("Indicador")

    # Verifica angulo insuficiente
    dist_ponta = distancia(dedos[8][x], dedos[7][x])
    dist_origem = distancia(dedos[7][x], dedos[5][x])

    if dist_origem < dist_ponta:
        return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_FRENTE_90)
def validar_dedo_indicador_frente_90(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.FRENTE:
        raise exc

    # TODO: Utilizar profundidade
    # Compara distância entre dedo e articulação polegar
    dist_dedo = distancia(dedos[8][y], dedos[5][y])
    dist_mao = distancia(dedos[5][y], dedos[2][y])

    if dist_dedo > dist_mao:
        return Invalido("Indicador")

    return Valido()


@registrar_validador(Dedo.INDICADOR_MEDIO_CRUZADO)
def validar_dedo_indicador_medio_cruzado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.FRENTE:
        raise exc

    mao_direita = dedos[2] < dedos[17]
    if mao_direita:
        distantes = dedos[8][x] < dedos[12][x]
    else:
        distantes = dedos[8][x] > dedos[12][x]

    if distantes:
        return Invalido("Indicador")

    return Valido()
