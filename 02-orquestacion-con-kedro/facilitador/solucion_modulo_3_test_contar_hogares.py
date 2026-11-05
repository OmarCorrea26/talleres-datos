# Solución de referencia. Ejercicio 3.8: prueba para contar_hogares.
# Va en tests/pipelines/preparacion/test_nodes.py, junto a las demás.

import pandas as pd

from encuesta_hogares.pipelines.preparacion.nodes import contar_hogares


def test_contar_hogares_no_repite_hogares():
    encuesta = pd.DataFrame(
        {
            "departamento": ["Bogota", "Bogota", "Bogota", "Valle"],
            "id_hogar": [1, 1, 2, 7],
        }
    )
    assert contar_hogares(encuesta) == {"Bogota": 2, "Valle": 1}
