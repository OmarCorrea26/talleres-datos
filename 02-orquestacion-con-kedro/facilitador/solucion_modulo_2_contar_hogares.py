# Solución de referencia. Ejercicio 2.12: un nodo más en la preparación.
#
# 1) Agregar esta función al final de src/encuesta_hogares/pipelines/preparacion/nodes.py

import pandas as pd


def contar_hogares(encuesta: pd.DataFrame) -> dict:
    """Número de hogares distintos por departamento, sobre la base limpia."""
    conteo = encuesta.groupby("departamento")["id_hogar"].nunique()
    return {departamento: int(n) for departamento, n in conteo.items()}


# 2) Agregar este nodo a la lista de pipeline.py del mismo pipeline (y a la
#    importación: from .nodes import calibrar, contar_hogares, limpiar, validar)
#
#             node(
#                 func=contar_hogares,
#                 inputs="encuesta_limpia",
#                 outputs="resumen_hogares",
#                 name="contar_hogares",
#             ),
#
# 3) No hay que tocar el catálogo: el patrón "resumen_{etapa}" captura la salida
#    y la escribe en data/02_intermediate/resumen_hogares.json.
#
# 4) kedro run --pipeline preparacion  -> cuatro tareas; el JSON tiene cinco llaves.
