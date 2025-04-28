from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Resultado,
    Valido,
    registrar_validador,
)
from facilibras.controladores.reconhecimento.validadores.utils import (
    distancia,
    distancia_euclidiana,
)
from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao

T_Dedos = dict[int, tuple[float, float, float]]

PROFUNDIDADE_BAIXO_CIMA = 0.02

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
        return Invalido()

    # Verifica se o polegar está para dentro da palma
    mao_direita = dedos[3][x] < dedos[9][x]
    if mao_direita:
        dentro_palma = dedos[4][x] > dedos[2][x]
    else:
        dentro_palma = dedos[4][x] < dedos[2][x]

    if dentro_palma:
        return Invalido()

    return Valido()


@registrar_validador(Dedo.POLEGAR_CURVADO)
def validar_dedo_polegar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.LATERAL):
        raise exc

    # Verifica se está dentro da palma
    if orientacao == Orientacao.LATERAL:
        mao_direita = dedos[5][x] < dedos[0][x]
    else:
        mao_direita = dedos[2][x] < dedos[17][x]

    if mao_direita:
        dentro_palma = dedos[4][x] > dedos[2][x]
    else:
        dentro_palma = dedos[4][x] < dedos[2][x]

    if dentro_palma:
        return Invalido()

    # Verifica curvatura suficiente
    if orientacao == Orientacao.LATERAL:
        curvado = dedos[4][y] < dedos[3][y]
        if not curvado:
            return Invalido()

    elif orientacao == Orientacao.FRENTE:
        if mao_direita:
            curvado = dedos[4][x] < dedos[3][x]
        else:
            curvado = dedos[4][x] < dedos[3][x]

        if not curvado:
            return Invalido()

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
            return Invalido()

    elif orientacao == Orientacao.LATERAL:
        # Verifica se está fora da palma
        if inclinacao == Inclinacao.RETA:
            fora_palma = dedos[4][z] < dedos[3][z]
            if fora_palma:
                return Invalido()
        elif inclinacao == Inclinacao.DENTRO_45:
            polegar_aberto = dedos[4][y] < dedos[3][y]
            if polegar_aberto:
                return Invalido()

    elif orientacao == Orientacao.TRAS:
        # Verifica se está fora da palma
        mao_direita = dedos[2][x] < dedos[17][x]

        if inclinacao in (Inclinacao.RETA, Inclinacao.DENTRO_45):
            if mao_direita:
                fora_palma = dedos[4][x] < dedos[2][x]
            else:
                fora_palma = dedos[4][x] > dedos[2][x]

        elif inclinacao == Inclinacao.DENTRO_90:
            fora_palma = dedos[4][y] < dedos[2][y]

        elif inclinacao == Inclinacao.DENTRO_180:
            if mao_direita:
                fora_palma = dedos[4][x] < dedos[2][x]
            else:
                fora_palma = dedos[4][x] > dedos[2][x]

        if fora_palma:
            return Invalido()

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
        return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_BAIXO)
def validar_dedo_indicador_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.BAIXO, Orientacao.TRAS):
        raise exc

    # Verifica se está para cima
    if orientacao in (Orientacao.FRENTE, Orientacao.BAIXO):
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido()

    elif orientacao == Orientacao.TRAS:
        if inclinacao != Inclinacao.DENTRO_90:
            raise exc

        para_cima = dedos[8][x] > dedos[6][x]
        if para_cima:
            return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_CIMA)
def validar_dedo_indicador_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.TRAS, Orientacao.LATERAL):
        raise exc

    # Verifica se está para baixo
    if orientacao in (Orientacao.FRENTE, Orientacao.LATERAL):
        if dedos[8][y] > dedos[6][y]:
            return Invalido()

    elif orientacao == Orientacao.TRAS:
        if inclinacao != Inclinacao.DENTRO_180:
            raise exc

        if dedos[8][y] < dedos[6][y]:
            return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_CURVADO)
def validar_dedo_indicador_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.LATERAL):
        raise exc

    # Verifica se está para cima
    para_cima = dedos[8][y] < dedos[6][y]
    if para_cima:
        return Invalido()

    # Verifica se está curvado demais (somente lateral)
    if orientacao == Orientacao.LATERAL:
        if inclinacao != Inclinacao.RETA:
            raise exc

        mao_direita = dedos[5][x] < dedos[0][x]
        if mao_direita:
            para_baixo = dedos[8][x] > dedos[6][x]
        else:
            para_baixo = dedos[8][x] < dedos[6][x]

        if para_baixo:
            return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_DIST_MEDIO)
def validar_dedo_indicador_dist_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE or inclinacao != Inclinacao.RETA:
        raise exc

    # Checa se os dedos estão próximos
    dist_entre_pontas = distancia(dedos[8][x], dedos[12][x])
    dist_entre_origens = distancia(dedos[5][x], dedos[9][x])
    if dist_entre_pontas < dist_entre_origens:
        return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_ENC_MEDIO)
def validar_dedo_indicador_enc_medio(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE or inclinacao != Inclinacao.RETA:
        raise exc

    # Checa se os dedos estão distantes
    dist_entre_pontas = distancia(dedos[8][x], dedos[12][x])
    dist_entre_origens = distancia(dedos[5][x], dedos[9][x])
    if dist_entre_pontas > dist_entre_origens:
        return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_ENC_POLEGAR)
def validar_dedo_indicador_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.LATERAL or inclinacao != Inclinacao.RETA:
        raise exc

    # Checa se os dedos estão distantes
    dist_maxima = distancia_euclidiana(dedos[8], dedos[7])
    dist_entre_pontas = distancia_euclidiana(dedos[8], dedos[4])
    if dist_entre_pontas > dist_maxima:
        return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_FLEXIONADO)
def validar_dedo_indicador_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao not in (Orientacao.FRENTE, Orientacao.BAIXO):
        raise exc

    if orientacao == Orientacao.FRENTE:
        # Verifica se está dobrado
        dobrado = dedos[8][y] > dedos[5][y]
        if dobrado:
            return Invalido()

        # Verifica se está para cima
        para_cima = dedos[8][y] < dedos[6][y]
        if para_cima:
            return Invalido()

    elif orientacao == Orientacao.BAIXO:
        # TODO: Testar logica semelhante na Orientacao.FRENTE
        dist_ponta = distancia(dedos[8][y], dedos[7][y])
        dist_origem = distancia(dedos[6][y], dedos[5][y])
        dist_media = distancia(dedos[7][y], dedos[6][y])
        if dist_media <= dist_ponta or dist_media <= dist_origem:
            return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_FRENTE_45)
def validar_dedo_indicador_frente_45(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.LATERAL:
        raise exc

    # Verifica se está para baixo
    para_baixo = dedos[8][y] < dedos[5][y]
    if para_baixo:
        return Invalido()

    # Verifica angulo insuficiente
    dist_ponta = distancia(dedos[8][x], dedos[7][x])
    dist_origem = distancia(dedos[7][x], dedos[5][x])

    if dist_origem < dist_ponta:
        return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_FRENTE_90)
def validar_dedo_indicador_frente_90(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE:
        raise exc

    # TODO: Utilizar profundidade
    # Compara distância entre dedo e articulação polegar
    dist_dedo = distancia(dedos[8][y], dedos[5][y])
    dist_mao = distancia(dedos[5][y], dedos[2][y])

    if dist_dedo > dist_mao:
        return Invalido()

    return Valido()


@registrar_validador(Dedo.INDICADOR_MEDIO_CRUZADO)
def validar_dedo_indicador_medio_cruzado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao != Orientacao.FRENTE:
        raise exc

    mao_direita = dedos[2] < dedos[17]
    if mao_direita:
        distantes = dedos[8][x] < dedos[12][x]
    else:
        distantes = dedos[8][x] > dedos[12][x]

    if distantes:
        return Invalido()

    return Valido()


@registrar_validador(Dedo.MEDIO_BAIXO)
def validar_dedo_medio_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[12][y] > dedos[10][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        if dedos[9][y] < dedos[10][y]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.MEDIO_CIMA)
def validar_dedo_medio_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_CURVADO)
def validar_dedo_medio_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_DIST_ANELAR)
def validar_dedo_medio_dist_anelar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_ENC_POLEGAR)
def validar_dedo_medio_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_FLEXIONADO)
def validar_dedo_medio_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MEDIO_FRENTE_45)
def validar_dedo_medio_frente_45(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()

@registrar_validador(Dedo.ANELAR_BAIXO)
def validar_dedo_anelar_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[16][y] > dedos[14][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        if dedos[13][y] < dedos[14][y]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.ANELAR_CIMA)
def validar_dedo_anelar_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.ANELAR_CURVADO)
def validar_dedo_anelar_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.ANELAR_ENC_POLEGAR)
def validar_dedo_anelar_enc_polegar(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.ANELAR_FLEXIONADO)
def validar_dedo_anelar_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MINIMO_BAIXO)
def validar_dedo_minimo_baixo(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[20][y] > dedos[18][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        if dedos[17][y] < dedos[18][y]:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.MINIMO_CIMA)
def validar_dedo_minimo_cima(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    if orientacao in (Orientacao.FRENTE, Orientacao.TRAS):
        if dedos[20][y] < dedos[18][y]:
            return Valido()
    elif orientacao == Orientacao.BAIXO:
        diff = abs(dedos[18][z] - dedos[17][z])
        if diff > 0.025:
            return Valido()
    else:
        raise NotImplementedError()

    return Invalido()


@registrar_validador(Dedo.MINIMO_CURVADO)
def validar_dedo_minimo_curvado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()


@registrar_validador(Dedo.MINIMO_FLEXIONADO)
def validar_dedo_minimo_flexionado(
    dedos: T_Dedos, orientacao: Orientacao, inclinacao: Inclinacao
) -> Resultado:
    raise NotImplementedError()
