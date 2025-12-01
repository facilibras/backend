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
mensagem = "Nenhum sinal cadastrado no momento deve chegar aqui"
exc = NotImplementedError(mensagem)


@registrar_validador(Dedo.POLEGAR_CURVADO)
def validar_dedo_polegar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Polegar deve estar curvado"

    def frente() -> Resultado:
        if mao == Mao.DIREITA:
            curvatura_minima = dedos[4][x] > dedos[3][x]
        else:
            curvatura_minima = dedos[4][x] < dedos[3][x]

        if curvatura_minima:
            return Valido()
        return Invalido(msg)

    def frente_dentro_45() -> Resultado:
        curvatura_minima = dedos[4][y] < dedos[2][y]

        if curvatura_minima:
            return Valido()
        return Invalido(msg)

    def lateral() -> Resultado:
        curvatura_minima = dedos[4][y] < dedos[3][y]
        if curvatura_minima:
            return Valido()
        return Invalido(msg)

    def tras_dentro_45() -> Resultado:
        if mao == Mao.DIREITA:
            curvatura_minima = dedos[4][x] > dedos[5][x]
        else:
            curvatura_minima = dedos[4][x] < dedos[5][x]

        if curvatura_minima:
            return Valido()
        return Invalido(msg)

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


@registrar_validador(Dedo.POLEGAR_DENTRO_PALMA)
def validar_dedo_polegar_dentro_palma(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Polegar deve estar dentro da palma"

    def baixo() -> Resultado:
        if mao == Mao.DIREITA:
            dentro = dedos[4][x] > dedos[2][x]
        else:
            dentro = dedos[4][x] < dedos[2][x]

        if dentro:
            return Valido()
        return Invalido(msg)

    def frente() -> Resultado:
        return baixo()

    def frente_dentro_45() -> Resultado:
        if mao == Mao.DIREITA:
            curvatura_minima = dedos[4][x] > dedos[2][x]
        else:
            curvatura_minima = dedos[4][x] < dedos[2][x]

        if curvatura_minima:
            return Valido()
        return Invalido(msg)

    def lateral() -> Resultado:
        dentro_palma = dedos[4][y] >= dedos[5][y]
        if dentro_palma:
            return Valido()
        return Invalido(msg)

    def lateral_fora_90() -> Resultado:
        dentro_palma = dedos[4][y] >= dedos[3][y]
        if dentro_palma:
            return Valido()
        return Invalido(msg)

    def tras() -> Resultado:
        if mao == Mao.DIREITA:
            dentro = dedos[4][x] < dedos[3][x]
        else:
            dentro = dedos[4][x] > dedos[3][x]

        if dentro:
            return Valido()
        return Invalido(msg)

    def tras_dentro_45() -> Resultado:
        return lateral()

    def tras_dentro_90() -> Resultado:
        dentro_palma = dedos[4][y] >= dedos[2][y]
        if dentro_palma:
            return Valido()
        return Invalido(msg)

    def tras_dentro_180() -> Resultado:
        if mao == Mao.DIREITA:
            dentro = dedos[4][x] > dedos[5][x]
        else:
            dentro = dedos[4][x] < dedos[5][x]

        if dentro:
            return Valido()
        return Invalido(msg)

    match (orientacao, inclinacao):
        case (Orientacao.BAIXO, Inclinacao.RETA):
            return baixo()
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


@registrar_validador(Dedo.POLEGAR_ENC_LATERAL)
def validar_dedo_polegar_enc_lateral(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Polegar deve encostar na lateral da mão"

    def frente() -> Resultado:
        dist_polegar_indicador = utils.distancia(dedos[3][x], dedos[5][x])
        dist_indicador_medio = utils.distancia(dedos[5][x], dedos[9][x])
        if dist_polegar_indicador > dist_indicador_medio * 1.5:
            return Invalido(msg)

        if mao == Mao.DIREITA:
            dentro_palma = dedos[4][x] > dedos[2][x]
        else:
            dentro_palma = dedos[4][x] < dedos[2][x]

        if dentro_palma:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        dist_polegar_indicador = utils.distancia2(dedos[3], dedos[5])
        dist_indicador_medio = utils.distancia2(dedos[5], dedos[9])
        if dist_polegar_indicador > dist_indicador_medio * 1.5:
            return Invalido(msg)

        if mao == Mao.DIREITA:
            dentro_palma = dedos[4][x] > dedos[5][x]
        else:
            dentro_palma = dedos[4][x] < dedos[2][x]

        if dentro_palma:
            return Invalido(msg)
        return Valido()

    def lateral() -> Resultado:
        dist_max = utils.distancia(dedos[17][y], dedos[0][y]) * 0.7
        dist_polegar_indicador = utils.distancia(dedos[4][x], dedos[0][x])
        dentro_margem = dist_polegar_indicador < dist_max
        if dentro_margem:
            return Valido()
        return Invalido(msg)

    def tras_dentro_45() -> Resultado:
        if mao == Mao.DIREITA:
            aberto = dedos[4][x] > dedos[2][x]
        else:
            aberto = dedos[4][x] < dedos[2][x]

        if aberto:
            return Invalido(msg)
        return Valido()

    def tras_dentro_180() -> Resultado:
        return frente()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.FRENTE, Inclinacao.DENTRO_45):
            return frente_dentro_45()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case (Orientacao.TRAS, Inclinacao.DENTRO_45):
            return tras_dentro_45()
        case (Orientacao.TRAS, Inclinacao.DENTRO_180):
            return tras_dentro_180()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.POLEGAR_ESTICADO)
def validar_dedo_polegar_esticado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Polegar deve estar esticado"

    def baixo() -> Resultado:
        if mao == Mao.DIREITA:
            aberto = dedos[4][x] < dedos[3][x]
        else:
            aberto = dedos[4][x] > dedos[3][x]

        if aberto:
            return Valido()
        return Invalido(msg)

    def cima_dentro_90() -> Resultado:
        esticado = dedos[4][y] < dedos[3][y]
        if esticado:
            return Valido()
        return Invalido(msg)

    def frente() -> Resultado:
        return baixo()

    def frente_dentro_45() -> Resultado:
        return frente()

    def tras() -> Resultado:
        if mao == Mao.DIREITA:
            dentro_palma = dedos[4][x] < dedos[5][x]
        else:
            dentro_palma = dedos[4][x] > dedos[5][x]

        if dentro_palma:
            return Invalido(msg)

        dist_min = utils.distancia(dedos[5][x], dedos[9][x]) * 1.8
        dist_pol_ind = utils.distancia(dedos[3][x], dedos[5][x])
        if dist_pol_ind <= dist_min:
            return Invalido(msg)
        return Valido()

    def tras_dentro_90() -> Resultado:
        dentro_palma = dedos[4][y] > dedos[3][y]
        if dentro_palma:
            return Invalido(msg)
        return Valido()

    def tras_dentro_270() -> Resultado:
        dentro_palma = dedos[4][y] < dedos[2][y]
        if dentro_palma:
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
        case (Orientacao.TRAS, Inclinacao.RETA):
            return tras()
        case (Orientacao.TRAS, Inclinacao.DENTRO_90):
            return tras_dentro_90()
        case (Orientacao.TRAS, Inclinacao.DENTRO_270):
            return tras_dentro_270()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)
