# etapas/etapa_2_limpiar/app.py
# Etapa 2 — limpiar, implementada (version de referencia del Taller 3).
# Ejecutar desde la raiz del repo:  uvicorn etapas.etapa_2_limpiar.app:app --port 8002

import pandas as pd

def procesar(entrada: dict) -> dict:
    df = pd.DataFrame(entrada["registros"])
    n_entrada = len(df)

    # 1) Duplicados exactos por id_persona (la llave de la encuesta)
    df = df.drop_duplicates(subset="id_persona").reset_index(drop=True)
    n_dup = n_entrada - len(df)

    # 2) Atipicos de ingreso: todo lo que supere el percentil 99 se recorta a ese valor (winsorizacion)
    p99 = df["ingreso"].quantile(0.99)
    atipicos = df["ingreso"] > p99
    df.loc[atipicos, "ingreso"] = p99
    n_atip = int(atipicos.sum())

    # 3) Imputacion: ocupados sin ingreso reciben la mediana de su grupo area x sexo
    df["ingreso_imputado"] = False
    faltan = (df["ocupado"] == 1) & df["ingreso"].isna()
    mediana = df[df["ocupado"] == 1].groupby(["area", "sexo"])["ingreso"].transform("median")
    df.loc[faltan, "ingreso"] = mediana[faltan]
    df.loc[faltan, "ingreso_imputado"] = True

    resumen = {
        "n_entrada": int(n_entrada),
        "n_duplicados_eliminados": int(n_dup),
        "n_salida": int(len(df)),
        "n_imputados": int(faltan.sum()),
        "n_atipicos_ajustados": n_atip,
        "metodo_imputacion": "mediana del ingreso de ocupados por area x sexo; atipicos recortados al percentil 99",
    }
    df["ocupado"] = df["ocupado"].astype("Int64")
    registros = df.astype(object).where(df.notna(), None).to_dict(orient="records")
    return {"registros": registros, "resumen": resumen}


from contrato.servicio import crear_app

NUMERO = 2
app = crear_app(NUMERO, procesar)
