"""Adaptador de línea de comandos: limpiar un archivo y dejar otro al lado.

Ejecutar:  python -m limpieza.adaptadores.cli entrada.csv salida.csv --percentil 0.99
           python -m limpieza.adaptadores.cli entrada.csv salida.parquet --metodo media

El formato de entrada y de salida lo decide la extensión; la fábrica de
adaptadores se encarga del resto.
"""

import argparse
from pathlib import Path

from limpieza.adaptadores.fabrica import crear_escritor, crear_lector
from limpieza.aplicacion import LimpiarEncuesta
from limpieza.dominio import PoliticaDeLimpieza


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Limpia la encuesta de hogares: duplicados, atípicos e imputación.")
    parser.add_argument("entrada", type=Path, help="archivo con la encuesta validada (.csv o .parquet)")
    parser.add_argument("salida", type=Path, help="archivo donde dejar la encuesta limpia (.csv o .parquet)")
    parser.add_argument("--percentil", type=float, default=0.99, help="percentil para recortar atípicos")
    parser.add_argument("--grupos", nargs="+", default=["area", "sexo"], help="columnas que definen el grupo de imputación")
    parser.add_argument("--metodo", default="mediana", help="estrategia de imputación: mediana, media o fijo")
    parser.add_argument("--valor-fijo", type=float, default=None, help="valor a imputar cuando el método es fijo")
    return parser


def main(argumentos: list[str] | None = None) -> int:
    opciones = construir_parser().parse_args(argumentos)
    politica = PoliticaDeLimpieza(
        percentil_atipicos=opciones.percentil,
        grupos_imputacion=tuple(opciones.grupos),
        metodo_imputacion=opciones.metodo,
        valor_fijo=opciones.valor_fijo,
    )
    caso_de_uso = LimpiarEncuesta(crear_lector(opciones.entrada), crear_escritor(opciones.salida), politica)
    resumen = caso_de_uso.ejecutar()
    print(
        f"{resumen.n_entrada} filas leídas, {resumen.n_duplicados_eliminados} duplicados eliminados, "
        f"{resumen.n_atipicos_ajustados} atípicos recortados, {resumen.n_imputados} ingresos imputados. "
        f"Salida: {opciones.salida}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
