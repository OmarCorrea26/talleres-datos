"""Caso de uso: limpiar una encuesta completa, de donde venga, hacia donde vaya."""

from limpieza.dominio import PoliticaDeLimpieza, ResumenLimpieza, limpiar
from limpieza.dominio.puertos import EscritorDeEncuesta, LectorDeEncuesta


class LimpiarEncuesta:
    """Lee con un lector, aplica las reglas y entrega con un escritor.

    No sabe qué son el lector ni el escritor: solo que cumplen los puertos.
    Por eso el mismo caso de uso sirve para archivos, para una prueba en
    memoria o para lo que aparezca después.
    """

    def __init__(self, lector: LectorDeEncuesta, escritor: EscritorDeEncuesta, politica: PoliticaDeLimpieza):
        self._lector = lector
        self._escritor = escritor
        self._politica = politica

    def ejecutar(self) -> ResumenLimpieza:
        encuesta = self._lector.leer()
        resultado = limpiar(encuesta, self._politica)
        self._escritor.escribir(resultado.encuesta, resultado.resumen)
        return resultado.resumen
