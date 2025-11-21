from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras


Meu = (
    SinalLibras(Categoria.IDENTIDADE, "meu")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
    .posicao_mao(Posicao.PEITO, ponto_ref=9)
)

Seu = (
    SinalLibras(Categoria.IDENTIDADE, "seu")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
    .descricao("Configuração inicial do sinal")
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .inclinacao_palma(Inclinacao.FORA_90)
    .descricao("Apontar para frente do corpo")
)

Eu = (
    SinalLibras(Categoria.IDENTIDADE, "eu")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
)

Voce = (
    SinalLibras(Categoria.IDENTIDADE, "você")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .inclinacao_palma(Inclinacao.FORA_90)
)

Nome = (
    SinalLibras(Categoria.IDENTIDADE, "nome")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_OPOSTO, ponto_ref=8)
    .descricao("Configuração inicial da mão")
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, ponto_ref=12)
    .descricao("Movimento de dentro para fora")
)
