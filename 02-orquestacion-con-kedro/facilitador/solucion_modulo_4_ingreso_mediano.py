# Solución de referencia. Ejercicio 4.4: ingreso mediano ponderado por área.
#
# 1) Agregar al final de src/encuesta_hogares/pipelines/estimacion/nodes.py

import pandas as pd


def _mediana_ponderada(valores: pd.Series, pesos: pd.Series) -> float:
    """Valor en el que el peso acumulado alcanza la mitad del peso total."""
    ordenado = pd.DataFrame({"x": valores.astype(float), "w": pesos}).sort_values("x")
    acumulado = ordenado["w"].cumsum()
    corte = ordenado["w"].sum() / 2
    return float(ordenado.loc[acumulado >= corte, "x"].iloc[0])


def estimar_ingreso_mediano(encuesta: pd.DataFrame) -> pd.DataFrame:
    """Ingreso mediano de los ocupados por área, ponderado con el factor calibrado."""
    ocupados = encuesta[encuesta["ocupado"] == 1]
    filas = []
    for area, g in ocupados.groupby("area"):
        filas.append(
            {
                "indicador": "ingreso_mediano",
                "area": area,
                "valor": _mediana_ponderada(g["ingreso"], g["factor_calibrado"]),
                "n_muestra": int(len(g)),
                "poblacion_estimada": float(g["factor_calibrado"].sum()),
            }
        )
    return pd.DataFrame(filas)


# 2) Nodo en pipeline.py del pipeline de estimación (y en la importación):
#
#             node(
#                 func=estimar_ingreso_mediano,
#                 inputs="encuesta_calibrada",
#                 outputs="ingreso_mediano",
#                 name="estimar_ingreso_mediano",
#             ),
#
# 3) Entrada en el catálogo:
#
# ingreso_mediano:
#   type: pandas.CSVDataset
#   filepath: data/07_model_output/ingreso_mediano.csv
#   save_args:
#     index: false
#
# 4) Prueba sugerida, en tests/pipelines/estimacion/test_nodes.py:

from encuesta_hogares.pipelines.estimacion.nodes import _mediana_ponderada as mediana_ponderada  # noqa: E402


def test_mediana_ponderada_respeta_los_pesos():
    valores = pd.Series([100, 200, 300])
    pesos = pd.Series([1, 1, 10])
    assert mediana_ponderada(valores, pesos) == 300
