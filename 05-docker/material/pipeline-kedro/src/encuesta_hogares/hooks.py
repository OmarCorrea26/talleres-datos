"""Hooks del proyecto: código que Kedro ejecuta en momentos fijos de la corrida.

Este hook registra cuántas filas produce cada nodo. No cambia el resultado,
solo observa. Se activa en settings.py con HOOKS = (RegistroDeFilas(),).
"""

import logging
import time

import pandas as pd
from kedro.framework.hooks import hook_impl

logger = logging.getLogger(__name__)


class RegistroDeFilas:
    def __init__(self):
        self._inicio = None

    @hook_impl
    def before_pipeline_run(self, run_params):
        self._inicio = time.perf_counter()
        logger.info("Arranca la corrida del pipeline '%s'", run_params.get("pipeline_name") or "__default__")

    @hook_impl
    def after_node_run(self, node, outputs):
        for nombre, valor in outputs.items():
            if isinstance(valor, pd.DataFrame):
                logger.info("%s -> %s: %d filas, %d columnas", node.name, nombre, len(valor), valor.shape[1])

    @hook_impl
    def after_pipeline_run(self, run_params):
        segundos = time.perf_counter() - self._inicio
        logger.info("Corrida terminada en %.1f segundos", segundos)
