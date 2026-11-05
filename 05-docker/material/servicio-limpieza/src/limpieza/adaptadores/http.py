"""Adaptador HTTP: la etapa 2 del muñeco, servida con FastAPI.

Ejecutar:  uvicorn limpieza.adaptadores.http:app --port 8002 --reload

Las rutas son las mismas del Taller 3 (GET /salud y POST /procesar), de modo
que el ensamblador del muñeco no nota la diferencia. Lo único que hace este
archivo es traducir: JSON a DataFrame, dominio, DataFrame a JSON.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from limpieza.adaptadores.contrato_json import registros_a_dataframe, resultado_a_salida
from limpieza.dominio import PoliticaDeLimpieza, limpiar

NUMERO = 2
NOMBRE = "limpiar"


class Entrada(BaseModel):
    registros: list[dict]
    politica: dict | None = None


app = FastAPI(
    title=f"Etapa {NUMERO} — {NOMBRE}",
    description="Eliminación de duplicados, tratamiento de atípicos e imputación de ingreso",
    version="1.0.0",
)


@app.get("/salud")
def salud():
    return {"etapa": NUMERO, "nombre": NOMBRE, "estado": "ok"}


@app.post("/procesar")
def procesar(entrada: Entrada):
    if not entrada.registros:
        raise HTTPException(status_code=422, detail="registros no puede estar vacío")
    politica = PoliticaDeLimpieza.desde_dict(entrada.politica or {})
    resultado = limpiar(registros_a_dataframe(entrada.registros), politica)
    return resultado_a_salida(resultado)
