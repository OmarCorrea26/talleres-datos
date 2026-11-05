"""Puertos: lo que el dominio necesita del mundo exterior, dicho en su propio idioma.

Un puerto es una interfaz. El dominio dice "necesito algo que me entregue la
encuesta" y "necesito algo que reciba el resultado", sin decir si eso es un
CSV, una tabla de SQL o una petición HTTP. Quien cumpla la interfaz sirve.

Se usan Protocol en vez de clases base para no obligar a heredar: cualquier
objeto con los métodos correctos encaja, incluso uno escrito para una prueba.
"""

from typing import Protocol

import pandas as pd

from .reglas import ResumenLimpieza


class LectorDeEncuesta(Protocol):
    def leer(self) -> pd.DataFrame:
        """Devuelve la encuesta validada, una fila por persona."""


class EscritorDeEncuesta(Protocol):
    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        """Recibe la encuesta limpia y su resumen, y hace con ellos lo que corresponda."""
