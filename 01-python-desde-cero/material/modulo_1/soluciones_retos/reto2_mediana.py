# reto2_mediana.py
# Reto 2: Cambiar .mean() por .median() y comparar.

import pandas as pd

df = pd.read_csv("../datos_ejemplo.csv")

print("PROMEDIO de ingreso por sexo:")
print(df.groupby("sexo")["ingreso"].mean().round(0))
print()

print("MEDIANA de ingreso por sexo:")
print(df.groupby("sexo")["ingreso"].median().round(0))
print()

# Observacion estadistica:
# La mediana es robusta a valores extremos; el promedio no.
# Si hay outliers (ingresos muy altos), promedio > mediana.
# Esta diferencia te dice algo sobre la distribucion de los datos.
