"""Los otros dos adaptadores: el nodo para Kedro y la línea de comandos."""

import json

import pandas as pd

from limpieza.adaptadores.cli import main
from limpieza.adaptadores.kedro import nodo_limpiar


def test_el_nodo_devuelve_lo_que_el_catalogo_espera(encuesta_minima):
    encuesta, resumen = nodo_limpiar(encuesta_minima, {"percentil_atipicos": 0.5, "grupos_imputacion": ["area", "sexo"]})
    assert isinstance(encuesta, pd.DataFrame)
    assert isinstance(resumen, dict)
    assert resumen["n_salida"] == 4


def test_la_cli_deja_el_csv_y_el_resumen(tmp_path, encuesta_minima):
    entrada = tmp_path / "entrada.csv"
    salida = tmp_path / "limpia" / "encuesta_limpia.csv"
    encuesta_minima.to_csv(entrada, index=False)

    codigo = main([str(entrada), str(salida), "--percentil", "0.5"])

    assert codigo == 0
    assert len(pd.read_csv(salida)) == 4
    resumen = json.loads((tmp_path / "limpia" / "encuesta_limpia_resumen.json").read_text(encoding="utf-8"))
    assert resumen["n_duplicados_eliminados"] == 1
