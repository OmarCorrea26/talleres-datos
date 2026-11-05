# Solución de referencia. Ejercicio 4.7: una estrategia y un formato más.
#
# 1) Estrategia MediaRecortada, al final de src/limpieza/dominio/imputacion.py,
#    y registrada en ESTRATEGIAS con el nombre "media_recortada".

import pandas as pd


class MediaRecortada:
    descripcion = "media recortada al 5 % del ingreso"

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        validos = ingresos_del_grupo.dropna()
        if len(validos) < 3:
            return validos.mean()
        inferior, superior = validos.quantile(0.05), validos.quantile(0.95)
        return validos[(validos >= inferior) & (validos <= superior)].mean()


# ESTRATEGIAS["media_recortada"] = MediaRecortada


# 2) src/limpieza/adaptadores/excel.py: la misma pareja, para .xlsx (requiere openpyxl).

import json  # noqa: E402
from pathlib import Path  # noqa: E402

from limpieza.dominio import ResumenLimpieza  # noqa: E402


class LectorExcel:
    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def leer(self) -> pd.DataFrame:
        df = pd.read_excel(self._ruta)
        df["ocupado"] = df["ocupado"].astype("Int64")
        return df


class EscritorExcel:
    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        encuesta.to_excel(self._ruta, index=False, sheet_name="encuesta_limpia")
        ruta_resumen = self._ruta.with_name(self._ruta.stem + "_resumen.json")
        ruta_resumen.write_text(json.dumps(resumen.como_dict(), indent=2, ensure_ascii=False), encoding="utf-8")


# 3) En fabrica.py: una línea más en FORMATOS.
#
# from limpieza.adaptadores.excel import EscritorExcel, LectorExcel
# FORMATOS[".xlsx"] = (LectorExcel, EscritorExcel)
#
#    Ojo: test_la_fabrica_elige_por_extension usaba ".xlsx" como ejemplo de formato
#    no soportado. Cámbialo por otra extensión (".sav", por ejemplo). Que una
#    prueba vieja falle al extender la fábrica es normal: documentaba el límite anterior.
#
# 4) Pruebas sugeridas:


def test_media_recortada_ignora_los_extremos():
    grupo = pd.Series([1.0] * 10 + [1_000_000.0] * 10 + [1e12])
    simple = grupo.mean()
    recortada = MediaRecortada().calcular(grupo)
    assert recortada < simple
    assert recortada < 1e6


def test_la_cli_escribe_excel(tmp_path, encuesta_minima):
    from limpieza.adaptadores.cli import main

    entrada = tmp_path / "entrada.csv"
    encuesta_minima.to_csv(entrada, index=False)
    assert main([str(entrada), str(tmp_path / "salida.xlsx")]) == 0
    assert len(pd.read_excel(tmp_path / "salida.xlsx")) == 4
