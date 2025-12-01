from facilibras.modelos.mao import Dedo, Orientacao, Posicao
from facilibras.modelos.sinais import Categoria, SinalLibras2Maos

Porta = (
    SinalLibras2Maos(Categoria.OUTROS, "porta")
    .mao_esquerda(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.LADO_OPOSTO, 5)
    .descricao("Configuração inicial da mão esquerda")
    .mao_direita(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Configuração inicial da mão direita")
    .depois()
    .mao_esquerda(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Abrir a porta com a mão esquerda")
    .mao_direita(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Mão direita na mesma posição")
)

Muro = (
    SinalLibras2Maos(Categoria.OUTROS, "muro")
    .mao_esquerda(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.CENTRO, 5)
    .descricao("Configuração inicial da mão esquerda")
    .mao_direita(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.CENTRO, 5)
    .descricao("Configuração inicial da mão direita")
    .depois()
    .mao_esquerda(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Movimentar mão esquerda para esquerda")
    .mao_direita(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.FRENTE)
    .posicao_mao(Posicao.MESMO_LADO, 5)
    .descricao("Movimentar mão esquerda para direita")
)
