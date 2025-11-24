import facilibras.controladores.reconhecimento.validadores.utils as utils
from facilibras.controladores.reconhecimento.validadores import (
    CombinacaoImpossivelError,
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Dedo, Inclinacao, Mao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

x, y, z = range(3)


@registrar_validador(Dedo.MEDIO_CURVADO)
def validar_dedo_medio_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, _: Mao
) -> Resultado:
    msg = "Médio deve estar curvado"

    def frente() -> Resultado:
        para_cima = dedos[12][y] < dedos[10][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        return frente()

    def lateral() -> Resultado:
        return frente()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.FRENTE, Inclinacao.DENTRO_45):
            return frente_dentro_45()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.MEDIO_DENTRO_PALMA)
def validar_dedo_medio_dentro_palma(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Médio deve estar dentro da palma"

    def baixo() -> Resultado:
        para_cima = dedos[12][y] < dedos[9][y]
        if para_cima:
            return Invalido(msg)

        dobrado = dedos[12][y] > dedos[11][y]
        if dobrado:
            return Invalido(msg)
        return Valido()

    def cima_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[12][x] < dedos[10][x]
        else:
            esticado = dedos[12][x] > dedos[10][x]

        if esticado:
            return Invalido(msg)
        return Valido()

    def frente() -> Resultado:
        para_cima = dedos[12][y] < dedos[10][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        return frente()

    def lateral() -> Resultado:
        return frente()

    def lateral_fora_90() -> Resultado:
        return cima_dentro_90()

    def tras() -> Resultado:
        para_cima = dedos[12][y] < dedos[10][y]

        if para_cima:
            return Invalido(msg)
        return Valido()

    def tras_dentro_45() -> Resultado:
        return tras()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            para_cima = dedos[12][x] < dedos[10][x]
        else:
            para_cima = dedos[12][x] > dedos[10][x]

        if para_cima:
            return Invalido(msg)
        return Valido()

    def tras_dentro_180() -> Resultado:
        esticado = dedos[12][y] > dedos[10][y]

        if esticado:
            return Invalido(msg)
        return Valido()

    def tras_dentro_270() -> Resultado:
        if mao == Mao.DIREITA:
            para_cima = dedos[12][x] > dedos[10][x]
        else:
            para_cima = dedos[12][x] < dedos[10][x]

        if para_cima:
            return Invalido(msg)
        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.BAIXO, Inclinacao.RETA):
            return baixo()
        case (Orientacao.CIMA, Inclinacao.DENTRO_90):
            return cima_dentro_90()
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.FRENTE, Inclinacao.DENTRO_45):
            return frente_dentro_45()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case (Orientacao.LATERAL, Inclinacao.FORA_90):
            return lateral_fora_90()
        case (Orientacao.TRAS, Inclinacao.RETA):
            return tras()
        case (Orientacao.TRAS, Inclinacao.DENTRO_45):
            return tras_dentro_45()
        case (Orientacao.TRAS, Inclinacao.DENTRO_90):
            return tras_dentro_90()
        case (Orientacao.TRAS, Inclinacao.DENTRO_180):
            return tras_dentro_180()
        case (Orientacao.TRAS, Inclinacao.DENTRO_270):
            return tras_dentro_270()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.MEDIO_DIST_ANELAR)
def validar_dedo_medio_dist_anelar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, _: Mao
) -> Resultado:
    msg = "Médio deve estar distante do anelar"

    def frente() -> Resultado:
        dist_entre_pontas = utils.distancia(dedos[12][x], dedos[16][x])
        dist_entre_origens = utils.distancia(dedos[9][x], dedos[13][x])
        if dist_entre_pontas < dist_entre_origens:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.MEDIO_ENC_POLEGAR)
def validar_dedo_medio_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, _: Mao
) -> Resultado:
    msg = "Médio deve estar encostando o polegar"

    def lateral() -> Resultado:
        para_baixo = dedos[4][y] > dedos[3][y]
        if para_baixo:
            return Invalido(msg)

        para_cima = dedos[12][y] < dedos[11][y]
        if para_cima:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.MEDIO_ESTICADO)
def validar_dedo_medio_esticado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Médio deve estar esticado"

    def frente() -> Resultado:
        para_baixo = dedos[12][y] > dedos[10][y]
        if para_baixo:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        return frente()

    def lateral() -> Resultado:
        return frente()

    def lateral_fora_90() -> Resultado:
        fora_90 = dedos[5][y] < dedos[9][y] and dedos[9][y] < dedos[13][y]
        if not fora_90:
            return Invalido(msg)
        return Valido()

    def tras() -> Resultado:
        return frente()

    def tras_dentro_45() -> Resultado:
        if mao == Mao.DIREITA:
            para_baixo = dedos[12][x] > dedos[10][x]
        else:
            para_baixo = dedos[12][x] < dedos[10][x]

        if para_baixo:
            return Invalido(msg)
        return Valido()

    def tras_dentro_90() -> Resultado:
        return tras_dentro_45()

    def tras_dentro_180() -> Resultado:
        para_baixo = dedos[12][y] < dedos[10][y]
        if para_baixo:
            return Invalido(msg)
        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.FRENTE, Inclinacao.DENTRO_45):
            return frente_dentro_45()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case (Orientacao.LATERAL, Inclinacao.FORA_90):
            return lateral_fora_90()
        case (Orientacao.TRAS, Inclinacao.RETA):
            return tras()
        case (Orientacao.TRAS, Inclinacao.DENTRO_45):
            return tras_dentro_45()
        case (Orientacao.TRAS, Inclinacao.DENTRO_90):
            return tras_dentro_90()
        case (Orientacao.TRAS, Inclinacao.DENTRO_180):
            return tras_dentro_180()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.MEDIO_FLEXIONADO)
def validar_dedo_medio_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Médio deve estar flexionado"

    def frente() -> Resultado:
        dobrado = dedos[12][y] > dedos[9][y]
        if dobrado:
            return Invalido(msg)

        para_cima = dedos[12][y] < dedos[10][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def lateral() -> Resultado:
        flex = dedos[12][y] > dedos[11][y]
        if not flex:
            return Invalido(msg)
        return Valido()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[12][x] < dedos[10][x]
        else:
            esticado = dedos[12][x] > dedos[10][x]

        if esticado:
            return Invalido(msg)
        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case (Orientacao.TRAS, Inclinacao.DENTRO_90):
            return tras_dentro_90()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.MEDIO_FRENTE_45)
def validar_dedo_medio_frente_45(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, _: Mao
) -> Resultado:
    msg = "Médio deve estar levemente para frente"

    def frente() -> Resultado:
        # Aceita para cima para não dar falso negativo
        para_baixo = dedos[12][y] > dedos[9][y]
        if para_baixo:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)
