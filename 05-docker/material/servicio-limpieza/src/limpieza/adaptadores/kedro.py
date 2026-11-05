"""Adaptador Kedro: la misma limpieza como nodo del pipeline del Taller 2.

Un nodo de Kedro es una función con DataFrames y diccionarios de entrada y
salida. Esta función traduce el diccionario de parámetros del YAML a una
política del dominio y devuelve lo que el catálogo espera. Para usarla en el
proyecto encuesta_hogares basta con importarla en pipeline.py:

    from limpieza.adaptadores.kedro import nodo_limpiar
    node(func=nodo_limpiar, inputs=["encuesta_validada", "params:limpieza"],
         outputs=["encuesta_limpia", "resumen_limpieza"], name="limpiar")

No importa kedro: no hace falta, y así el adaptador se prueba sin instalarlo.
"""

import pandas as pd

from limpieza.dominio import PoliticaDeLimpieza, limpiar


def nodo_limpiar(encuesta: pd.DataFrame, parametros: dict) -> tuple[pd.DataFrame, dict]:
    politica = PoliticaDeLimpieza.desde_dict(parametros)
    resultado = limpiar(encuesta, politica)
    return resultado.encuesta, resultado.resumen.como_dict()
