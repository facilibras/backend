import facilibras.controladores.reconhecimento.validadores.utils as utils
from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Regiao,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.modelos.mao import Mao, Posicao

T_Ponto = tuple[float, float, float]
T_Corpo = dict[int, T_Ponto]

x, y, z = range(3)


@registrar_validador(Posicao.BOCA)
def validar_posicao_boca(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver na região da boca definida por um retângulo:
    - largura: entre os pontos 3 e 6 (horizontal)
    - altura: distância do nariz ao lábio inferior, para cima e para baixo da boca
    """
    labio_inferior = corpo[10]
    labio_superior = corpo[9]
    nariz = corpo[0]

    x_min = min(corpo[3][x], corpo[6][x])
    x_max = max(corpo[3][x], corpo[6][x])

    altura_ref = abs(labio_inferior[y] - nariz[y])
    y_centro = (labio_superior[y] + labio_inferior[y]) / 2

    y_min = y_centro - altura_ref
    y_max = y_centro + altura_ref

    x_ok = x_min <= pos_dedo[x] <= x_max
    y_ok = y_min <= pos_dedo[y] <= y_max

    if x_ok and y_ok:
        return Valido()
    return Invalido("Mão deve estar na frente da boca")


@registrar_validador(Posicao.CENTRO)
def validar_posicao_centro(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se o ponto estiver no terço central do eixo X.
    A posição em Y não importa.
    """
    px = pos_dedo[x]
    limite_inferior = 1 / 3
    limite_superior = 2 / 3

    if limite_inferior <= px <= limite_superior:
        return Valido()
    return Invalido("Mão deve estar próximo da região central do quadro")


@registrar_validador(Posicao.DISTANTE_AO_CORPO)
def validar_posicao_distante_ao_corpo(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver distante ao corpo
    assume a grande maioria das vezes a mão está acima da boca quando distante
    (achar forma melhor!)
    """
    centro_boca_y = (corpo[9][y] + corpo[10][y]) / 2

    if pos_dedo[y] < centro_boca_y:
        return Valido()

    return Invalido("Mão deve estar distante do corpo e centralizada")


@registrar_validador(Posicao.LADO_ESQUERDO_BAIXO)
def validar_posicao_lado_esquerdo_baixo(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver no quadrante inferior esquerdo da tela
    """
    if utils.ponto_em_regiao(pos_dedo, Regiao.INFERIOR_ESQUERDA):
        return Valido()
    return Invalido("Mão deve se deslocar para a esquerda, reduzindo a altura.")


@registrar_validador(Posicao.LADO_ESQUERDO_CIMA)
def validar_posicao_lado_esquerdo_cima(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver no quadrante superior esquerdo da tela
    """
    if utils.ponto_em_regiao(pos_dedo, Regiao.SUPERIOR_ESQUERDA):
        return Valido()
    return Invalido("Mão deve estar mais alta e deslocada para esquerda")


@registrar_validador(Posicao.LADO_DIREITA_BAIXO)
def validar_posicao_lado_direita_baixo(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver no quadrante inferior direito da tela
    """
    if utils.ponto_em_regiao(pos_dedo, Regiao.INFERIOR_DIREITA):
        return Valido()
    return Invalido("Mão deve se deslocar para a direita, mantendo a altura.")


@registrar_validador(Posicao.LADO_DIREITA_CIMA)
def validar_posicao_lado_direita_cima(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver no quadrante superior direito da tela
    """
    if utils.ponto_em_regiao(pos_dedo, Regiao.SUPERIOR_DIREITA):
        return Valido()
    return Invalido("Mão deve se deslocar para a direita, mantendo a altura.")


@registrar_validador(Posicao.LADO_OPOSTO)
def validar_posicao_lado_oposto(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se cada mão estiver no lado oposto ao seu lado natural
    (mão esquerda no lado direito e mão direita no lado esquerdo)
    """
    if mao == Mao.ESQUERDA:
        correto = utils.ponto_em_regiao(pos_dedo, Regiao.DIREITA)
    else:  # mao == Mao.DIREITA:
        correto = utils.ponto_em_regiao(pos_dedo, Regiao.ESQUERDA)

    if correto:
        return Valido()
    return Invalido("Mão deve estar no lado oposto do seu lado natural")


@registrar_validador(Posicao.MESMO_LADO)
def validar_posicao_mesmo_lado(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se não houver cruzamento de lados entre as mãos
    (mão esquerda no lado esquerdo e mão direita no lado direito)
    """
    if mao == Mao.ESQUERDA:
        correto = utils.ponto_em_regiao(pos_dedo, Regiao.ESQUERDA)
    else:  # mao == Mao.DIREITA:
        correto = utils.ponto_em_regiao(pos_dedo, Regiao.DIREITA)

    if correto:
        return Valido()
    return Invalido("Mão não deve estar cruzando lado oposto do corpo.")


@registrar_validador(Posicao.OMBRO_PRA_CIMA)
def validar_posicao_ombro_pra_cima(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se o ponto estiver acima dos ombros
    (região da cabeça, orelhas, etc.)
    """
    ombro_esq = corpo[11]
    ombro_dir = corpo[12]
    y_min = min(ombro_esq[y], ombro_dir[y])

    if pos_dedo[y] <= y_min:
        return Valido()

    return Invalido("Mão deve estar acima dos ombros")


@registrar_validador(Posicao.ORELHA)
def validar_posicao_orelha(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver acima dos ombros e lateral da cabeça,
    desde que não esteja na região central entre os olhos.
    """
    ombro_esq = corpo[11]
    ombro_dir = corpo[12]
    olho_dir = corpo[3]
    olho_esq = corpo[6]
    orelha_esq = corpo[8]
    orelha_dir = corpo[7]

    y_lim = min(ombro_esq[y], ombro_dir[y])
    if pos_dedo[y] > y_lim:
        return Invalido("Mão deve estar próximo de uma orelha")

    x_min_olhos = min(olho_esq[x], olho_dir[x])
    x_max_olhos = max(olho_esq[x], olho_dir[x])
    if x_min_olhos <= pos_dedo[x] <= x_max_olhos:
        return Invalido("Mão deve estar próximo de uma orelha")

    lateral_direita = pos_dedo[x] > olho_dir[x]
    lateral_esquerda = pos_dedo[x] < olho_esq[x]

    distancia_max = utils.distancia(orelha_esq[x], orelha_dir[x]) * 1.5
    perto_orelha = (
        utils.distancia(pos_dedo[x], orelha_esq[x]) <= distancia_max
        or utils.distancia(pos_dedo[x], orelha_dir[x]) <= distancia_max
    )

    if (lateral_esquerda or lateral_direita) and perto_orelha:
        return Valido()

    return Invalido("Mão deve estar próximo de uma orelha")


@registrar_validador(Posicao.PEITO)
def validar_posicao_peito(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se o ponto estiver na região do peito
    (entre os ombros horizontalmente e abaixo deles verticalmente)
    """
    ombro_esq = corpo[11]
    ombro_dir = corpo[12]

    # entre os ombros
    x_min = min(ombro_esq[x], ombro_dir[x])
    x_max = max(ombro_esq[x], ombro_dir[x])

    # abaixo da linha dos ombros
    y_min = max(ombro_esq[y], ombro_dir[y])

    x_ok = x_min <= pos_dedo[x] <= x_max
    y_ok = pos_dedo[y] >= y_min

    if x_ok and y_ok:
        return Valido()

    return Invalido("Ponto deve estar na região do peito")


@registrar_validador(Posicao.PROXIMO_AO_CORPO)
def validar_posicao_proximo_ao_corpo(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver distante ao corpo
    assume a grande maioria das vezes a mão está abaixo da boca quando distante
    (achar forma melhor!)
    """
    centro_boca_y = (corpo[9][y] + corpo[10][y]) / 2

    if pos_dedo[y] >= centro_boca_y:
        return Valido()

    return Invalido("Mão deve estar mais próxima do corpo")


@registrar_validador(Posicao.QUALQUER)
def validar_posicao_qualquer(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se independente de posição
    """
    return Valido()


@registrar_validador(Posicao.QUEIXO)
def validar_posicao_queixo(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver na região do queixo
    (a partir da área entre nariz e ombros)
    """
    nariz = corpo[0]
    ombro_esq = corpo[11]
    ombro_dir = corpo[12]

    # determinando a área (nariz/ombros)
    x_min = min(ombro_esq[x], ombro_dir[x])
    x_max = max(ombro_esq[x], ombro_dir[x])
    y_min = nariz[y]
    y_max = max(ombro_esq[y], ombro_dir[y])

    x_ok = x_min <= pos_dedo[x] <= x_max
    y_ok = y_min <= pos_dedo[y] <= y_max

    if x_ok and y_ok:
        return Valido()
    return Invalido("Ponto deve estar na região do queixo")


@registrar_validador(Posicao.SOMBRANCELHA)
def validar_posicao_sombrancelha(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver na região das sombrancelhas
    (a partir da área entre sombrancelhas, nariz e testa)
    """
    olho_dir = corpo[1]
    olho_esq = corpo[4]
    nariz = corpo[0]

    # linha dos olhos (altura de referência)
    y_olho = (olho_dir[y] + olho_esq[y]) / 2

    altura = abs(y_olho - nariz[y])
    y_min = y_olho - altura
    y_max = y_olho

    # entre olhos
    x_min = min(olho_dir[x], olho_esq[x])
    x_max = max(olho_dir[x], olho_esq[x])

    x_ok = x_min <= pos_dedo[x] <= x_max
    y_ok = y_min <= pos_dedo[y] <= y_max

    if x_ok and y_ok:
        return Valido()
    return Invalido("Mão deve estar na região das sobrancelhas")


@registrar_validador(Posicao.TESTA)
def validar_posicao_testa(
    pos_dedo: T_Ponto, pos_anterior: T_Ponto, corpo: T_Corpo, mao: Mao
) -> Resultado:
    """
    Considera válido se estiver na região da testa
    (acima das sombrancelhas mas não fora da cabeça)
    """
    sobrancelha_dir = corpo[2]
    sobrancelha_esq = corpo[5]
    nariz = corpo[0]
    orelha_dir = corpo[7]
    orelha_esq = corpo[8]

    x_min = min(orelha_esq[x], orelha_dir[x])
    x_max = max(orelha_esq[x], orelha_dir[x])

    altura_ref = max(
        utils.distancia2(sobrancelha_dir, nariz),
        utils.distancia2(sobrancelha_esq, nariz),
    )
    altura_max = 2 * altura_ref

    y_sobrancelha = min(sobrancelha_dir[y], sobrancelha_esq[y])
    dentro_altura = (y_sobrancelha - altura_max) <= pos_dedo[y] <= y_sobrancelha
    dentro_largura = x_min <= pos_dedo[x] <= x_max

    if dentro_altura and dentro_largura:
        return Valido()
    return Invalido("Mão deve estar na região da testa")
