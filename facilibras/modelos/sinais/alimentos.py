from facilibras.modelos.mao import Dedo, Expressao, Inclinacao, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras

Agua = (
    SinalLibras(Categoria.ALIMENTOS, "água")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .posicao_mao(Posicao.BOCA, ponto_ref=8)
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .depois()
    .configuracao_anterior(0)
)

Biscoito = (
    SinalLibras(Categoria.ALIMENTOS, "biscoito")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .posicao_mao(Posicao.SOMBRANCELHA, ponto_ref=8)
)

Bolacha = (
    SinalLibras(Categoria.ALIMENTOS, "bolacha")
    .mao(
        Dedo.POLEGAR_CURVADO,
        Dedo.INDICADOR_CURVADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_45)
    .posicao_mao(Posicao.QUEIXO, ponto_ref=5)
    .expressao_facial(Expressao.BOCA_ABERTA)
)
