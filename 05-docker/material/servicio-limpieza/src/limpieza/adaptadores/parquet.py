"""Adaptadores Parquet: la misma pareja lector y escritor, para otro formato.

Requiere pyarrow. Compara con archivos.py: cambia cómo se lee y se escribe,
no cambia nada de lo que el dominio recibe o devuelve.
"""

import json
from pathlib import Path

import pandas as pd

from limpieza.dominio import ResumenLimpieza


class LectorParquet:
    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def leer(self) -> pd.DataFrame:
        return pd.read_parquet(self._ruta)


class EscritorParquet:
    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        encuesta.to_parquet(self._ruta, index=False)
        ruta_resumen = self._ruta.with_name(self._ruta.stem + "_resumen.json")
        ruta_resumen.write_text(json.dumps(resumen.como_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
