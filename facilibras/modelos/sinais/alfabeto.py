from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras

LetraA = (
    SinalLibras(Categoria.ALFABETO, "letra_a")
    .mao(
        Dedo.POLEGAR_ENC_LATERAL,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraB = (
    SinalLibras(Categoria.ALFABETO, "letra_b")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
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
    .descricao("Configuração inicial do sinal")
    .depois()
    .mao(
        Dedo.POLEGAR_CURVADO,
        Dedo.INDICADOR_CURVADO,
        Dedo.MEDIO_CURVADO,
        Dedo.ANELAR_CURVADO,
        Dedo.MINIMO_CURVADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .descricao("Movimento da palma para a frente")
)

LetraD = (
    SinalLibras(Categoria.ALFABETO, "letra_d")
    .mao(
        Dedo.INDICADOR_ESTICADO,
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
        Dedo.POLEGAR_ENC_LATERAL,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraG = (
    SinalLibras(Categoria.ALFABETO, "letra_g")
    .mao(
        Dedo.POLEGAR_ENC_LATERAL,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraH = (
    SinalLibras(Categoria.ALFABETO, "letra_h")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .descricao("Configuração inicial do sinal")
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .descricao("Movimento da palma para a trás")
)

LetraI = (
    SinalLibras(Categoria.ALFABETO, "letra_i")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraJ = (
    SinalLibras(Categoria.ALFABETO, "letra_j")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .descricao("Configuração inicial do sinal")
    .depois()
    .configuracao_anterior()
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
    .descricao("Movimento curvo da letra J")
)

LetraK = (
    SinalLibras(Categoria.ALFABETO, "letra_k")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_FRENTE_45,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraL = (
    SinalLibras(Categoria.ALFABETO, "letra_l")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraM = (
    SinalLibras(Categoria.ALFABETO, "letra_m")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_180)
)

LetraN = (
    SinalLibras(Categoria.ALFABETO, "letra_n")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
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
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_45)
)

LetraQ = (
    SinalLibras(Categoria.ALFABETO, "letra_q")
    .mao(
        Dedo.POLEGAR_ENC_LATERAL,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_180)
)

LetraR = (
    SinalLibras(Categoria.ALFABETO, "letra_r")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_MEDIO_CRUZADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraS = (
    SinalLibras(Categoria.ALFABETO, "letra_s")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraT = (
    SinalLibras(Categoria.ALFABETO, "letra_t")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraU = (
    SinalLibras(Categoria.ALFABETO, "letra_u")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ENC_MEDIO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraV = (
    SinalLibras(Categoria.ALFABETO, "letra_v")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DIST_MEDIO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraW = (
    SinalLibras(Categoria.ALFABETO, "letra_w")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_DIST_MEDIO,
        Dedo.MEDIO_DIST_ANELAR,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

LetraX = (
    SinalLibras(Categoria.ALFABETO, "letra_x")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_FLEXIONADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.BAIXO)
    .posicao_mao(Posicao.DISTANTE_AO_CORPO, ponto_ref=0)
    .descricao("Configuração inicial do sinal")
    .depois()
    .configuracao_anterior()
    .posicao_mao(Posicao.PROXIMO_AO_CORPO)
    .descricao("Movimento para trás")
)

LetraY = (
    SinalLibras(Categoria.ALFABETO, "letra_y")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.BAIXO)
    .descricao("Configuração inicial do sinal")
    .depois()
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .descricao("Movimento de baixo para cima")
)

LetraZ = (
    SinalLibras(Categoria.ALFABETO, "letra_z")
    .mao(
        Dedo.POLEGAR_DENTRO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_ESQUERDO_CIMA, ponto_ref=12)
    .descricao("Configuração inicial do sinal na metade superior esquerda.")
    .depois()
    .configuracao_anterior(exceto_posicao=Posicao.LADO_DIREITA_CIMA)
    .descricao("Movimento para a metade superior direita da tela")
    .depois()
    .configuracao_anterior(exceto_posicao=Posicao.LADO_ESQUERDO_BAIXO)
    .descricao("Movimento para a metade inferior esquerda da tela")
    .depois()
    .configuracao_anterior(exceto_posicao=Posicao.LADO_DIREITA_BAIXO)
    .descricao("Movimento para a metade inferior direita da tela")
)
