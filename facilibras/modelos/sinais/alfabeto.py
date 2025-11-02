from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras

LetraA = (
    SinalLibras(Categoria.ALFABETO, "letra_a")
    .mao(
        Dedo.POLEGAR_CIMA,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraB = (
    SinalLibras(Categoria.ALFABETO, "letra_b")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_CIMA,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraC = (
    SinalLibras(Categoria.ALFABETO, "letra_c")
    .mao(
        Dedo.POLEGAR_CURVADO,
        Dedo.INDICADOR_CURVADO,
        Dedo.MEDIO_CURVADO,
        Dedo.ANELAR_CURVADO,
        Dedo.MINIMO_CURVADO,
    )
    .orientacao_palma(Orientacao.LATERAL)
)

LetraCC = (
    SinalLibras(Categoria.ALFABETO, "letra_ç")
    .mao(
        Dedo.POLEGAR_CURVADO,
        Dedo.INDICADOR_CURVADO,
        Dedo.MEDIO_CURVADO,
        Dedo.ANELAR_CURVADO,
        Dedo.MINIMO_CURVADO,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .depois()
    .mao(
        Dedo.POLEGAR_CURVADO,
        Dedo.INDICADOR_CURVADO,
        Dedo.MEDIO_CURVADO,
        Dedo.ANELAR_CURVADO,
        Dedo.MINIMO_CURVADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraD = (
    SinalLibras(Categoria.ALFABETO, "letra_d")
    .mao(
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_ENC_POLEGAR,
        Dedo.ANELAR_ENC_POLEGAR,
        Dedo.MINIMO_CURVADO,
    )
    .orientacao_palma(Orientacao.LATERAL)
)

LetraE = (
    SinalLibras(Categoria.ALFABETO, "letra_e")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FLEXIONADO,
        Dedo.MEDIO_FLEXIONADO,
        Dedo.ANELAR_FLEXIONADO,
        Dedo.MINIMO_FLEXIONADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraF = (
    SinalLibras(Categoria.ALFABETO, "letra_f")
    .mao(
        Dedo.POLEGAR_CIMA,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_CIMA,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraG = (
    SinalLibras(Categoria.ALFABETO, "letra_g")
    .mao(
        Dedo.POLEGAR_CIMA,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraH = (
    SinalLibras(Categoria.ALFABETO, "letra_h")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.TRAS)
)

LetraI = (
    SinalLibras(Categoria.ALFABETO, "letra_i")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraJ = (
    SinalLibras(Categoria.ALFABETO, "letra_j")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
)

LetraK = (
    SinalLibras(Categoria.ALFABETO, "letra_k")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_FRENTE_45,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraL = (
    SinalLibras(Categoria.ALFABETO, "letra_l")
    .mao(
        Dedo.POLEGAR_FORA,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraM = (
    SinalLibras(Categoria.ALFABETO, "letra_m")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_CIMA,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_180)
)

LetraN = (
    SinalLibras(Categoria.ALFABETO, "letra_n")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_180)
)

LetraO = (
    SinalLibras(Categoria.ALFABETO, "letra_o")
    .mao(
        Dedo.INDICADOR_ENC_POLEGAR,
        Dedo.MEDIO_ENC_POLEGAR,
        Dedo.ANELAR_ENC_POLEGAR,
        Dedo.MINIMO_CURVADO,
    )
    .orientacao_palma(Orientacao.LATERAL)
)

LetraP = (
    SinalLibras(Categoria.ALFABETO, "letra_p")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_45)
)

LetraQ = (
    SinalLibras(Categoria.ALFABETO, "letra_q")
    .mao(
        Dedo.POLEGAR_CIMA,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_180)
)

LetraR = (
    SinalLibras(Categoria.ALFABETO, "letra_r")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_MEDIO_CRUZADO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraS = (
    SinalLibras(Categoria.ALFABETO, "letra_s")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraT = (
    SinalLibras(Categoria.ALFABETO, "letra_t")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_CIMA,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraU = (
    SinalLibras(Categoria.ALFABETO, "letra_u")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ENC_MEDIO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraV = (
    SinalLibras(Categoria.ALFABETO, "letra_v")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DIST_MEDIO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraW = (
    SinalLibras(Categoria.ALFABETO, "letra_w")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DIST_MEDIO,
        Dedo.MEDIO_DIST_ANELAR,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

_mao_x = [
    Dedo.POLEGAR_DENTRO,
    Dedo.INDICADOR_FLEXIONADO,
    Dedo.MEDIO_BAIXO,
    Dedo.ANELAR_BAIXO,
    Dedo.MINIMO_BAIXO,
]
LetraX = (
    SinalLibras(Categoria.ALFABETO, "letra_x")
    .mao(*_mao_x)
    .orientacao_palma(Orientacao.BAIXO)
    .posicao_mao(Posicao.DISTANTE_AO_CORPO, ponto_ref=0)
    .depois()
    .mao(*_mao_x)
    .orientacao_palma(Orientacao.BAIXO)
    .posicao_mao(Posicao.PROXIMO_AO_CORPO, ponto_ref=0)
)

LetraY = (
    SinalLibras(Categoria.ALFABETO, "letra_y")
    .mao(
        Dedo.POLEGAR_FORA,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.BAIXO)
    .depois()
    .mao(
        Dedo.POLEGAR_FORA,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

_mao_z = [
    Dedo.POLEGAR_DENTRO,
    Dedo.INDICADOR_CIMA,
    Dedo.MEDIO_BAIXO,
    Dedo.ANELAR_BAIXO,
    Dedo.MINIMO_BAIXO,
]
LetraZ = (
    SinalLibras(Categoria.ALFABETO, "letra_z")
    .mao(*_mao_z)
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_ESQUERDO_CIMA, ponto_ref=12)
    .depois()
    .mao(*_mao_z)
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_DIREITA_CIMA, ponto_ref=12)
    .depois()
    .mao(*_mao_z)
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_ESQUERDO_BAIXO, ponto_ref=12)
    .depois()
    .mao(*_mao_z)
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_DIREITA_BAIXO, ponto_ref=12)
)
