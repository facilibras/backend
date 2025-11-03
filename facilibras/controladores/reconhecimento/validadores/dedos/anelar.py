from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Dedo, Inclinacao, Mao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

x, y, z = range(3)
mensagem = "Nenhum sinal cadastrado no momento deve chegar aqui"
exc = NotImplementedError(mensagem)


@registrar_validador(Dedo.ANELAR_BAIXO)
def validar_dedo_anelar_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao not in (
        Orientacao.FRENTE,
        Orientacao.TRAS,
        Orientacao.LATERAL,
        Orientacao.BAIXO,
    ):
        raise exc

    # Verifica se está para cima
    if inclinacao == Inclinacao.RETA or orientacao == Orientacao.LATERAL:
        para_cima = dedos[16][y] < dedos[13][y]
        if para_cima:
            return Invalido("Anelar")

    elif orientacao == Orientacao.TRAS:
        if inclinacao == Inclinacao.DENTRO_90:
            mao_direita = dedos[9][x] < dedos[0][x]
            if mao_direita:
                para_cima = dedos[16][x] < dedos[14][x]
            else:
                para_cima = dedos[16][x] > dedos[14][x]

            if para_cima:
                return Invalido("Anelar")

        elif inclinacao == Inclinacao.DENTRO_180:
            para_cima = dedos[16][y] > dedos[14][y]

            if para_cima:
                return Invalido("Anelar")

    return Valido()


@registrar_validador(Dedo.ANELAR_CIMA)
def validar_dedo_anelar_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.TRAS):
        raise exc

    if orientacao == Orientacao.FRENTE:
        para_baixo = dedos[16][y] > dedos[14][y]

    elif orientacao == Orientacao.TRAS:
        para_baixo = dedos[16][y] < dedos[14][y]

    if para_baixo:
        return Invalido("Anelar")

    return Valido()


@registrar_validador(Dedo.ANELAR_CURVADO)
def validar_dedo_anelar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.LATERAL):
        raise exc

    # Verifica se está para cima
    para_cima = dedos[16][y] < dedos[14][y]
    if para_cima:
        return Invalido("Anelar")

    # Verifica se está flexionado demais
    # TODO: Se for bem, substituir nos outros dedos_curvados
    flexionado_demais = dedos[14][y] > dedos[13][y]
    if flexionado_demais:
        return Invalido("Anelar")

    return Valido()


@registrar_validador(Dedo.ANELAR_ENC_POLEGAR)
def validar_dedo_anelar_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.LATERAL or inclinacao != Inclinacao.RETA:
        raise exc

    # Verifica polegar para baixo
    para_baixo = dedos[4][y] > dedos[3][y]
    if para_baixo:
        return Invalido("Anelar")

    # Verifica anelar para cima
    para_cima = dedos[16][y] < dedos[15][y]
    if para_cima:
        return Invalido("Anelar")

    return Valido()


@registrar_validador(Dedo.ANELAR_FLEXIONADO)
def validar_dedo_anelar_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    if orientacao != Orientacao.FRENTE or inclinacao != Inclinacao.RETA:
        raise exc

    # Verifica se está dobrado
    dobrado = dedos[16][y] > dedos[13][y]
    if dobrado:
        return Invalido("Anelar")

    # Verifica se está para cima
    para_cima = dedos[16][y] < dedos[15][y]
    if para_cima:
        return Invalido("Anelar")

    return Valido()
