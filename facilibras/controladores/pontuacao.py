NIVEIS = {1: 100, 2: 500, 3: 1000, 4: 3000, 5: 5000}
PONTOS_PRIMEIRA_VEZ = 100


def pontos_para_subir(nivel_atual: int, pontos_nivel: int) -> int:
    proximo_nivel = NIVEIS.get(nivel_atual)
    if proximo_nivel is None:
        return 0  # já no nível máximo
    return max(proximo_nivel - pontos_nivel, 0)


def calcular_porcentagem(nivel_atual: int, pontos_nivel: int) -> int:
    proximo_nivel = NIVEIS.get(nivel_atual)
    if not proximo_nivel or proximo_nivel <= 0:
        return 100

    porcentagem = (pontos_nivel / proximo_nivel) * 100
    return min(max(int(porcentagem), 0), 100)
