from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras

Entender = (
    SinalLibras(Categoria.VERBOS, "entender")
    .mao(
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_45)
    .posicao_mao(Posicao.TESTA, ponto_ref=8)
    .descricao("Configuração inicial da mão")
    .depois()
    .mao(
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .inclinacao_palma(Inclinacao.DENTRO_45)
    .posicao_mao(Posicao.TESTA, ponto_ref=20)
    .descricao("Virar a palma para frente")
)

Ouvir = (
    SinalLibras(Categoria.VERBOS, "ouvir")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.ORELHA, ponto_ref=5)
    .descricao("Configuração inicial da mão")
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.ORELHA, ponto_ref=6)
    .descricao("Fechar a mão do lado da orelha")
)

Aprender = (
    SinalLibras(Categoria.VERBOS, "aprender")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .inclinacao_palma(Inclinacao.DENTRO_45)
    .posicao_mao(Posicao.TESTA, ponto_ref=10)
    .descricao("Configuração inicial da mão")
    .depois()
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.TESTA, ponto_ref=9)
    .descricao("Abrir a mão")
    .depois()
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .inclinacao_palma(Inclinacao.DENTRO_45)
    .posicao_mao(Posicao.TESTA, ponto_ref=9)
    .descricao("Fechar a mão")
)

Saber = (
    SinalLibras(Categoria.VERBOS, "saber")
    .mao(
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .posicao_mao(Posicao.TESTA, ponto_ref=12)
    .descricao("Configuração inicial da mão")
    .depois()
    .mao(
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
    .posicao_mao(Posicao.OMBRO_PRA_CIMA, ponto_ref=17)
    .descricao("Fechar a mão enquanto afasta do rosto")
)
