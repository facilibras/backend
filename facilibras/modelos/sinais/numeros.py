from facilibras.modelos.mao import Dedo, Inclinacao, Orientacao
from facilibras.modelos.sinais import Categoria, SinalLibras
from facilibras.modelos.sinais.alfabeto import LetraO

# Ordinais
Numero1 = (
    SinalLibras(Categoria.NUMEROS, "número_1")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
)

Numero2 = (
    SinalLibras(Categoria.NUMEROS, "número_2")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
)

Numero3 = (
    SinalLibras(Categoria.NUMEROS, "número_4")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
)

Numero4 = (
    SinalLibras(Categoria.NUMEROS, "número_4")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_ESTICADO,
        Dedo.MINIMO_ESTICADO,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_90)
)

Numero5 = (
    SinalLibras(Categoria.NUMEROS, "número_5")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_FLEXIONADO,
        Dedo.MEDIO_FLEXIONADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.LATERAL)
)

Numero6 = (
    SinalLibras(Categoria.NUMEROS, "número_6")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.CIMA)
    .inclinacao_palma(Inclinacao.DENTRO_90)
)

Numero7 = (
    SinalLibras(Categoria.NUMEROS, "número_7")
    .mao(
        Dedo.POLEGAR_ENC_LATERAL,
        Dedo.INDICADOR_FRENTE_90,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

Numero8 = (
    SinalLibras(Categoria.NUMEROS, "número_8")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.FRENTE)
)

Numero9 = (
    SinalLibras(Categoria.NUMEROS, "número_9")
    .mao(
        Dedo.POLEGAR_ESTICADO,
        Dedo.INDICADOR_DENTRO_PALMA,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
    .inclinacao_palma(Inclinacao.DENTRO_270)
)

Numero0 = SinalLibras(Categoria.NUMEROS, "número_0").igual_a(LetraO)

# Variantes quantitativas
Numero1_2 = (
    SinalLibras(Categoria.NUMEROS, "número_1_2")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_DENTRO_PALMA,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
)

Numero2_2 = (
    SinalLibras(Categoria.NUMEROS, "número_2_2")
    .mao(
        Dedo.POLEGAR_DENTRO_PALMA,
        Dedo.INDICADOR_ESTICADO,
        Dedo.MEDIO_ESTICADO,
        Dedo.ANELAR_DENTRO_PALMA,
        Dedo.MINIMO_DENTRO_PALMA,
    )
    .orientacao_palma(Orientacao.TRAS)
)

Numero3_2 = (
    SinalLibras(Categoria.NUMEROS, "número_3_2")
    .igual_a(Numero3)
    .inclinacao_palma(Inclinacao.RETA)
)

Numero4_2 = (
    SinalLibras(Categoria.NUMEROS, "número_4_2")
    .igual_a(Numero4)
    .inclinacao_palma(Inclinacao.RETA)
)
