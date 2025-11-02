from collections import namedtuple
from collections.abc import Callable
from typing import TypeAlias, overload

from facilibras.modelos.mao import (
    Componente,
    Dedo,
    Inclinacao,
    Mao,
    Orientacao,
)

Valido = namedtuple("Valido", [])
Invalido = namedtuple("Invalido", ["mensagem"])

T_Ponto: TypeAlias = tuple[float, float, float]
T_Dedos: TypeAlias = dict[int, T_Ponto]
Resultado: TypeAlias = Valido | Invalido
T_ValidaDedos: TypeAlias = Callable[[T_Dedos, Mao], Resultado]
T_ValidaFormato: TypeAlias = Callable[[T_Dedos, Orientacao, Inclinacao], Resultado]
T_Validador: TypeAlias = T_ValidaDedos | T_ValidaFormato


_validadores: dict[Componente, T_Validador] = {}


@overload
def registrar_validador(
    chave: Inclinacao | Orientacao,
) -> Callable[[T_ValidaDedos], T_ValidaDedos]: ...


@overload
def registrar_validador(
    chave: Dedo,
) -> Callable[[T_ValidaFormato], T_ValidaFormato]: ...


@overload
def get_validador(chave: Inclinacao | Orientacao) -> T_ValidaDedos: ...


@overload
def get_validador(chave: Dedo) -> T_ValidaFormato: ...


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
