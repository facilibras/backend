from facilibras.modelos.mao import Dedo, Inclinacao, Movimento, Orientacao
from facilibras.modelos.sinais import Categoria, SinalLibras

LetraA = (
    SinalLibras(Categoria.ALFABETO, "A")
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
    SinalLibras(Categoria.ALFABETO, "B")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_BAIXO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraC = (
    SinalLibras(Categoria.ALFABETO, "C")
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
    SinalLibras(Categoria.ALFABETO, "Ç")
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
    SinalLibras(Categoria.ALFABETO, "D")
    .mao(
        Dedo.INDICADOR_ENC_POLEGAR,
        Dedo.MEDIO_ENC_POLEGAR,
        Dedo.ANELAR_ENC_POLEGAR,
        Dedo.MINIMO_CIMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
)

LetraE = (
    SinalLibras(Categoria.ALFABETO, "E")
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
    SinalLibras(Categoria.ALFABETO, "F")
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
    SinalLibras(Categoria.ALFABETO, "G")
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
    SinalLibras(Categoria.ALFABETO, "H")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.TRAS)
)

LetraI = (
    SinalLibras(Categoria.ALFABETO, "I")
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
    SinalLibras(Categoria.ALFABETO, "J")
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
    SinalLibras(Categoria.ALFABETO, "K")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .movimento(Movimento.CIMA)
)

LetraL = (
    SinalLibras(Categoria.ALFABETO, "L")
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
    SinalLibras(Categoria.ALFABETO, "M")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_CIMA,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraN = (
    SinalLibras(Categoria.ALFABETO, "N")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraO = (
    SinalLibras(Categoria.ALFABETO, "O")
    .mao(
        Dedo.INDICADOR_ENC_POLEGAR,
        Dedo.MEDIO_ENC_POLEGAR,
        Dedo.ANELAR_ENC_POLEGAR,
        Dedo.MINIMO_CURVADO,
    )
    .orientacao_palma(Orientacao.LATERAL)
)

LetraP = (
    SinalLibras(Categoria.ALFABETO, "P")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_CIMA,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_45)
)

LetraQ = (
    SinalLibras(Categoria.ALFABETO, "Q")
    .mao(
        Dedo.POLEGAR_CIMA,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraR = (
    SinalLibras(Categoria.ALFABETO, "R")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_MEDIO_CRUZADO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraS = (
    SinalLibras(Categoria.ALFABETO, "S")
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
    SinalLibras(Categoria.ALFABETO, "T")
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
    SinalLibras(Categoria.ALFABETO, "U")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ENC_MEDIO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraV = (
    SinalLibras(Categoria.ALFABETO, "V")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DIST_MEDIO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraW = (
    SinalLibras(Categoria.ALFABETO, "W")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DIST_MEDIO,
        Dedo.MEDIO_DIST_ANELAR,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraX = (
    SinalLibras(Categoria.ALFABETO, "X")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FLEXIONADO,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.BAIXO)
    .movimento(Movimento.TRAS)
)

LetraY = (
    SinalLibras(Categoria.ALFABETO, "Y")
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
LetraZ = (
    SinalLibras(Categoria.ALFABETO, "Z")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_CIMA,
        Dedo.MEDIO_BAIXO,
        Dedo.ANELAR_BAIXO,
        Dedo.MINIMO_BAIXO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .movimento(Movimento.DIREITA, Movimento.BAIXO_ESQUERDA, Movimento.DIREITA)
)
