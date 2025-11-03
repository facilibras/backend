from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.controladores.reconhecimento.validadores.utils import (
    distancia,
)
from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

x, y, z = range(3)
mensagem = "Nenhum sinal cadastrado no momento deve chegar aqui"
exc = NotImplementedError(mensagem)


@registrar_validador(Dedo.MEDIO_BAIXO)
def validar_dedo_medio_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (
        Orientacao.FRENTE,
        Orientacao.TRAS,
        Orientacao.LATERAL,
        Orientacao.BAIXO,
    ):
        raise exc

    # Verificar se está para cima
    if orientacao in (Orientacao.FRENTE, Orientacao.BAIXO):
        para_cima = dedos[12][y] < dedos[9][y]
        if para_cima:
            return Invalido("Médio")

    elif orientacao == Orientacao.TRAS:
        if inclinacao == Inclinacao.DENTRO_90:
            mao_direita = dedos[9][x] < dedos[0][x]
            if mao_direita:
                para_cima = dedos[12][x] < dedos[10][x]
            else:
                para_cima = dedos[12][x] > dedos[10][x]

            if para_cima:
                return Invalido("Médio")

        elif inclinacao == Inclinacao.DENTRO_180:
            para_cima = dedos[12][y] > dedos[11][y]
            if para_cima:
                return Invalido("Médio")
        else:
            raise exc

    return Valido()


@registrar_validador(Dedo.MEDIO_CIMA)
def validar_dedo_medio_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.TRAS, Orientacao.LATERAL):
        raise exc

    # Verifica se está para baixo
    if inclinacao == Inclinacao.RETA:
        para_baixo = dedos[12][y] > dedos[11][y]
        if para_baixo:
            return Invalido("Médio")

    if orientacao == Orientacao.LATERAL:
        if inclinacao == Inclinacao.DENTRO_45:
            # Verifica se o dedo está inclinado
            nao_inclinado = dedos[12][y] > dedos[10][y]

            if nao_inclinado:
                return Invalido("Médio")

    elif orientacao == Orientacao.TRAS and inclinacao == Inclinacao.DENTRO_180:
        para_baixo = dedos[12][y] < dedos[10][y]
        if para_baixo:
            return Invalido("Médio")

    return Valido()


@registrar_validador(Dedo.MEDIO_CURVADO)
def validar_dedo_medio_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.LATERAL):
        raise exc

    # Verifica se está para cima
    para_cima = dedos[12][y] < dedos[10][y]
    if para_cima:
        return Invalido("Médio")

    # Verifica se está curvado demais (somente lateral)
    if orientacao == Orientacao.LATERAL:
        if inclinacao != Inclinacao.RETA:
            raise exc

        mao_direita = dedos[5][x] < dedos[0][x]
        if mao_direita:
            para_baixo = dedos[11][x] > dedos[9][x]
        else:
            para_baixo = dedos[11][x] < dedos[9][x]

        if para_baixo:
            return Invalido("Médio")

    return Valido()


@registrar_validador(Dedo.MEDIO_DIST_ANELAR)
def validar_dedo_medio_dist_anelar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE:
        raise exc

    # Checa se os dedos estão próximos
    dist_entre_pontas = distancia(dedos[12][x], dedos[16][x])
    dist_entre_origens = distancia(dedos[9][x], dedos[13][x])
    if dist_entre_pontas < dist_entre_origens:
        return Invalido("Médio")

    return Valido()


@registrar_validador(Dedo.MEDIO_ENC_POLEGAR)
def validar_dedo_medio_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.LATERAL or inclinacao != Inclinacao.RETA:
        raise exc

    # Verifica se polegar está para baixo
    para_baixo = dedos[4][y] > dedos[3][y]
    if para_baixo:
        return Invalido("Médio")

    # Verifica se polegar está para baixo
    para_cima = dedos[12][y] < dedos[11][y]
    if para_cima:
        return Invalido("Médio")

    return Valido()


@registrar_validador(Dedo.MEDIO_FLEXIONADO)
def validar_dedo_medio_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE:
        raise exc

    # Verifica se está dobrado
    dobrado = dedos[12][y] > dedos[9][y]
    if dobrado:
        return Invalido("Médio")

    # Verifica se está para cima
    para_cima = dedos[12][y] < dedos[10][y]
    if para_cima:
        return Invalido("Médio")

    return Valido()


@registrar_validador(Dedo.MEDIO_FRENTE_45)
def validar_dedo_medio_frente_45(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE:
        raise exc

    # Verifica se está para baixo
    para_baixo = dedos[12][y] > dedos[9][y]
    if para_baixo:
        return Invalido("Médio")

    return Valido()
