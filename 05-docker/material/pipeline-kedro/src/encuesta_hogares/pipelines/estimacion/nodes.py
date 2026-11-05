"""Nodos del pipeline de estimación."""

import math
from datetime import date

import pandas as pd

DOMINIOS = ["departamento", "sexo", "area"]
CUANTIL_NORMAL = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}


def _estimar_por_grupo(df: pd.DataFrame, variable: str, grupos: list[str], nombre: str) -> pd.DataFrame:
    filas = []
    for claves, g in df.groupby(grupos):
        if not isinstance(claves, tuple):
            claves = (claves,)
        pesos = g["factor_calibrado"]
        fila = {"indicador": nombre}
        fila.update(dict(zip(grupos, (str(c) for c in claves))))
        fila.update(
            {
                "valor": float((g[variable] * pesos).sum() / pesos.sum()),
                "n_muestra": int(len(g)),
                "poblacion_estimada": float(pesos.sum()),
            }
        )
        filas.append(fila)
    return pd.DataFrame(filas)


def estimar_indicadores(encuesta: pd.DataFrame, parametros: dict) -> pd.DataFrame:
    """Tasa de ocupación por departamento y sexo, e ingreso promedio por área.

    Ambos ponderados con el factor calibrado. Devuelve una tabla plana con una
    columna por dominio; las que no aplican quedan vacías.
    """
    edad_minima = parametros["edad_minima_ocupacion"]

    en_edad = encuesta[encuesta["edad"] >= edad_minima].copy()
    en_edad["ocupado"] = en_edad["ocupado"].astype(float)
    tasas = _estimar_por_grupo(en_edad, "ocupado", ["departamento", "sexo"], "tasa_ocupacion")

    ocupados = encuesta[encuesta["ocupado"] == 1].copy()
    ingresos = _estimar_por_grupo(ocupados, "ingreso", ["area"], "ingreso_promedio")

    columnas = ["indicador", *DOMINIOS, "valor", "n_muestra", "poblacion_estimada"]
    return pd.concat([tasas, ingresos], ignore_index=True).reindex(columns=columnas)


def _error_estandar(g: pd.DataFrame, variable: str) -> float:
    pesos = g["factor_calibrado"]
    x = g[variable].astype(float)
    media = (x * pesos).sum() / pesos.sum()
    varianza = (pesos * (x - media) ** 2).sum() / pesos.sum()
    n_efectivo = pesos.sum() ** 2 / (pesos**2).sum()
    return math.sqrt(varianza / n_efectivo)


def calcular_precision(encuesta: pd.DataFrame, indicadores: pd.DataFrame, parametros: dict) -> pd.DataFrame:
    """Error estándar, coeficiente de variación e intervalo de confianza por fila."""
    z = CUANTIL_NORMAL[parametros["nivel_confianza"]]
    edad_minima = parametros["edad_minima_ocupacion"]
    resultado = indicadores.copy()

    errores = []
    for _, fila in indicadores.iterrows():
        if fila["indicador"] == "tasa_ocupacion":
            base, variable = encuesta[encuesta["edad"] >= edad_minima], "ocupado"
        else:
            base, variable = encuesta[encuesta["ocupado"] == 1], "ingreso"
        mascara = pd.Series(True, index=base.index)
        for dominio in DOMINIOS:
            if pd.notna(fila[dominio]):
                mascara &= base[dominio].astype(str) == fila[dominio]
        errores.append(_error_estandar(base[mascara], variable))

    resultado["error_estandar"] = errores
    resultado["cv"] = 100 * resultado["error_estandar"] / resultado["valor"]
    resultado["limite_inferior"] = resultado["valor"] - z * resultado["error_estandar"]
    resultado["limite_superior"] = resultado["valor"] + z * resultado["error_estandar"]
    return resultado


def clasificar_calidad(indicadores: pd.DataFrame, umbrales: dict) -> pd.DataFrame:
    """Etiqueta cada estimación como buena, aceptable o poco confiable según su CV."""

    def etiqueta(cv: float) -> str:
        if cv <= umbrales["buena"]:
            return "buena"
        if cv <= umbrales["aceptable"]:
            return "aceptable"
        return "poco confiable"

    tabulados = indicadores.copy()
    tabulados["calidad"] = tabulados["cv"].apply(etiqueta)
    return tabulados


def generar_metadatos(tabulados: pd.DataFrame, umbrales: dict, parametros: dict) -> dict:
    """Ficha que acompaña a los tabulados publicados."""
    return {
        "titulo": "Tabulados de ocupación e ingreso. Encuesta sintética de hogares",
        "fuente": "Taller 2. Datos ficticios generados con generar_encuesta.py",
        "fecha_proceso": date.today().isoformat(),
        "n_indicadores": int(len(tabulados)),
        "nivel_confianza": parametros["nivel_confianza"],
        "nota_metodologica": (
            "Estimaciones ponderadas con factores calibrados por departamento. "
            f"Calidad según coeficiente de variación: buena (<= {umbrales['buena']} %), "
            f"aceptable (hasta {umbrales['aceptable']} %), poco confiable (mayor)."
        ),
    }


def filtrar_area(encuesta: pd.DataFrame, area: str) -> pd.DataFrame:
    """Se queda con las personas de un área (Urbana o Rural)."""
    return encuesta[encuesta["area"] == area].reset_index(drop=True)
