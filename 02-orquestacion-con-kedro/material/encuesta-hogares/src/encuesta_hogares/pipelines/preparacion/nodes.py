"""Nodos del pipeline de preparación.

Cada función recibe DataFrames o parámetros y devuelve DataFrames o
diccionarios. Ninguna lee ni escribe archivos: de eso se encarga el catálogo.
"""

import pandas as pd

COLUMNAS = [
    "id_persona",
    "id_hogar",
    "departamento",
    "area",
    "sexo",
    "edad",
    "ocupado",
    "ingreso",
    "factor_expansion",
]


def validar(encuesta: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Verifica columnas, fija los tipos y cuenta nulos.

    Devuelve la encuesta tipada y un resumen con lo encontrado.
    """
    faltan = [c for c in COLUMNAS if c not in encuesta.columns]
    if faltan:
        raise ValueError(f"Faltan columnas obligatorias: {faltan}")

    df = encuesta[COLUMNAS].copy()
    df["id_persona"] = df["id_persona"].astype(int)
    df["id_hogar"] = df["id_hogar"].astype(int)
    df["edad"] = df["edad"].astype(int)
    df["ocupado"] = df["ocupado"].astype("Int64")
    df["ingreso"] = pd.to_numeric(df["ingreso"], errors="coerce")
    df["factor_expansion"] = df["factor_expansion"].astype(float)
    for columna in ["departamento", "area", "sexo"]:
        df[columna] = df[columna].astype(str).str.strip()

    resumen = {
        "n_filas": int(len(df)),
        "columnas": COLUMNAS,
        "n_nulos_por_columna": {c: int(df[c].isna().sum()) for c in COLUMNAS},
    }
    return df, resumen


def limpiar(encuesta: pd.DataFrame, parametros: dict) -> tuple[pd.DataFrame, dict]:
    """Elimina duplicados, recorta atípicos e imputa ingresos faltantes."""
    n_entrada = len(encuesta)
    df = encuesta.drop_duplicates(subset="id_persona").reset_index(drop=True)
    n_duplicados = n_entrada - len(df)

    percentil = df["ingreso"].quantile(parametros["percentil_atipicos"])
    atipicos = df["ingreso"] > percentil
    df.loc[atipicos, "ingreso"] = percentil

    grupos = parametros["grupos_imputacion"]
    df["ingreso_imputado"] = False
    faltantes = (df["ocupado"] == 1) & df["ingreso"].isna()
    mediana = df[df["ocupado"] == 1].groupby(grupos)["ingreso"].transform("median")
    df.loc[faltantes, "ingreso"] = mediana[faltantes]
    df.loc[faltantes, "ingreso_imputado"] = True

    resumen = {
        "n_entrada": int(n_entrada),
        "n_duplicados_eliminados": int(n_duplicados),
        "n_salida": int(len(df)),
        "n_atipicos_ajustados": int(atipicos.sum()),
        "n_imputados": int(faltantes.sum()),
        "metodo": (
            f"atípicos recortados al percentil {parametros['percentil_atipicos']:.0%}; "
            f"imputación por mediana de ocupados según {' x '.join(grupos)}"
        ),
    }
    return df, resumen


def calibrar(encuesta: pd.DataFrame, poblacion_objetivo: dict) -> tuple[pd.DataFrame, dict]:
    """Ajusta los factores de expansión a los totales conocidos por departamento."""
    df = encuesta.copy()
    suma_cruda = df.groupby("departamento")["factor_expansion"].sum()
    razon = {d: poblacion_objetivo[d] / suma_cruda[d] for d in poblacion_objetivo}
    df["factor_calibrado"] = df["factor_expansion"] * df["departamento"].map(razon)

    totales = df.groupby("departamento")["factor_calibrado"].sum().round(2)
    resumen = {
        "razon_de_ajuste": {d: round(float(r), 4) for d, r in razon.items()},
        "totales_calibrados": {d: float(t) for d, t in totales.items()},
        "poblacion_objetivo": {d: float(p) for d, p in poblacion_objetivo.items()},
    }
    return df, resumen
