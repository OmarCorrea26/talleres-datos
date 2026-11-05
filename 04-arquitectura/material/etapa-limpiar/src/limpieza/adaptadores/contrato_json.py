"""Traducción entre el contrato JSON del Taller 3 y los DataFrames del dominio.

El contrato dice: entra {"registros": [...]} y sale {"registros": [...], "resumen": {...}}.
Esa forma es cosa del transporte, no de las reglas de limpieza, y por eso la
traducción vive en un adaptador y no en el dominio.
"""

import pandas as pd

from limpieza.dominio import ResultadoLimpieza


def registros_a_dataframe(registros: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(registros)
    df["ocupado"] = df["ocupado"].astype("Int64")
    df["ingreso"] = pd.to_numeric(df["ingreso"], errors="coerce")
    return df


def dataframe_a_registros(df: pd.DataFrame) -> list[dict]:
    # JSON no tiene NaN: los vacíos deben salir como null
    return df.astype(object).where(df.notna(), None).to_dict(orient="records")


def resultado_a_salida(resultado: ResultadoLimpieza) -> dict:
    return {
        "registros": dataframe_a_registros(resultado.encuesta),
        "resumen": resultado.resumen.como_dict(),
    }
