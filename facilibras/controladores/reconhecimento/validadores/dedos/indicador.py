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


@registrar_validador(Dedo.INDICADOR_CURVADO)
def validar_dedo_indicador_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar curvadoa"

    def frente() -> Resultado:
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        return frente()

    def lateral() -> Resultado:
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido(msg)

        if mao == Mao.DIREITA:
            para_lado = dedos[7][x] > dedos[5][x]
        else:
            para_lado = dedos[7][x] < dedos[5][x]

        if para_lado:
            return Invalido(msg)

        return Valido()

    def tras_dentro_45() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[8][x] < dedos[6][x]
        else:
            esticado = dedos[8][x] > dedos[6][x]

        if esticado:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.FRENTE, Inclinacao.DENTRO_45):
            return frente_dentro_45()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case (Orientacao.TRAS, Inclinacao.DENTRO_45):
            return tras_dentro_45()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.INDICADOR_DENTRO_PALMA)
def validar_dedo_indicador_dentro_palma(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar dentro da palma"

    def baixo() -> Resultado:
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def cima_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[8][x] < dedos[6][x]
        else:
            esticado = dedos[8][x] > dedos[6][x]
        
        if esticado:
            return Invalido(msg)
        return Valido()

    def frente() -> Resultado:
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        return frente()

    def lateral() -> Resultado: 
        return frente()

    def tras() -> Resultado:
        para_cima = dedos[8][y] < dedos[5][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[8][x] < dedos[7][x]
        else:
            esticado = dedos[8][x] > dedos[7][x]

        if esticado:
            return Invalido(msg)
        return Valido()

    def tras_dentro_270() -> Resultado: 
        if mao == Mao.DIREITA:
            esticado = dedos[8][x] > dedos[7][x]
        else:
            esticado = dedos[8][x] < dedos[7][x]

        if esticado:
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
        case (Orientacao.TRAS, Inclinacao.RETA):
            return tras()
        case (Orientacao.TRAS, Inclinacao.DENTRO_90):
            return tras_dentro_90()
        case (Orientacao.TRAS, Inclinacao.DENTRO_270):
            return tras_dentro_270()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.INDICADOR_DIST_MEDIO)
def validar_dedo_indicador_dist_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar distante do dedo médio"

    def frente() -> Resultado:
        dist_entre_pontas = utils.distancia(dedos[8][x], dedos[12][x])
        dist_entre_origens = utils.distancia(dedos[5][x], dedos[9][x])
        if dist_entre_pontas < dist_entre_origens:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.INDICADOR_ENC_MEDIO)
def validar_dedo_indicador_enc_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar encostado no dedo médio"

    def frente() -> Resultado:
        dist_entre_pontas = utils.distancia(dedos[8][x], dedos[12][x])
        dist_entre_origens = utils.distancia(dedos[5][x], dedos[9][x])
        if dist_entre_pontas > dist_entre_origens:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.INDICADOR_ENC_POLEGAR)
def validar_dedo_indicador_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar encostado no dedo médio"

    def lateral() -> Resultado:
        dist_maxima = utils.distancia3(dedos[8], dedos[7])
        dist_entre_pontas = utils.distancia3(dedos[8], dedos[4])
        if dist_entre_pontas > dist_maxima:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.INDICADOR_ESTICADO)
def validar_dedo_indicador_esticado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar esticado"

    def frente() -> Resultado:
        if dedos[8][y] > dedos[6][y]:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        return frente()

    def lateral() -> Resultado:
        return frente()

    def lateral_fora_90() -> Resultado:
        if mao == Mao.DIREITA:
            dobrado = dedos[6][x] < dedos[5][x] and dedos[8][x] > dedos[6][x]
        else:
            dobrado = dedos[6][x] > dedos[5][x] and dedos[8][x] < dedos[6][x]
        
        if dobrado:
            return Invalido(msg)
        return Valido()

    def tras() -> Resultado:
        return frente()

    def tras_dentro_45() -> Resultado:
        return frente()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            dentro = dedos[8][x] > dedos[6][x]
        else:
            dentro = dedos[8][x] < dedos[6][x]

        if dentro:
            return Invalido(msg)
        return Valido()

    def tras_dentro_180() -> Resultado:
        if dedos[8][y] < dedos[6][y]:
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


@registrar_validador(Dedo.INDICADOR_FLEXIONADO)
def validar_dedo_indicador_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar flexionado"

    def baixo() -> Resultado:
        flexionado = dedos[8][y] > dedos[5][y]
        if not flexionado:
            return Invalido(msg)
        return Valido()

    def frente() -> Resultado:
        dobrado = dedos[8][y] > dedos[5][y]
        if dobrado:
            return Invalido(msg)

        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def lateral() -> Resultado:
        return frente()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[8][x] < dedos[6][x]
        else:
            esticado = dedos[8][x] > dedos[6][x]

        if esticado:
            return Invalido(msg)
        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.BAIXO, Inclinacao.RETA):
            return baixo()
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case (Orientacao.TRAS, Inclinacao.DENTRO_90):
            return tras_dentro_90()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.INDICADOR_FRENTE_90)
def validar_dedo_indicador_frente_90(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador deve estar para a frente"

    def frente() -> Resultado:
        dist_dedo = utils.distancia(dedos[8][y], dedos[5][y])
        dist_mao = utils.distancia(dedos[5][y], dedos[2][y])

        if dist_dedo > dist_mao:
            return Invalido(msg)

        return Valido()

    def lateral() -> Resultado:
        dobrado = dedos[8][y] > dedos[6][y]
        if dobrado:
            return Invalido(msg)

        if mao == Mao.DIREITA:
            reto = dedos[8][x] > dedos[2][x]
        else:
            reto = dedos[8][x] < dedos[2][x]

        if reto:
            return Invalido(msg)
        return Valido()

    def tras_dentro_90() -> Resultado:
        dist_5_2 = utils.distancia(dedos[5][x], dedos[2][x])
        dist_8_5 = utils.distancia(dedos[8][x], dedos[5][x])
        esticado = dist_5_2 < dist_8_5
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


@registrar_validador(Dedo.INDICADOR_MEDIO_CRUZADO)
def validar_dedo_indicador_medio_cruzado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Indicador e médio devem estar cruzados"

    def frente() -> Resultado:
        if mao == Mao.DIREITA:
            distantes = dedos[8][x] < dedos[12][x]
        else:
            distantes = dedos[8][x] > dedos[12][x]

        if distantes:
            return Invalido(msg)

        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)
