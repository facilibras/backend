from enum import Enum, StrEnum
from typing import Self, Type, TypeVar

from facilibras.modelos.mao import (
    ConfiguracaoMao,
    Dedo,
    Inclinacao,
    Movimento,
    Orientacao,
)


class Tipo(Enum):
    ESTATICO = 1
    COM_MOVIMENTO = 2
    COM_TRANSICAO = 3
    COMPLETO = 4


class Categoria(StrEnum):
    ALFABETO = "alfabeto"
    NUMEROS = "numeros"


class SinalLibras:
    def __init__(self, categoria: Categoria | None, nome: str) -> None:
        self.nome = nome
        self.categoria = categoria
        self.confs: list[ConfiguracaoMao] = []
        self.conf_atual = ConfiguracaoMao()
        self.configurando = True

        _sinais[nome] = self

    def preparar_reconhecimento(self) -> Self:
        if self.configurando:
            self.confs.append(self.conf_atual)
            self.configurando = False

        return self

    def depois_de(self, sinal: Self) -> Self:
        # TODO: Implementar
        return self

    def igual_a(self, sinal: Self) -> Self:
        # TODO: Implementar
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

    def movimento(self, *movimentos: Movimento) -> Self:
        self.conf_atual.movimentos = list(movimentos)
        return self

    def depois(self) -> Self:
        self.configurando = True
        self.confs.append(self.conf_atual)
        self.conf_atual = ConfiguracaoMao()
        return self

    @property
    def possui_transicao(self):
        return len(self.confs) > 1

    @property
    def tipo(self) -> Tipo:
        if len(self.confs) > 1:
            return Tipo.COM_TRANSICAO

        for conf in self.confs:
            if conf.movimentos:
                return Tipo.COM_MOVIMENTO

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
    dedos: list[str], inclinacao: str = "RETA", orientacao: str = "FRENTE"
) -> SinalLibras:
    o = get_componente(orientacao, Orientacao)
    i = get_componente(inclinacao, Inclinacao)
    d = [get_componente(dedo, Dedo) for dedo in dedos] if dedos else []

    return (
        SinalLibras(None, "interativo").mao(*d).orientacao_palma(o).inclinacao_palma(i)
    )
