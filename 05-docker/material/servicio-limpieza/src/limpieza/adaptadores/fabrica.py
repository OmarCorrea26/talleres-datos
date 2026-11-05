"""Fábrica de adaptadores de archivo: elige el lector y el escritor según la extensión.

Es el patrón Factory. Quien necesita leer o escribir no decide qué clase usar;
le pasa la ruta a la fábrica y recibe un objeto que cumple el puerto. Agregar
un formato es agregar una pareja de clases y una línea en el registro.
"""

from pathlib import Path

from limpieza.adaptadores.archivos import EscritorCSV, LectorCSV
from limpieza.adaptadores.parquet import EscritorParquet, LectorParquet
from limpieza.dominio.puertos import EscritorDeEncuesta, LectorDeEncuesta

FORMATOS = {
    ".csv": (LectorCSV, EscritorCSV),
    ".parquet": (LectorParquet, EscritorParquet),
}


def _pareja(ruta: Path):
    extension = Path(ruta).suffix.lower()
    try:
        return FORMATOS[extension]
    except KeyError:
        raise ValueError(f"formato no soportado: {extension!r}; opciones: {sorted(FORMATOS)}") from None


def crear_lector(ruta: Path) -> LectorDeEncuesta:
    return _pareja(ruta)[0](ruta)


def crear_escritor(ruta: Path) -> EscritorDeEncuesta:
    return _pareja(ruta)[1](ruta)
