# reto4_exportar_excel.py
# Reto 4: Exportar el resultado del groupby a un archivo Excel.

import pandas as pd

df = pd.read_csv("../datos_ejemplo.csv")

# Paso 1: guardar el resultado del groupby en una variable
# (groupby devuelve una Serie; .reset_index() la convierte a DataFrame,
#  que se exporta mejor a Excel con encabezados claros)
resumen = df.groupby("sexo")["ingreso"].mean().round(0).reset_index()
resumen.columns = ["sexo", "ingreso_promedio"]

# Paso 2: exportar a Excel
resumen.to_excel("resumen.xlsx", index=False)

print("Archivo resumen.xlsx creado correctamente.")
print()
print("Contenido exportado:")
print(resumen)

# Nota tecnica:
# .to_excel() requiere el paquete openpyxl, que ya instalaste en el Modulo 1.
# Si te da error de "ModuleNotFoundError: openpyxl", ejecuta en la terminal
# (con el entorno virtual activo):
#     pip install openpyxl
