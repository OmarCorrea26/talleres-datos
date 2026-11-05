"""Adaptadores de archivos: leen y escriben en disco cumpliendo los puertos del dominio."""

import json
from pathlib import Path

import pandas as pd

from limpieza.dominio import ResumenLimpieza


class LectorCSV:
    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def leer(self) -> pd.DataFrame:
        df = pd.read_csv(self._ruta)
        df["ocupado"] = df["ocupado"].astype("Int64")
        return df


class EscritorCSV:
    """Escribe la encuesta limpia como CSV y el resumen como JSON al lado."""

    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        encuesta.to_csv(self._ruta, index=False)
        ruta_resumen = self._ruta.with_name(self._ruta.stem + "_resumen.json")
        ruta_resumen.write_text(json.dumps(resumen.como_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
