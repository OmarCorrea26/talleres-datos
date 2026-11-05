"""Pruebas del patrón Factory: la extensión decide el adaptador, y los dos formatos son equivalentes."""

import pandas as pd
import pytest

from limpieza.adaptadores.archivos import EscritorCSV, LectorCSV
from limpieza.adaptadores.cli import main
from limpieza.adaptadores.fabrica import crear_escritor, crear_lector
from limpieza.adaptadores.parquet import EscritorParquet, LectorParquet


def test_la_fabrica_elige_por_extension(tmp_path):
    assert isinstance(crear_lector(tmp_path / "a.csv"), LectorCSV)
    assert isinstance(crear_escritor(tmp_path / "a.CSV"), EscritorCSV)
    assert isinstance(crear_lector(tmp_path / "a.parquet"), LectorParquet)
    assert isinstance(crear_escritor(tmp_path / "a.parquet"), EscritorParquet)
    with pytest.raises(ValueError, match="no soportado"):
        crear_lector(tmp_path / "a.xlsx")


def test_csv_y_parquet_producen_la_misma_limpieza(tmp_path, encuesta_minima):
    entrada_csv = tmp_path / "entrada.csv"
    entrada_parquet = tmp_path / "entrada.parquet"
    encuesta_minima.to_csv(entrada_csv, index=False)
    encuesta_minima.to_parquet(entrada_parquet, index=False)

    main([str(entrada_csv), str(tmp_path / "salida_a.csv"), "--percentil", "0.5"])
    main([str(entrada_parquet), str(tmp_path / "salida_b.parquet"), "--percentil", "0.5"])

    desde_csv = pd.read_csv(tmp_path / "salida_a.csv")
    desde_parquet = pd.read_parquet(tmp_path / "salida_b.parquet")
    # NaN no es igual a NaN: por eso se compara con fillna y no con ==
    assert desde_csv["ingreso"].fillna(-1).tolist() == desde_parquet["ingreso"].fillna(-1).tolist()
    assert desde_csv["id_persona"].tolist() == desde_parquet["id_persona"].tolist()
