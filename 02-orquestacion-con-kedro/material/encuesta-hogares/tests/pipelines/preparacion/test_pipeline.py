"""Prueba del pipeline de preparación completo, de nodo en nodo, sin tocar disco.

Se arma un catálogo en memoria con la entrada y los parámetros, y se corre el
pipeline con SequentialRunner. Lo que se verifica es la salida final.
"""

import pandas as pd
from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner

from encuesta_hogares.pipelines.preparacion import create_pipeline


def test_pipeline_preparacion_deja_una_base_calibrada():
    encuesta = pd.DataFrame(
        {
            "id_persona": [1, 2, 3, 4],
            "id_hogar": [1, 1, 2, 2],
            "departamento": ["Bogota", "Bogota", "Valle", "Valle"],
            "area": ["Urbana", "Urbana", "Rural", "Rural"],
            "sexo": ["H", "M", "H", "M"],
            "edad": [30, 40, 25, 50],
            "ocupado": [1, 0, 1, 1],
            "ingreso": [1_000_000, None, 2_000_000, 1_500_000],
            "factor_expansion": [100.0, 100.0, 50.0, 50.0],
        }
    )
    catalogo = DataCatalog(
        {
            "encuesta_cruda": MemoryDataset(encuesta),
            "params:limpieza": MemoryDataset({"percentil_atipicos": 0.99, "grupos_imputacion": ["area", "sexo"]}),
            "params:poblacion_objetivo": MemoryDataset({"Bogota": 2000, "Valle": 300}),
        }
    )

    # El runner devuelve las salidas libres del pipeline como datasets en memoria
    salida = SequentialRunner().run(create_pipeline(), catalogo)

    calibrada = salida["encuesta_calibrada"].load()
    assert "factor_calibrado" in calibrada.columns
    assert calibrada.groupby("departamento")["factor_calibrado"].sum().round(6).to_dict() == {
        "Bogota": 2000.0,
        "Valle": 300.0,
    }
    assert salida["resumen_limpieza"].load()["n_duplicados_eliminados"] == 0
