"""Ensamble del pipeline de estimación."""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import calcular_precision, clasificar_calidad, estimar_indicadores, generar_metadatos


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=estimar_indicadores,
                inputs=["encuesta_calibrada", "params:estimacion"],
                outputs="indicadores",
                name="estimar_indicadores",
            ),
            node(
                func=calcular_precision,
                inputs=["encuesta_calibrada", "indicadores", "params:estimacion"],
                outputs="indicadores_con_precision",
                name="calcular_precision",
            ),
            node(
                func=clasificar_calidad,
                inputs=["indicadores_con_precision", "params:umbrales_cv"],
                outputs="tabulados",
                name="clasificar_calidad",
            ),
            node(
                func=generar_metadatos,
                inputs=["tabulados", "params:umbrales_cv", "params:estimacion"],
                outputs="metadatos",
                name="generar_metadatos",
            ),
        ]
    )
