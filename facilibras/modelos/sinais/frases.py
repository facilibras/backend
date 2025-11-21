from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras

Oi_Tudo_Bem = (
    SinalLibras(Categoria.FRASES, "oi_tudo_bem")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_OPOSTO, ponto_ref=6)
    .descricao("Configuração do sinal do Oi")
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, ponto_ref=20)
    .descricao("Movimento de dentro para fora")
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .posicao_mao(Posicao.QUEIXO, ponto_ref=9)
    .descricao("Mão fechada na frente do rosto")
    .depois()
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .descricao("Abra sua mão")
    .depois()
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
    .descricao("Faça o sinal do joinha")
)
