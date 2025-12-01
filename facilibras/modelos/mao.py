from dataclasses import dataclass, field
from enum import Enum, auto
from typing import override


class Componente(Enum):
    """
    Classe base para criação de enums com identificadores únicos globais.
    """

    @override
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


class Dedo(Componente):
    """
    Representa uma posição ou flexão específica de um dedo.
    """

    # Polegar
    POLEGAR_CURVADO = auto()
    POLEGAR_DENTRO_PALMA = auto()
    POLEGAR_ENC_LATERAL = auto()
    POLEGAR_ESTICADO = auto()
    POLEGAR_FLEXIONADO = auto()
    # Indicador
    INDICADOR_CURVADO = auto()
    INDICADOR_DENTRO_PALMA = auto()
    INDICADOR_DIST_MEDIO = auto()
    INDICADOR_ESTICADO = auto()
    INDICADOR_FLEXIONADO = auto()
    INDICADOR_FRENTE_90 = auto()
    INDICADOR_FRENTE_45 = auto()
    INDICADOR_ENC_MEDIO = auto()
    INDICADOR_ENC_POLEGAR = auto()
    INDICADOR_MEDIO_CRUZADO = auto()
    # Médio
    MEDIO_CURVADO = auto()
    MEDIO_DENTRO_PALMA = auto()
    MEDIO_DIST_ANELAR = auto()
    MEDIO_ENC_POLEGAR = auto()
    MEDIO_ESTICADO = auto()
    MEDIO_FLEXIONADO = auto()
    MEDIO_FRENTE_45 = auto()
    # Anelar
    ANELAR_CURVADO = auto()
    ANELAR_DENTRO_PALMA = auto()
    ANELAR_ENC_POLEGAR = auto()
    ANELAR_ESTICADO = auto()
    ANELAR_FLEXIONADO = auto()
    # Mínimo
    MINIMO_CURVADO = auto()
    MINIMO_DENTRO_PALMA = auto()
    MINIMO_ESTICADO = auto()
    MINIMO_FLEXIONADO = auto()


class Mao(Componente):
    """
    Representa e identifica uma das mãos.
    """

    ESQUERDA = auto()
    DIREITA = auto()


class Orientacao(Componente):
    """
    Representa as diferentes orientações da palma da mão.
    """

    FRENTE = auto()
    LATERAL = auto()
    TRAS = auto()
    CIMA = auto()
    BAIXO = auto()


class Inclinacao(Componente):
    """
    Representa os diferentes graus de inclinação da palma da mão.
    """

    DENTRO_45 = auto()
    DENTRO_90 = auto()
    DENTRO_180 = auto()
    DENTRO_270 = auto()
    FORA_90 = auto()
    RETA = auto()


class Posicao(Componente):
    """
    Representa a posição da mão em relação ao uma parte do corpo
    """

    BOCA = auto()
    CENTRO = auto()
    DISTANTE_AO_CORPO = auto()
    LADO_ESQUERDO_BAIXO = auto()
    LADO_ESQUERDO_CIMA = auto()
    LADO_DIREITA_BAIXO = auto()
    LADO_DIREITA_CIMA = auto()
    LADO_OPOSTO = auto()  # mão alinhada com o ombro oposto
    MESMO_LADO = auto()  # mão alinhada com o ombro do mesmo lado
    OMBRO_PRA_CIMA = auto()
    ORELHA = auto()
    PEITO = auto()
    PROXIMO_AO_CORPO = auto()
    QUALQUER = auto()
    QUEIXO = auto()
    SOMBRANCELHA = auto()
    TESTA = auto()


class Expressao(Componente):
    BOCA_ABERTA = auto()
    BOCA_FECHADA = auto()
    QUALQUER = auto()


@dataclass
class Configuracao:
    dedos: list[Dedo] = field(default_factory=list)
    orientacao: Orientacao = Orientacao.FRENTE
    inclinacao: Inclinacao = Inclinacao.RETA
    posicao: Posicao = Posicao.QUALQUER
    expressao: Expressao = Expressao.QUALQUER
    descricao: str = "Configuração do sinal"
    ponto_ref: int = 0
    mao: Mao | None = None

    @property
    def possui_expressao_facial(self) -> bool:
        return self.expressao != Expressao.QUALQUER

    @property
    def possui_posicao(self) -> bool:
        return self.posicao != Posicao.QUALQUER

    def __repr__(self) -> str:
        todos = []
        if self.dedos:
            todos.extend(self.dedos)
        if self.orientacao:
            todos.append(self.orientacao)
        if self.inclinacao:
            todos.append(self.inclinacao)
        if self.posicao:
            todos.append(f"{self.posicao} ({self.ponto_ref})")
        if self.expressao:
            todos.append(self.expressao)
        if self.mao:
            todos.append(self.mao)

        return " - ".join(map(str, todos))
