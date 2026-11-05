"""Registro de pipelines del proyecto.

Kedro puede descubrir solo los pipelines de src/encuesta_hogares/pipelines/
con find_pipelines(). Aquí se registran a mano porque, además de los dos
pipelines base, se arma una variante (la estimación solo para el área rural)
que no corresponde a ninguna carpeta.
"""

from __future__ import annotations

from kedro.pipeline import Pipeline, node, pipeline

from encuesta_hogares.pipelines import estimacion, preparacion
from encuesta_hogares.pipelines.estimacion.nodes import filtrar_area


def register_pipelines() -> dict[str, Pipeline]:
    pipeline_preparacion = preparacion.create_pipeline()
    pipeline_estimacion = estimacion.create_pipeline()

    # La misma estimación, bajo el espacio de nombres "rural", alimentada con un
    # subconjunto de la base. Los parámetros se comparten con la versión nacional.
    pipeline_rural = pipeline(
        [
            node(
                func=filtrar_area,
                inputs=["encuesta_calibrada", "params:area_de_interes"],
                outputs="encuesta_rural",
                name="filtrar_rural",
            )
        ]
    ) + pipeline(
        pipeline_estimacion,
        namespace="rural",
        inputs={"encuesta_calibrada": "encuesta_rural"},
        parameters={"params:estimacion", "params:umbrales_cv"},
    )

    return {
        "preparacion": pipeline_preparacion,
        "estimacion": pipeline_estimacion,
        "estimacion_rural": pipeline_rural,
        "__default__": pipeline_preparacion + pipeline_estimacion,
    }
