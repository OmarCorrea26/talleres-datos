"""Estrategias de imputación: cómo se calcula el valor que reemplaza un ingreso faltante.

Es el patrón Strategy. La regla de imputación (a quién se imputa, con qué
grupo) es una sola; lo que cambia es el cálculo del valor de reemplazo. Cada
cálculo es una clase pequeña con la misma forma, y la política elige cuál.
"""

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class EstrategiaDeImputacion(Protocol):
    descripcion: str

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        """Devuelve el valor con el que se imputa a los faltantes de un grupo."""


class MedianaDelGrupo:
    descripcion = "mediana del ingreso"

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        return ingresos_del_grupo.median()


class MediaDelGrupo:
    descripcion = "media del ingreso"

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        return ingresos_del_grupo.mean()


@dataclass(frozen=True)
class ValorFijo:
    valor: float

    @property
    def descripcion(self) -> str:
        return f"valor fijo de {self.valor:,.0f}"

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        return self.valor


ESTRATEGIAS = {
    "mediana": MedianaDelGrupo,
    "media": MediaDelGrupo,
}


def estrategia_de_imputacion(nombre: str, valor_fijo: float | None = None) -> EstrategiaDeImputacion:
    """Fábrica: convierte el nombre que viene de la configuración en una estrategia."""
    if nombre == "fijo":
        if valor_fijo is None:
            raise ValueError("la estrategia 'fijo' necesita valor_fijo")
        return ValorFijo(valor_fijo)
    try:
        return ESTRATEGIAS[nombre]()
    except KeyError:
        raise ValueError(f"estrategia de imputación desconocida: {nombre!r}; opciones: {sorted(ESTRATEGIAS)} o 'fijo'") from None
