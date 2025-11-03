from collections import namedtuple
from collections.abc import Callable
from enum import Enum, auto
from typing import TypeAlias, overload

from facilibras.modelos.mao import (
    Componente,
    Dedo,
    Expressao,
    Inclinacao,
    Mao,
    Orientacao,
    Posicao,
)


class CombinacaoImpossivelError(ValueError):
    def __init__(self, orientacao: Orientacao, inclinacao: Inclinacao):
        msg = f"Nenhum sinal tem {orientacao.value} e {inclinacao.value}"
        super().__init__(msg)


class Regiao(Enum):
    ESQUERDA = auto()
    DIREITA = auto()
    CIMA = auto()
    BAIXO = auto()
    SUPERIOR_ESQUERDA = auto()
    SUPERIOR_DIREITA = auto()
    INFERIOR_ESQUERDA = auto()
    INFERIOR_DIREITA = auto()


Valido = namedtuple("Valido", [])
Invalido = namedtuple("Invalido", ["mensagem"])
Resultado: TypeAlias = Valido | Invalido


T_Ponto: TypeAlias = tuple[float, float, float]
T_Dedos: TypeAlias = dict[int, T_Ponto]
T_Corpo: TypeAlias = dict[int, T_Ponto]
T_Rosto: TypeAlias = dict[int, T_Ponto]

T_ValidaFormato: TypeAlias = Callable[[T_Dedos, Orientacao, Inclinacao, Mao], Resultado]
T_ValidaPosicao: TypeAlias = Callable[[T_Ponto, T_Ponto, T_Corpo, Mao], Resultado]
T_ValidaExpressao: TypeAlias = Callable[[T_Rosto], Resultado]
T_Validador: TypeAlias = T_ValidaFormato | T_ValidaPosicao | T_ValidaExpressao

_validadores: dict[Componente, T_Validador] = {}


@overload
def registrar_validador(
    chave: Dedo,
) -> Callable[[T_ValidaFormato], T_ValidaFormato]: ...


@overload
def registrar_validador(
    chave: Posicao,
) -> Callable[[T_ValidaPosicao], T_ValidaPosicao]: ...


@overload
def registrar_validador(
    chave: Expressao,
) -> Callable[[T_ValidaExpressao], T_ValidaExpressao]: ...


@overload
def get_validador(chave: Dedo) -> T_ValidaFormato: ...


@overload
def get_validador(chave: Posicao) -> T_ValidaPosicao: ...


@overload
def get_validador(chave: Expressao) -> T_ValidaExpressao: ...


def registrar_validador(chave: Componente) -> Callable:
    def decorador(func: T_Validador) -> T_Validador:
        _validadores[chave] = func
        return func

    return decorador


def get_validador(chave: Componente) -> T_Validador:
    func = _validadores.get(chave)
    if not func:
        exc = f"Validador para {chave.value} não registrado!"
        raise ValueError(exc)

    return func
