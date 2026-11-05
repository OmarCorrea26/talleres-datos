import pandas as pd
import pytest


@pytest.fixture
def encuesta_minima() -> pd.DataFrame:
    """Cinco personas: un duplicado, un atípico evidente y un ocupado sin ingreso."""
    return pd.DataFrame(
        {
            "id_persona": [1, 2, 3, 3, 4],
            "id_hogar": [1, 1, 2, 2, 3],
            "departamento": ["Bogota", "Bogota", "Valle", "Valle", "Valle"],
            "area": ["Urbana", "Urbana", "Urbana", "Urbana", "Rural"],
            "sexo": ["H", "H", "H", "H", "M"],
            "edad": [30, 40, 25, 25, 50],
            "ocupado": pd.array([1, 1, 1, 1, 0], dtype="Int64"),
            "ingreso": [1_000_000.0, None, 50_000_000.0, 50_000_000.0, None],
            "factor_expansion": [100.0, 100.0, 50.0, 50.0, 50.0],
        }
    )
