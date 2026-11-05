"""El dominio: reglas de limpieza puras, sin frameworks ni archivos."""

from .politica import PoliticaDeLimpieza
from .reglas import ResultadoLimpieza, ResumenLimpieza, limpiar

__all__ = ["PoliticaDeLimpieza", "ResultadoLimpieza", "ResumenLimpieza", "limpiar"]
