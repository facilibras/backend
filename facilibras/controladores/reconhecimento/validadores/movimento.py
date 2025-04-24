from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Validando,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Movimento

Ponto = tuple[float, float, float]

x, y, z = range(3)


@registrar_validador(Movimento.CIMA)
def validar_movimento_cima(
    pos_anterior: Ponto,
    pos_atual: Ponto,
    acumulado: Ponto,
    limiar_correto: int,
    limiar_incorreto: int,
) -> Resultado:
    # Chegagem de movimento em horizontal
    mov_x = pos_atual[x] - pos_anterior[x] + acumulado[x]
    if abs(mov_x) >= limiar_incorreto:
        return Invalido()

    # Checagem de movimento vertical
    mov_y = pos_atual[y] - pos_anterior[y] + acumulado[y]
    if mov_y >= limiar_incorreto:
        return Invalido()
    if mov_y <= -limiar_correto:
        return Valido()

    # Movimento não suficiente
    return Validando((mov_x, mov_y))


@registrar_validador(Movimento.DIREITA)
def validar_movimento_direita(
    pos_anterior: Ponto,
    pos_atual: Ponto,
    acumulado: Ponto,
    limiar_correto: int,
    limiar_incorreto: int,
) -> Resultado:
    # Chegagem de movimento em vertical
    mov_y = pos_atual[y] - pos_anterior[y] + acumulado[y]
    if abs(mov_y) >= limiar_incorreto:
        return Invalido()

    # Chegagem de movimento em horizontal
    mov_x = pos_atual[x] - pos_anterior[x] + acumulado[x]
    if mov_x <= -limiar_incorreto:
        return Invalido()
    if mov_x >= limiar_correto:
        return Valido()

    # Movimento não suficiente
    return Validando((mov_x, mov_y))


@registrar_validador(Movimento.TRAS)
def validar_movimento_tras(
    pos_anterior: Ponto,
    pos_atual: Ponto,
    acumulado: Ponto,
    limiar_correto: int,
    limiar_incorreto: int,
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Movimento.BAIXO_ESQUERDA)
def validar_movimento_baixo_esquerda(
    pos_anterior: Ponto,
    pos_atual: Ponto,
    acumulado: Ponto,
    limiar_correto: int,
    limiar_incorreto: int,
) -> Resultado:
    # Checagem de movimento contrário (direita)
    mov_x = pos_atual[x] - pos_anterior[x] + acumulado[x]
    if mov_x >= limiar_incorreto:
        return Invalido()

    # Checagem de movimento contrário (cima)
    mov_y = pos_atual[y] - pos_anterior[y] + acumulado[y]
    if mov_y <= -limiar_incorreto:
        return Invalido()

    # Suficiente na direção horizontal (esquerda)
    if mov_x <= -limiar_correto and mov_y >= limiar_correto // 2:
        return Valido()

    # Suficiente na direção vertical (baixo)
    if mov_x <= -limiar_correto // 2 and mov_y >= limiar_correto:
        return Valido()

    # Movimento não suficiente
    return Validando((mov_x, mov_y))
