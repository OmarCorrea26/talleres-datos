# generar_fixtures.py (solo para el facilitador)
# Encadena las seis soluciones de referencia y guarda entrada/salida de cada etapa en repo/fixtures/.
import json, sys, importlib
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1] / "taller-api-muneco"
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(Path(__file__).parent))
from contrato.validaciones import validar

df = pd.read_csv(RAIZ / "datos" / "encuesta_hogares.csv")
entrada = {"registros": df.astype(object).where(df.notna(), None).to_dict(orient="records")}
nombres = ["validar", "limpiar", "calibrar", "indicadores", "precision", "publicar"]
for n, nom in enumerate(nombres, start=1):
    mod = importlib.import_module(f"etapa_{n}_{nom}")
    (RAIZ / "fixtures" / f"etapa_{n}_entrada.json").write_text(json.dumps(entrada, ensure_ascii=False), encoding="utf-8")
    salida = mod.procesar(entrada)
    errores = validar(n, entrada, salida, usar_referencia=False)
    print(f"Etapa {n} {nom}: {'OK' if not errores else errores}")
    (RAIZ / "fixtures" / f"etapa_{n}_salida.json").write_text(json.dumps(salida, ensure_ascii=False), encoding="utf-8")
    entrada = salida
print(json.dumps(salida["tabulados"][:3], indent=1, ensure_ascii=False))
