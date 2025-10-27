from dataclasses import dataclass, field
from enum import Enum, auto
from typing import override


class EnumUnico(Enum):
    """
    Classe base para criação de enums com identificadores únicos globais.
    """

    def __new__(cls, value):
        """
        Padroniza o nome como CLASSE_VALOR para a identificação única de cada unidade.
        Ex: `Dedo.POLEGAR_DENTRO` tem o valor de `DEDO_POLEGAR_DENTRO`
        """
        obj = object.__new__(cls)
        obj._value_ = f"{cls.__name__}_{value}".upper()
        return obj

    @override
    @staticmethod
    def _generate_next_value_(name, *args, **kwargs):
        """
        Utiliza o nome criado no `__new__` para garantir uma chave única.
        """
        return name


class Dedo(EnumUnico):
    """
    Representa uma posição ou flexão específica de um dedo.
    """

    # Polegar
    POLEGAR_DENTRO = auto()
    POLEGAR_FORA = auto()
    POLEGAR_CIMA = auto()
    POLEGAR_FLEXIONADO = auto()
    POLEGAR_CURVADO = auto()
    # Indicador
    INDICADOR_CIMA = auto()
    INDICADOR_BAIXO = auto()
    INDICADOR_FLEXIONADO = auto()
    INDICADOR_CURVADO = auto()
    INDICADOR_FRENTE_90 = auto()
    INDICADOR_FRENTE_45 = auto()
    # Médio
    MEDIO_CIMA = auto()
    MEDIO_BAIXO = auto()
    MEDIO_FLEXIONADO = auto()
    MEDIO_FRENTE_45 = auto()
    MEDIO_CURVADO = auto()
    # Anelar
    ANELAR_CIMA = auto()
    ANELAR_BAIXO = auto()
    ANELAR_FLEXIONADO = auto()
    ANELAR_CURVADO = auto()
    # Mínimo
    MINIMO_CIMA = auto()
    MINIMO_BAIXO = auto()
    MINIMO_FLEXIONADO = auto()
    MINIMO_CURVADO = auto()
    # Posições Especiais
    INDICADOR_MEDIO_CRUZADO = auto()
    INDICADOR_ENC_POLEGAR = auto()
    INDICADOR_ENC_MEDIO = auto()
    MEDIO_ENC_POLEGAR = auto()
    ANELAR_ENC_POLEGAR = auto()
    INDICADOR_DIST_MEDIO = auto()
    MEDIO_DIST_ANELAR = auto()


class Mao(EnumUnico):
    """
    Representa e identifica uma das mãos.
    """

    ESQUERDA = auto()
    DIREITA = auto()


class Orientacao(EnumUnico):
    """
    Representa as diferentes orientações da palma da mão.
    """

    FRENTE = auto()
    LATERAL = auto()
    TRAS = auto()
    CIMA = auto()
    BAIXO = auto()


class Inclinacao(EnumUnico):
    """
    Representa os diferentes graus de inclinação da palma da mão.
    """

    RETA = auto()
    DENTRO_45 = auto()
    DENTRO_90 = auto()
    DENTRO_180 = auto()


class Movimento(EnumUnico):
    """
    Representa os diferentes movimentos direcionais da mão.
    """

    ESQUERDA = auto()
    DIREITA = auto()
    CIMA = auto()
    BAIXO = auto()

    FRENTE = auto()
    TRAS = auto()

    CIMA_DIREITA = auto()
    CIMA_ESQUERDA = auto()
    BAIXO_DIREITA = auto()
    BAIXO_ESQUERDA = auto()


class Posicao(EnumUnico):
    """
    Representa a posição da mão em relação ao uma parte do corpo
    """

    QUALQUER = auto()
    MESMO_LADO = auto()  # mão alinhada com o ombro do mesmo lado
    LADO_OPPOSTO = auto()  # mão alinhada com o ombro oposto


@dataclass
class ConfiguracaoMao:
    dedos: list[Dedo] = field(default_factory=list)
    orientacao: Orientacao | None = None
    inclinacao: Inclinacao | None = None
    posicao: Posicao = Posicao.QUALQUER
    movimentos: list[Movimento] = field(default_factory=list)
    descricao: str | None = None

    def __repr__(self) -> str:
        todos = []
        if self.dedos:
            todos.extend(self.dedos)
        if self.orientacao:
            todos.append(self.orientacao)
        if self.inclinacao:
            todos.append(self.inclinacao)
        if self.movimentos:
            todos.append(self.movimentos)

        return " - ".join(map(str, todos))
