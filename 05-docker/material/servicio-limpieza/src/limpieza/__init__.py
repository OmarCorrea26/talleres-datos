"""Etapa de limpieza de la encuesta de hogares.

La estructura dice de qué trata el paquete antes de abrir un archivo:

    dominio/      las reglas de limpieza y lo que necesitan del exterior (puertos)
    aplicacion/   el caso de uso que las orquesta
    adaptadores/  las formas de entrar y salir: archivos, HTTP, Kedro, terminal

Las dependencias apuntan hacia adentro: los adaptadores conocen al dominio,
el dominio no conoce a nadie.
"""
