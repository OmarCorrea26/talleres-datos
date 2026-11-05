# etapas/etapa_5_precision/app.py
# Etapa 5 — precision, implementada (version de referencia del Taller 3).
# Ejecutar desde la raiz del repo:  uvicorn etapas.etapa_5_precision.app:app --port 8005

import math
import pandas as pd

Z = 1.96  # cuantil normal para un intervalo del 95 %

def _error_estandar(g: pd.DataFrame, variable: str) -> float:
    w = g["factor_calibrado"]
    x = g[variable].astype(float)
    media = (x * w).sum() / w.sum()
    # Varianza ponderada de la variable dentro del dominio
    var = (w * (x - media) ** 2).sum() / w.sum()
    # Tamano de muestra efectivo (Kish): penaliza la dispersion de los pesos
    n_ef = w.sum() ** 2 / (w ** 2).sum()
    return math.sqrt(var / n_ef)

def procesar(entrada: dict) -> dict:
    df = pd.DataFrame(entrada["registros"])
    salida = []
    for ind in entrada["indicadores"]:
        if ind["indicador"] == "tasa_ocupacion":
            base, variable = df[df["edad"] >= 15], "ocupado"
        else:
            base, variable = df[df["ocupado"] == 1], "ingreso"
        mask = pd.Series(True, index=base.index)
        for k, v in ind["desagregacion"].items():
            mask &= base[k].astype(str) == v
        ee = _error_estandar(base[mask], variable)
        valor = ind["valor"]
        salida.append({
            **ind,
            "error_estandar": ee,
            "cv": 100 * ee / valor if valor else 0.0,
            "limite_inferior": valor - Z * ee,
            "limite_superior": valor + Z * ee,
        })
    return {"indicadores": salida}


from contrato.servicio import crear_app

NUMERO = 5
app = crear_app(NUMERO, procesar)
