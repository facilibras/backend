from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

x, y, z = range(3)
mensagem = "Nenhum sinal cadastrado no momento deve chegar aqui"
exc = NotImplementedError(mensagem)


@registrar_validador(Dedo.MINIMO_BAIXO)
def validar_dedo_minimo_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (
        Orientacao.FRENTE,
        Orientacao.TRAS,
        Orientacao.LATERAL,
        Orientacao.BAIXO,
    ):
        raise exc

    if orientacao == Orientacao.BAIXO:
        if dedos[19][y] > dedos[18][y]:
            return Valido()
        if dedos[18][y] > dedos[17][y]:
            return Valido()

    # Verifica se está para cima
    if inclinacao == Inclinacao.RETA or orientacao == Orientacao.LATERAL:
        para_cima = dedos[20][y] < dedos[18][y]
        if para_cima:
            return Invalido("Mínimo")

    elif orientacao == Orientacao.TRAS:
        if inclinacao == Inclinacao.DENTRO_45:
            para_baixo = dedos[20][x] > dedos[18][x]
            if para_baixo:
                return Valido()

        para_cima = dedos[20][y] > dedos[18][y]
        if para_cima:
            return Invalido("Mínimo")

    return Valido()


@registrar_validador(Dedo.MINIMO_CIMA)
def validar_dedo_minimo_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.TRAS, Orientacao.BAIXO):
        raise exc

    if orientacao in (Orientacao.FRENTE, Orientacao.BAIXO):
        para_baixo = dedos[20][y] > dedos[18][y]
        if para_baixo:
            return Invalido("Mínimo")

    elif orientacao == Orientacao.TRAS:
        mao_direita = dedos[9][x] < dedos[0][x]
        if mao_direita:
            para_baixo = dedos[20][x] > dedos[18][x]
        else:
            para_baixo = dedos[20][x] < dedos[18][x]

        if para_baixo:
            return Invalido("Mínimo")

    return Valido()


@registrar_validador(Dedo.MINIMO_CURVADO)
def validar_dedo_minimo_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.LATERAL):
        raise exc

    # Verifica se está para cima
    para_cima = dedos[20][y] < dedos[18][y]
    if para_cima:
        return Invalido("Mínimo")

    # Verifica se está flexionado demais
    flexionado_demais = dedos[18][y] > dedos[17][y]
    if flexionado_demais:
        return Invalido("Mínimo")

    return Valido()


@registrar_validador(Dedo.MINIMO_FLEXIONADO)
def validar_dedo_minimo_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE or inclinacao != Inclinacao.RETA:
        raise exc

    # Verifica se está dobrado
    dobrado = dedos[20][y] > dedos[17][y]
    if dobrado:
        return Invalido("Mínimo")

    # Verifica se está para cima
    para_cima = dedos[20][y] < dedos[19][y]
    if para_cima:
        return Invalido("Mínimo")

    return Valido()
