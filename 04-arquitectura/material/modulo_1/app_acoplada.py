# app_acoplada.py
# El "antes" del Taller 4: la etapa 2 del muñeco tal como suele quedar cuando
# funciona y se entrega. Todo en un archivo: el servidor HTTP, la traducción
# de JSON, las reglas estadísticas y las constantes metodológicas.
#
# Funciona. Pásale el fixture del muñeco y cumple el contrato. El problema no
# es que esté mal: es que tiene cuatro razones distintas para cambiar y todas
# viven en las mismas treinta líneas.
#
# Ejecutar:  uvicorn app_acoplada:app --port 8002 --reload   (desde modulo_1/)

import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Etapa 2 — limpiar", version="1.0.0")

PERCENTIL = 0.99                     # decisión metodológica, escondida como constante
GRUPOS = ["area", "sexo"]            # otra


@app.get("/salud")
def salud():
    return {"etapa": 2, "nombre": "limpiar", "estado": "ok"}


@app.post("/procesar")
async def procesar(request: Request):
    entrada = await request.json()                          # transporte
    try:
        df = pd.DataFrame(entrada["registros"])             # traducción JSON -> pandas
        df["ocupado"] = df["ocupado"].astype("Int64")
        n_entrada = len(df)

        df = df.drop_duplicates(subset="id_persona").reset_index(drop=True)   # regla 1
        n_dup = n_entrada - len(df)

        p99 = df["ingreso"].quantile(PERCENTIL)                               # regla 2
        atipicos = df["ingreso"] > p99
        df.loc[atipicos, "ingreso"] = p99

        df["ingreso_imputado"] = False                                        # regla 3
        faltan = (df["ocupado"] == 1) & df["ingreso"].isna()
        mediana = df[df["ocupado"] == 1].groupby(GRUPOS)["ingreso"].transform("median")
        df.loc[faltan, "ingreso"] = mediana[faltan]
        df.loc[faltan, "ingreso_imputado"] = True

        resumen = {                                                           # resumen
            "n_entrada": int(n_entrada),
            "n_duplicados_eliminados": int(n_dup),
            "n_salida": int(len(df)),
            "n_imputados": int(faltan.sum()),
            "n_atipicos_ajustados": int(atipicos.sum()),
            "metodo_imputacion": "mediana del ingreso de ocupados por area x sexo; atipicos recortados al percentil 99",
        }
        registros = df.astype(object).where(df.notna(), None).to_dict(orient="records")  # pandas -> JSON
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
    return JSONResponse(content={"registros": registros, "resumen": resumen})    # transporte
