from copy import deepcopy
from enum import Enum, StrEnum
from typing import Self, Type, TypeVar

from facilibras.modelos.mao import (
    Configuracao,
    Dedo,
    Expressao,
    Inclinacao,
    Orientacao,
    Posicao,
)


class Tipo(Enum):
    ESTATICO = 1
    COM_TRANSICAO = 2


class Categoria(StrEnum):
    ALFABETO = "alfabeto"
    NUMEROS = "numeros"


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
    ):
        self.conf_atual = deepcopy(self.confs[idx])
        if exceto_posicao:
            self.conf_atual.posicao = exceto_posicao
        return self

    def igual_a(self, configuracao: Configuracao):
        self.conf_atual = deepcopy(configuracao)
        return self

    @property
    def possui_transicao(self):
        return len(self.confs) > 1

    @property
    def possui_expressao_facial(self):
        return any(conf.expressao != Expressao.QUALQUER for conf in self.confs)

    @property
    def tipo(self) -> Tipo:
        if len(self.confs) > 1:
            return Tipo.COM_TRANSICAO

        return Tipo.ESTATICO

    def __str__(self) -> str:
        s = "Configurações Necessárias p/ Reconhecer:"
        if self.confs:
            s += "\n"
        s += "\n".join([f"{i + 1}: {conf}" for i, conf in enumerate(self.confs)])
        if self.configurando:
            s += f"\n{len(self.confs) + 1}: {self.conf_atual}"

        return s


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
