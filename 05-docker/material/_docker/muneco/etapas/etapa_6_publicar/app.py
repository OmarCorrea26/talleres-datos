# etapas/etapa_6_publicar/app.py
# Etapa 6 — publicar, implementada (version de referencia del Taller 3).
# Ejecutar desde la raiz del repo:  uvicorn etapas.etapa_6_publicar.app:app --port 8006

from datetime import date
from pathlib import Path
import pandas as pd

from contrato.validaciones import clasificar_calidad

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "salida" / "tabulados.xlsx"

def procesar(entrada: dict) -> dict:
    tabulados = [{**i, "calidad": clasificar_calidad(i["cv"])} for i in entrada["indicadores"]]

    # Version plana para Excel: una columna por desagregacion
    filas = []
    for t in tabulados:
        fila = {k: v for k, v in t.items() if k != "desagregacion"}
        fila.update(t["desagregacion"])
        filas.append(fila)
    SALIDA.parent.mkdir(exist_ok=True)
    pd.DataFrame(filas).to_excel(SALIDA, index=False, sheet_name="tabulados")

    metadatos = {
        "titulo": "Tabulados de ocupacion e ingreso — encuesta sintetica de hogares",
        "fuente": "Taller 3 — datos ficticios generados con datos/generar_datos.py",
        "fecha_proceso": date.today().isoformat(),
        "n_indicadores": len(tabulados),
        "nota_metodologica": (
            "Estimaciones ponderadas con factores calibrados por departamento. "
            "Calidad segun coeficiente de variacion: buena (<=7.5 %), aceptable (7.5-15 %), "
            "poco confiable (>15 %). Intervalos de confianza al 95 %."
        ),
    }
    return {"metadatos": metadatos, "tabulados": tabulados, "archivo_excel": str(SALIDA.relative_to(RAIZ)).replace("\\", "/")}


from contrato.servicio import crear_app

NUMERO = 6
app = crear_app(NUMERO, procesar)
