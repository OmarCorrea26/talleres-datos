"""Prueba del caso de uso con puertos falsos en memoria.

Aquí se ve para qué sirven los puertos: el caso de uso se prueba completo sin
tocar el disco, porque el lector y el escritor son dos clases de diez líneas
escritas para la prueba.
"""

import pandas as pd

from limpieza.aplicacion import LimpiarEncuesta
from limpieza.dominio import PoliticaDeLimpieza, ResumenLimpieza


class LectorEnMemoria:
    def __init__(self, encuesta: pd.DataFrame):
        self._encuesta = encuesta

    def leer(self) -> pd.DataFrame:
        return self._encuesta


class EscritorEnMemoria:
    def __init__(self):
        self.encuesta = None
        self.resumen = None

    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        self.encuesta = encuesta
        self.resumen = resumen


def test_el_caso_de_uso_lee_limpia_y_escribe(encuesta_minima):
    escritor = EscritorEnMemoria()
    caso_de_uso = LimpiarEncuesta(LectorEnMemoria(encuesta_minima), escritor, PoliticaDeLimpieza())

    resumen = caso_de_uso.ejecutar()

    assert resumen is escritor.resumen
    assert len(escritor.encuesta) == 4
    assert resumen.n_duplicados_eliminados == 1
