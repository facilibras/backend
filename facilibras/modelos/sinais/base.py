from copy import deepcopy
from enum import Enum, StrEnum
from typing import Self, Type, TypeVar

from facilibras.modelos.mao import (
    Configuracao,
    Dedo,
    Expressao,
    Inclinacao,
    Mao,
    Orientacao,
    Posicao,
)


class Tipo(Enum):
    UMA_MAO = 1
    DUAS_MAOS = 2


class Categoria(StrEnum):
    ALFABETO = "alfabeto"
    NUMEROS = "números"
    ALIMENTOS = "alimentos"
    SAUDACOES = "saudações"
    OUTROS = "outros"


class SinalLibras:
    def __init__(self, categoria: Categoria | None, nome: str) -> None:
        self.nome = nome
        self.categoria = categoria
        self.confs: list[Configuracao] = []
        self.conf_atual = Configuracao()
        self.configurando = True

        _sinais[nome] = self

    def preparar_reconhecimento(self) -> Self:
        if self.configurando:
            self.confs.append(self.conf_atual)
            self.configurando = False

        return self

    def mao(self, *dedos: Dedo) -> Self:
        self.conf_atual.dedos = list(dedos)
        return self

    def orientacao_palma(self, orientacao: Orientacao) -> Self:
        self.conf_atual.orientacao = Orientacao(orientacao)
        return self

    def inclinacao_palma(self, inclinacao: Inclinacao):
        self.conf_atual.inclinacao = inclinacao
        return self

    def posicao_mao(self, posicao: Posicao, ponto_ref: int):
        self.conf_atual.posicao = posicao
        self.conf_atual.ponto_ref = ponto_ref
        return self

    def expressao_facial(self, expressao: Expressao):
        self.conf_atual.expressao = expressao
        return self

    def descricao(self, desc: str) -> Self:
        self.conf_atual.descricao = desc
        return self

    def depois(self) -> Self:
        self.configurando = True
        self.confs.append(self.conf_atual)
        self.conf_atual = Configuracao()
        return self

    def depois_de(self, configuracao: Configuracao) -> Self:
        self.conf_atual = deepcopy(configuracao)
        self.configurando = True
        self.confs.append(self.conf_atual)
        self.conf_atual = Configuracao()
        return self

    def configuracao_anterior(
        self, idx: int = -1, *, exceto_posicao: Posicao | None = None
    ) -> Self:
        self.conf_atual = deepcopy(self.confs[idx])
        if exceto_posicao:
            self.conf_atual.posicao = exceto_posicao
        return self

    def igual_a(self, sinal: Self, conf_idx: int = 0) -> Self:
        if sinal.configurando and conf_idx == 0:
            configuracao = sinal.conf_atual
        else:
            configuracao = sinal.confs[conf_idx]

        self.conf_atual = deepcopy(configuracao)
        return self

    def par_config(self, idx_config: int) -> tuple[Configuracao, Configuracao]:
        msg = "Apenas sinais de duas mãos devem chamar essa função"
        raise TypeError(msg)

    @property
    def possui_transicao(self) -> bool:
        return len(self.confs) > 1

    @property
    def possui_expressao_facial(self) -> bool:
        return any(conf.expressao != Expressao.QUALQUER for conf in self.confs)

    @property
    def possui_posicao(self) -> bool:
        return any(conf.posicao != Posicao.QUALQUER for conf in self.confs)

    @property
    def tipo(self) -> Tipo:
        return Tipo.UMA_MAO

    @property
    def simples(self) -> bool:
        return not (
            self.possui_expressao_facial or self.possui_transicao or self.possui_posicao
        )

    def __str__(self) -> str:
        s = "Configurações Necessárias p/ Reconhecer:"
        if self.confs:
            s += "\n"
        s += "\n".join([f"{i + 1}: {conf}" for i, conf in enumerate(self.confs)])
        if self.configurando:
            s += f"\n{len(self.confs) + 1}: {self.conf_atual}"

        return s


class SinalLibras2Maos(SinalLibras):
    def __init__(self, categoria: Categoria | None, nome: str) -> None:
        super().__init__(categoria, nome)
        self.configurando_mao: Mao | None = Mao.ESQUERDA

    def mao_direita(self, *dedos: Dedo) -> Self:
        if self.configurando_mao == Mao.ESQUERDA:
            self.depois()

        self.configurando_mao = Mao.DIREITA
        self.conf_atual.mao = Mao.DIREITA
        return super().mao(*dedos)

    def mao_esquerda(self, *dedos: Dedo) -> Self:
        if self.configurando_mao == Mao.ESQUERDA:
            self.depois()

        self.configurando_mao = Mao.ESQUERDA
        self.conf_atual.mao = Mao.ESQUERDA
        return super().mao(*dedos)

    def depois(self) -> Self:
        self.configurando_mao = None
        return super().depois()

    def par_config(self, idx_config: int) -> tuple[Configuracao, Configuracao]:
        idx = 2 * idx_config
        if idx + 1 < len(self.confs):
            return self.confs[idx], self.confs[idx + 1]
        msg = f"Index: {idx_config} fora do range de pares"
        raise ValueError(msg)

    @property
    def tipo(self) -> Tipo:
        return Tipo.DUAS_MAOS


_sinais: dict[str, SinalLibras] = {}


def get_sinal(sinal: str) -> SinalLibras:
    if not (s := _sinais.get(sinal)):
        exc = "Nenhum sinal com esse nome registrado."
        raise ValueError(exc)

    return s


def listar_sinais() -> None:
    print(", ".join(_sinais.keys()))


T = TypeVar("T", bound=Enum)


def get_componente(nome: str, tipo: Type[T]) -> T:
    return tipo[nome]


def construir_sinal(
    dedos: list[str],
    inclinacao: str = "RETA",
    orientacao: str = "FRENTE",
    posicao: str = "QUALQUER",
    expressao: str = "QUALQUER",
    ponto_ref: int = 0,
) -> SinalLibras:
    d = [get_componente(dedo, Dedo) for dedo in dedos] if dedos else []
    o = get_componente(orientacao, Orientacao)
    i = get_componente(inclinacao, Inclinacao)
    p = get_componente(posicao, Posicao)
    e = get_componente(expressao, Expressao)

    return (
        SinalLibras(None, "interativo")
        .mao(*d)
        .orientacao_palma(o)
        .inclinacao_palma(i)
        .posicao_mao(p, ponto_ref)
        .expressao_facial(e)
    )
