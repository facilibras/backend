from facilibras.modelos.mao import Dedo, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras2Maos

Porta = (
    SinalLibras2Maos(Categoria.OUTROS, "porta")
    .mao_esquerda(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Configuração incial da mão esquerda")
    .mao_direita(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_OPOSTO, 5)
    .descricao("Configuração incial da mão direita")
    .depois()
    .mao_esquerda(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Abrir a porta com a mão esquerda")
    .mao_direita(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Mão direita na mesma posição")
)
