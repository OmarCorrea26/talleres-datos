# Solución de referencia. Ejercicio 5.4: la etapa 1 (validar) con la misma estructura.
#
# 1) src/limpieza/dominio/validacion.py
#    Solo importa pandas y dataclasses. Reproduce los conteos del fixture
#    etapa_1_salida.json del Taller 3.

from dataclasses import asdict, dataclass

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


@dataclass(frozen=True)
class ResumenValidacion:
    n_filas: int
    columnas: list[str]
    n_nulos_por_columna: dict[str, int]

    def como_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ResultadoValidacion:
    encuesta: pd.DataFrame
    resumen: ResumenValidacion


def validar(encuesta: pd.DataFrame) -> ResultadoValidacion:
    """Verifica columnas obligatorias, fija los tipos y cuenta nulos."""
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

    resumen = ResumenValidacion(
        n_filas=int(len(df)),
        columnas=list(COLUMNAS),
        n_nulos_por_columna={c: int(df[c].isna().sum()) for c in COLUMNAS},
    )
    return ResultadoValidacion(encuesta=df, resumen=resumen)


# 2) En src/limpieza/adaptadores/kedro.py, al lado de nodo_limpiar:
#
# from limpieza.dominio.validacion import validar
#
# def nodo_validar(encuesta: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
#     resultado = validar(encuesta)
#     return resultado.encuesta, resultado.resumen.como_dict()
#
# 3) ADR 0004 (cinco líneas bastan): validar y limpiar comparten paquete porque
#    comparten el modelo de datos y las pruebas, pero son etapas distintas del
#    muñeco y cada una tiene su propio servicio. Un servicio por etapa es el
#    contrato del Taller 3; el paquete es una decisión de este equipo.
#
# 4) Pruebas sugeridas, en tests/dominio/test_validacion.py:

import pytest  # noqa: E402


def test_validar_falla_si_falta_una_columna(encuesta_minima):
    with pytest.raises(ValueError, match="ingreso"):
        validar(encuesta_minima.drop(columns=["ingreso"]))


def test_validar_cuenta_nulos(encuesta_minima):
    resultado = validar(encuesta_minima)
    assert resultado.resumen.n_filas == 5
    assert resultado.resumen.n_nulos_por_columna["ingreso"] == 2
    assert str(resultado.encuesta["ocupado"].dtype) == "Int64"


def test_validar_descarta_columnas_de_mas(encuesta_minima):
    con_extra = encuesta_minima.assign(comentario="x")
    assert "comentario" not in validar(con_extra).encuesta.columns
