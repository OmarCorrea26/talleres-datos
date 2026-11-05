"""Pruebas de los nodos de preparación.

Cada prueba arma un DataFrame pequeño a mano, llama al nodo como a cualquier
función de Python y verifica una sola cosa. No hace falta Kedro para esto.
"""

import pandas as pd
import pytest

from encuesta_hogares.pipelines.preparacion.nodes import calibrar, limpiar, validar


@pytest.fixture
def encuesta_minima() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id_persona": [1, 2, 3, 3, 4],
            "id_hogar": [1, 1, 2, 2, 3],
            "departamento": ["Bogota", "Bogota", "Valle", "Valle", "Valle"],
            "area": ["Urbana", "Urbana", "Rural", "Rural", "Rural"],
            "sexo": ["H", "M", "H", "H", "M"],
            "edad": [30, 40, 25, 25, 10],
            "ocupado": [1, 1, 1, 1, None],
            "ingreso": [1_000_000, None, 2_000_000, 2_000_000, None],
            "factor_expansion": [100.0, 100.0, 50.0, 50.0, 50.0],
        }
    )


def test_validar_falla_si_falta_una_columna(encuesta_minima):
    sin_columna = encuesta_minima.drop(columns=["ingreso"])
    with pytest.raises(ValueError, match="ingreso"):
        validar(sin_columna)


def test_validar_cuenta_nulos(encuesta_minima):
    _, resumen = validar(encuesta_minima)
    assert resumen["n_filas"] == 5
    assert resumen["n_nulos_por_columna"]["ingreso"] == 2
    assert resumen["n_nulos_por_columna"]["ocupado"] == 1


def test_limpiar_elimina_duplicados_e_imputa(encuesta_minima):
    validada, _ = validar(encuesta_minima)
    parametros = {"percentil_atipicos": 0.99, "grupos_imputacion": ["area", "sexo"]}
    limpia, resumen = limpiar(validada, parametros)

    assert resumen["n_duplicados_eliminados"] == 1
    assert len(limpia) == 4
    assert resumen["n_imputados"] == 1
    assert limpia["ingreso_imputado"].sum() == 1
    # El ocupado sin ingreso era mujer urbana: la mediana de su grupo es la suya misma,
    # y como no hay otra, la imputación queda vacía. Eso también se verifica.
    assert limpia.loc[limpia["id_persona"] == 2, "ingreso"].isna().all()


def test_calibrar_reproduce_la_poblacion_objetivo(encuesta_minima):
    validada, _ = validar(encuesta_minima)
    limpia, _ = limpiar(validada, {"percentil_atipicos": 0.99, "grupos_imputacion": ["area", "sexo"]})
    objetivo = {"Bogota": 1000, "Valle": 500}

    calibrada, resumen = calibrar(limpia, objetivo)

    totales = calibrada.groupby("departamento")["factor_calibrado"].sum()
    assert totales["Bogota"] == pytest.approx(1000)
    assert totales["Valle"] == pytest.approx(500)
    assert resumen["razon_de_ajuste"]["Bogota"] == pytest.approx(5.0)
