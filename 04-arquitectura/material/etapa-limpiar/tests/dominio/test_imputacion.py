"""Pruebas del patrón Strategy: la regla es una, el cálculo del reemplazo es intercambiable."""

import pandas as pd
import pytest

from limpieza.dominio import PoliticaDeLimpieza, limpiar
from limpieza.dominio.imputacion import MediaDelGrupo, MedianaDelGrupo, ValorFijo, estrategia_de_imputacion
from limpieza.dominio.reglas import imputar_ingresos


def test_cada_estrategia_calcula_su_valor():
    grupo = pd.Series([1_000_000.0, 2_000_000.0, 6_000_000.0])
    assert MedianaDelGrupo().calcular(grupo) == 2_000_000.0
    assert MediaDelGrupo().calcular(grupo) == 3_000_000.0
    assert ValorFijo(500_000.0).calcular(grupo) == 500_000.0


def test_imputar_acepta_cualquier_estrategia(encuesta_minima):
    con_media, _ = imputar_ingresos(encuesta_minima, ("area", "sexo"), MediaDelGrupo())
    con_fijo, _ = imputar_ingresos(encuesta_minima, ("area", "sexo"), ValorFijo(1.0))
    fila_media = con_media.loc[con_media["id_persona"] == 2, "ingreso"].iloc[0]
    fila_fijo = con_fijo.loc[con_fijo["id_persona"] == 2, "ingreso"].iloc[0]
    # hombres urbanos ocupados con ingreso: 1M, 50M, 50M -> media 33.67M, mediana 50M
    assert round(fila_media) == 33_666_667
    assert fila_fijo == 1.0


def test_la_fabrica_de_estrategias_entiende_la_configuracion():
    assert isinstance(estrategia_de_imputacion("media"), MediaDelGrupo)
    assert estrategia_de_imputacion("fijo", 7.0) == ValorFijo(7.0)
    with pytest.raises(ValueError, match="desconocida"):
        estrategia_de_imputacion("vecino")
    with pytest.raises(ValueError, match="valor_fijo"):
        estrategia_de_imputacion("fijo")


def test_la_politica_elige_la_estrategia_y_la_describe(encuesta_minima):
    politica = PoliticaDeLimpieza(metodo_imputacion="media")
    resultado = limpiar(encuesta_minima, politica)
    assert resultado.resumen.metodo_imputacion.startswith("media del ingreso de ocupados por area x sexo")
    with pytest.raises(ValueError):
        PoliticaDeLimpieza(metodo_imputacion="inventada")
