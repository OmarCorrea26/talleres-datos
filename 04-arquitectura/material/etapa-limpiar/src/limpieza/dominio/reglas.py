"""Las reglas de limpieza de la encuesta.

Tres reglas pequeñas y una función que las compone. Todas reciben un DataFrame
y devuelven otro, junto con el número que describe lo que hicieron. Ninguna
abre archivos, ninguna sabe de HTTP ni de Kedro, ninguna lee configuración.
"""

from dataclasses import asdict, dataclass

import pandas as pd

from .imputacion import EstrategiaDeImputacion, MedianaDelGrupo
from .politica import PoliticaDeLimpieza


@dataclass(frozen=True)
class ResumenLimpieza:
    n_entrada: int
    n_duplicados_eliminados: int
    n_salida: int
    n_imputados: int
    n_atipicos_ajustados: int
    metodo_imputacion: str

    def como_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ResultadoLimpieza:
    encuesta: pd.DataFrame
    resumen: ResumenLimpieza


def eliminar_duplicados(encuesta: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Conserva la primera aparición de cada id_persona."""
    sin_duplicados = encuesta.drop_duplicates(subset="id_persona").reset_index(drop=True)
    return sin_duplicados, len(encuesta) - len(sin_duplicados)


def recortar_atipicos(encuesta: pd.DataFrame, percentil: float) -> tuple[pd.DataFrame, int]:
    """Todo ingreso por encima del percentil se recorta a ese valor (winsorización)."""
    df = encuesta.copy()
    tope = df["ingreso"].quantile(percentil)
    atipicos = df["ingreso"] > tope
    df.loc[atipicos, "ingreso"] = tope
    return df, int(atipicos.sum())


def imputar_ingresos(
    encuesta: pd.DataFrame,
    grupos: tuple[str, ...],
    estrategia: EstrategiaDeImputacion = MedianaDelGrupo(),
) -> tuple[pd.DataFrame, int]:
    """Los ocupados sin ingreso reciben el valor que calcula la estrategia para su grupo."""
    df = encuesta.copy()
    ocupados = df["ocupado"] == 1
    faltantes = ocupados & df["ingreso"].isna()
    reemplazo = df[ocupados].groupby(list(grupos))["ingreso"].transform(estrategia.calcular)
    df["ingreso_imputado"] = False
    df.loc[faltantes, "ingreso"] = reemplazo[faltantes]
    df.loc[faltantes, "ingreso_imputado"] = True
    return df, int(faltantes.sum())


def limpiar(encuesta: pd.DataFrame, politica: PoliticaDeLimpieza) -> ResultadoLimpieza:
    """Aplica las tres reglas en orden y devuelve la base limpia con su resumen."""
    n_entrada = len(encuesta)
    df, n_duplicados = eliminar_duplicados(encuesta)
    df, n_atipicos = recortar_atipicos(df, politica.percentil_atipicos)
    df, n_imputados = imputar_ingresos(df, politica.grupos_imputacion, politica.estrategia)
    df["ocupado"] = df["ocupado"].astype("Int64")

    resumen = ResumenLimpieza(
        n_entrada=int(n_entrada),
        n_duplicados_eliminados=int(n_duplicados),
        n_salida=int(len(df)),
        n_imputados=n_imputados,
        n_atipicos_ajustados=n_atipicos,
        metodo_imputacion=politica.descripcion,
    )
    return ResultadoLimpieza(encuesta=df, resumen=resumen)
