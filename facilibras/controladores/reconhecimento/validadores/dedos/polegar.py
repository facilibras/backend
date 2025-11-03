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


@registrar_validador(Dedo.POLEGAR_CIMA)
def validar_dedo_polegar_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if not (
        (orientacao == Orientacao.FRENTE and inclinacao == Inclinacao.RETA)
        or (orientacao == Orientacao.TRAS and inclinacao == Inclinacao.DENTRO_180)
    ):
        raise exc

    # Verifica se o polegar está aberto
    dist_polegar_indicador = distancia(dedos[3][x], dedos[5][x])
    dist_indicador_medio = distancia(dedos[5][x], dedos[9][x])
    if dist_polegar_indicador > dist_indicador_medio * 1.5:
        return Invalido("Polegar")

    # Verifica se o polegar está para dentro da palma
    mao_direita = dedos[3][x] < dedos[17][x]
    if mao_direita:
        dentro_palma = dedos[4][x] > dedos[2][x]
    else:
        dentro_palma = dedos[4][x] < dedos[2][x]

    if dentro_palma:
        return Invalido("Polegar")

    return Valido()


@registrar_validador(Dedo.POLEGAR_CURVADO)
def validar_dedo_polegar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.LATERAL):
        raise exc

    if orientacao == Orientacao.LATERAL:
        mao_direita = dedos[5][x] < dedos[0][x]
    else:
        mao_direita = dedos[2][x] < dedos[17][x]

    # Verifica curvatura suficiente
    if orientacao == Orientacao.LATERAL:
        curvado = dedos[4][y] < dedos[3][y]
        if not curvado:
            return Invalido("Polegar")

    elif orientacao == Orientacao.FRENTE:
        # Verifica se está dentro da palma
        if mao_direita:
            dentro_palma = dedos[4][x] > dedos[2][x]
        else:
            dentro_palma = dedos[4][x] < dedos[2][x]

        if dentro_palma:
            return Invalido("Polegar")

        # Verifica curvatura
        curvado = dedos[4][y] < dedos[3][y]

        if not curvado:
            return Invalido("Polegar")

    return Valido()


@registrar_validador(Dedo.POLEGAR_DENTRO)
def validar_dedo_polegar_dentro(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.BAIXO):
        if inclinacao != Inclinacao.RETA:
            raise exc

        # Verifica se está fora da palma
        mao_direita = dedos[2][x] < dedos[17][x]
        if mao_direita:
            fora_palma = dedos[4][x] < dedos[2][x]
        else:
            fora_palma = dedos[4][x] > dedos[2][x]

        if fora_palma:
            return Invalido("Polegar")

    elif orientacao == Orientacao.LATERAL:
        # Verifica se está fora da palma
        if inclinacao == Inclinacao.RETA:
            fora_palma = dedos[4][y] < dedos[5][y]
            if fora_palma:
                return Invalido("Polegar")

    elif orientacao == Orientacao.TRAS:
        # Verifica se está fora da palma
        mao_direita = dedos[2][x] < dedos[17][x]

        if inclinacao == Inclinacao.RETA:
            if mao_direita:
                fora_palma = dedos[4][x] < dedos[2][x]
            else:
                fora_palma = dedos[4][x] > dedos[2][x]

        elif inclinacao == Inclinacao.DENTRO_45:
            if mao_direita:
                fora_palma = dedos[4][x] < dedos[5][x]
            else:
                fora_palma = dedos[4][x] > dedos[5][x]

        elif inclinacao == Inclinacao.DENTRO_90:
            fora_palma = dedos[4][y] < dedos[2][y]

        elif inclinacao == Inclinacao.DENTRO_180:
            if mao_direita:
                fora_palma = dedos[4][x] < dedos[2][x]
            else:
                fora_palma = dedos[4][x] > dedos[2][x]

        if fora_palma:
            return Invalido("Polegar")

    else:
        raise exc

    return Valido()


@registrar_validador(Dedo.POLEGAR_FORA)
def validar_dedo_polegar_fora(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.BAIXO):
        raise exc

    # Verifica se está dentro da palma
    mao_direita = dedos[2] < dedos[17]
    if mao_direita:
        dentro_palma = dedos[4][x] > dedos[2][x]
    else:
        dentro_palma = dedos[4][x] < dedos[2][x]

    if dentro_palma:
        return Invalido("Polegar")

    return Valido()
