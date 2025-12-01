import math

from facilibras.controladores.reconhecimento.validadores import Regiao

XYZ = tuple[float, float, float]


def distancia(p1: float, p2: float) -> float:
    return abs(p1 - p2)


def distancia2(p1: XYZ, p2: XYZ) -> float:
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx**2 + dy**2)


def distancia3(p1: XYZ, p2: XYZ) -> float:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def produto_vetorial(v1: XYZ, v2: XYZ):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return (y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2)


def ponto_em_regiao(pos: tuple[float, float, float], regiao: Regiao) -> bool:
    x, y, _ = pos

    match regiao:
        case Regiao.INFERIOR_ESQUERDA:
            return x < 0.5 and y >= 0.5
        case Regiao.INFERIOR_DIREITA:
            return x >= 0.5 and y >= 0.5
        case Regiao.SUPERIOR_ESQUERDA:
            return x < 0.5 and y < 0.5
        case Regiao.SUPERIOR_DIREITA:
            return x >= 0.5 and y < 0.5
        case Regiao.CIMA:
            return y < 0.5
        case Regiao.ESQUERDA:
            return x < 0.5
        case Regiao.DIREITA:
            return x > 0.5
        case Regiao.BAIXO:
            return y > 0.5
