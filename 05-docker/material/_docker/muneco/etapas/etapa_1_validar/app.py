# etapas/etapa_1_validar/app.py
# Etapa 1 — validar, implementada (version de referencia del Taller 3).
# Ejecutar desde la raiz del repo:  uvicorn etapas.etapa_1_validar.app:app --port 8001

import pandas as pd

COLUMNAS = ["id_persona", "id_hogar", "departamento", "area", "sexo",
            "edad", "ocupado", "ingreso", "factor_expansion"]

def procesar(entrada: dict) -> dict:
    df = pd.DataFrame(entrada["registros"])

    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas obligatorias: {faltan}")
    df = df[COLUMNAS]                                   # descarta columnas de mas y fija el orden

    # Tipado explicito: lo que entra como texto o float sale con su tipo correcto
    df["id_persona"] = df["id_persona"].astype(int)
    df["id_hogar"] = df["id_hogar"].astype(int)
    df["edad"] = df["edad"].astype(int)
    df["ocupado"] = df["ocupado"].astype("Int64")       # entero que admite nulos
    df["ingreso"] = pd.to_numeric(df["ingreso"], errors="coerce")
    df["factor_expansion"] = df["factor_expansion"].astype(float)
    for c in ["departamento", "area", "sexo"]:
        df[c] = df[c].astype(str).str.strip()

    resumen = {
        "n_filas": int(len(df)),
        "columnas": COLUMNAS,
        "n_nulos_por_columna": {c: int(df[c].isna().sum()) for c in COLUMNAS},
    }
    # Pandas -> JSON: los nulos deben salir como None, no como NaN
    registros = df.astype(object).where(df.notna(), None).to_dict(orient="records")
    return {"registros": registros, "resumen": resumen}


from contrato.servicio import crear_app

NUMERO = 1
app = crear_app(NUMERO, procesar)
