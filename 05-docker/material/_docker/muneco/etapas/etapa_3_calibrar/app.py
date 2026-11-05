# etapas/etapa_3_calibrar/app.py
# Etapa 3 — calibrar, implementada (version de referencia del Taller 3).
# Ejecutar desde la raiz del repo:  uvicorn etapas.etapa_3_calibrar.app:app --port 8003

import json
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OBJETIVO = json.loads((RAIZ / "contrato" / "poblacion_objetivo.json").read_text(encoding="utf-8"))

def procesar(entrada: dict) -> dict:
    df = pd.DataFrame(entrada["registros"])

    # Suma de factores crudos por departamento y razon de ajuste
    suma_cruda = df.groupby("departamento")["factor_expansion"].sum()
    razon = {d: OBJETIVO[d] / suma_cruda[d] for d in OBJETIVO}
    df["factor_calibrado"] = df["factor_expansion"] * df["departamento"].map(razon)

    totales = df.groupby("departamento")["factor_calibrado"].sum().round(2).to_dict()
    resumen = {
        "totales_por_departamento": {k: float(v) for k, v in totales.items()},
        "poblacion_objetivo": {k: float(v) for k, v in OBJETIVO.items()},
    }
    df["ocupado"] = df["ocupado"].astype("Int64")
    registros = df.astype(object).where(df.notna(), None).to_dict(orient="records")
    return {"registros": registros, "resumen": resumen}


from contrato.servicio import crear_app

NUMERO = 3
app = crear_app(NUMERO, procesar)
