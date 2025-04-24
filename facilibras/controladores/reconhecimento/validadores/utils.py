import math

from facilibras.modelos.mao import Inclinacao, Orientacao

XYZ = tuple[float, float, float]


def distancia_euclidiana(p1: XYZ, p2: XYZ) -> float:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def produto_vetorial(v1: XYZ, v2: XYZ):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return (y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2)


def calcular_orientacao_atual(dedos: list[float]) -> Orientacao: ...


def calcular_inclinacao_atual(dedos: list[float]) -> Inclinacao: ...
