"""Ensamble del pipeline de preparación."""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import calibrar, limpiar, validar


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=validar,
                inputs="encuesta_cruda",
                outputs=["encuesta_validada", "resumen_validacion"],
                name="validar",
            ),
            node(
                func=limpiar,
                inputs=["encuesta_validada", "params:limpieza"],
                outputs=["encuesta_limpia", "resumen_limpieza"],
                name="limpiar",
            ),
            node(
                func=calibrar,
                inputs=["encuesta_limpia", "params:poblacion_objetivo"],
                outputs=["encuesta_calibrada", "resumen_calibracion"],
                name="calibrar",
            ),
        ]
    )
