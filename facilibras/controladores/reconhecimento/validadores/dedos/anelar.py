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


@registrar_validador(Dedo.ANELAR_CURVADO)
def validar_dedo_anelar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, _: Mao
) -> Resultado:
    msg = "Anelar deve estar curvado"

    def frente() -> Resultado:
        para_cima = dedos[16][y] < dedos[14][y]
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


@registrar_validador(Dedo.ANELAR_DENTRO_PALMA)
def validar_dedo_anelar_dentro_palma(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Anelar deve estar dentro da palma"

    def baixo() -> Resultado:
        esticado = dedos[14][y] < dedos[13][y]
        if esticado:
            return Invalido(msg)
        return Valido()

    def cima_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[16][x] < dedos[14][x]
        else:
            esticado = dedos[16][x] > dedos[14][x]

        if esticado:
            return Invalido(msg)
        return Valido()

    def frente() -> Resultado:
        para_cima = dedos[16][y] < dedos[14][y]
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
        return frente()

    def tras_dentro_45() -> Resultado:
        return tras_dentro_90()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[16][x] < dedos[14][x]
        else:
            esticado = dedos[16][x] > dedos[14][x]

        if esticado:
            return Invalido(msg)
        return Valido()

    def tras_dentro_180() -> Resultado:
        esticado = dedos[16][y] > dedos[14][y]

        if esticado:
            return Invalido(msg)
        return Valido()

    def tras_dentro_270() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[16][x] > dedos[14][x]
        else:
            esticado = dedos[16][x] < dedos[14][x]

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


@registrar_validador(Dedo.ANELAR_ENC_POLEGAR)
def validar_dedo_anelar_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, _: Mao
) -> Resultado:
    msg = "Anelar deve estar perto do polegar"

    def lateral() -> Resultado:
        # Bastante falso positivos para não falhar sinal O
        para_cima = dedos[16][y] < dedos[14][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)


@registrar_validador(Dedo.ANELAR_ESTICADO)
def validar_dedo_anelar_esticado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Anelar deve estar esticado"

    def frente() -> Resultado:
        para_baixo = dedos[16][y] > dedos[14][y]
        if para_baixo:
            return Invalido(msg)
        return Valido()

    def frente_dentro_45() -> Resultado:
        return frente()

    def lateral() -> Resultado:
        return frente()

    def tras() -> Resultado:
        return frente()

    def tras_dentro_45() -> Resultado:
        return tras_dentro_90()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            dobrado = dedos[16][x] > dedos[14][x]
        else:
            dobrado = dedos[16][x] < dedos[14][x]

        if dobrado:
            return Invalido(msg)
        return Valido()

    def tras_dentro_180() -> Resultado:
        dobrado = dedos[16][y] < dedos[14][y]
        if dobrado:
            return Invalido(msg)
        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.FRENTE, Inclinacao.DENTRO_45):
            return frente_dentro_45()
        case (Orientacao.LATERAL, Inclinacao.RETA):
            return lateral()
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


@registrar_validador(Dedo.ANELAR_FLEXIONADO)
def validar_dedo_anelar_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao, mao: Mao
) -> Resultado:
    msg = "Anelar deve estar flexionado"

    def frente() -> Resultado:
        dobrado = dedos[16][y] > dedos[13][y]
        if dobrado:
            return Invalido(msg)

        para_cima = dedos[16][y] < dedos[15][y]
        if para_cima:
            return Invalido(msg)
        return Valido()

    def tras_dentro_90() -> Resultado:
        if mao == Mao.DIREITA:
            esticado = dedos[16][x] < dedos[14][x]
        else:
            esticado = dedos[16][x] > dedos[14][x]

        if esticado:
            return Invalido(msg)
        return Valido()

    match (orientacao, inclinacao):
        case (Orientacao.FRENTE, Inclinacao.RETA):
            return frente()
        case (Orientacao.TRAS, Inclinacao.DENTRO_90):
            return tras_dentro_90()
        case _:
            raise CombinacaoImpossivelError(orientacao, inclinacao)
