"""Pruebas del dominio: sin archivos, sin HTTP, sin Kedro. Solo DataFrames y reglas."""

import pandas as pd
import pytest

from limpieza.dominio import PoliticaDeLimpieza, limpiar
from limpieza.dominio.reglas import eliminar_duplicados, imputar_ingresos, recortar_atipicos


def test_eliminar_duplicados_conserva_la_primera_aparicion(encuesta_minima):
    sin_duplicados, eliminados = eliminar_duplicados(encuesta_minima)
    assert eliminados == 1
    assert sin_duplicados["id_persona"].tolist() == [1, 2, 3, 4]


def test_recortar_atipicos_baja_el_ingreso_al_tope():
    encuesta = pd.DataFrame({"ingreso": [1_000_000.0, 2_000_000.0, 3_000_000.0, 100_000_000.0, None]})
    tope = encuesta["ingreso"].quantile(0.75)

    recortada, ajustados = recortar_atipicos(encuesta, percentil=0.75)

    assert ajustados == 1
    assert recortada["ingreso"].max() == tope
    assert recortada["ingreso"].isna().sum() == 1, "los vacíos no se tocan"


def test_imputar_ingresos_usa_la_mediana_del_grupo(encuesta_minima):
    imputada, n = imputar_ingresos(encuesta_minima, grupos=("area", "sexo"))
    assert n == 1
    fila = imputada.loc[imputada["id_persona"] == 2].iloc[0]
    assert fila["ingreso_imputado"]
    # mediana de los hombres urbanos ocupados con ingreso: 1M, 50M, 50M -> 50M
    assert fila["ingreso"] == 50_000_000.0


def test_limpiar_compone_las_tres_reglas(encuesta_minima):
    resultado = limpiar(encuesta_minima, PoliticaDeLimpieza(percentil_atipicos=0.5))
    resumen = resultado.resumen
    assert (resumen.n_entrada, resumen.n_salida) == (5, 4)
    assert resumen.n_duplicados_eliminados == 1
    assert resumen.n_imputados == 1
    assert "percentil 50" in resumen.metodo_imputacion
    assert str(resultado.encuesta["ocupado"].dtype) == "Int64"


def test_la_politica_rechaza_valores_imposibles():
    with pytest.raises(ValueError):
        PoliticaDeLimpieza(percentil_atipicos=1.5)
    with pytest.raises(ValueError):
        PoliticaDeLimpieza(grupos_imputacion=())


def test_la_politica_se_construye_desde_un_diccionario():
    politica = PoliticaDeLimpieza.desde_dict({"percentil_atipicos": 0.95, "grupos_imputacion": ["area"]})
    assert politica.percentil_atipicos == 0.95
    assert politica.grupos_imputacion == ("area",)
