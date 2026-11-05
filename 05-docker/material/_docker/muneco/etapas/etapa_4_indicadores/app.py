# etapas/etapa_4_indicadores/app.py
# Etapa 4 — indicadores, implementada (version de referencia del Taller 3).
# Ejecutar desde la raiz del repo:  uvicorn etapas.etapa_4_indicadores.app:app --port 8004

import pandas as pd

def _estimar(df: pd.DataFrame, variable: str, grupos: list[str], nombre: str) -> list[dict]:
    salida = []
    for claves, g in df.groupby(grupos):
        if not isinstance(claves, tuple):
            claves = (claves,)
        w = g["factor_calibrado"]
        salida.append({
            "indicador": nombre,
            "desagregacion": {k: str(v) for k, v in zip(grupos, claves)},
            "valor": float((g[variable] * w).sum() / w.sum()),
            "n_muestra": int(len(g)),
            "poblacion_estimada": float(w.sum()),
        })
    return salida

def procesar(entrada: dict) -> dict:
    df = pd.DataFrame(entrada["registros"])

    # Tasa de ocupacion: ocupados / poblacion de 15 anos o mas, ponderado, por departamento x sexo
    pet = df[df["edad"] >= 15].copy()
    pet["ocupado"] = pet["ocupado"].astype(float)
    tasas = _estimar(pet, "ocupado", ["departamento", "sexo"], "tasa_ocupacion")

    # Ingreso promedio de los ocupados, ponderado, por area
    ocu = df[df["ocupado"] == 1].copy()
    ingresos = _estimar(ocu, "ingreso", ["area"], "ingreso_promedio")

    return {"registros": entrada["registros"], "indicadores": tasas + ingresos}


from contrato.servicio import crear_app

NUMERO = 4
app = crear_app(NUMERO, procesar)
