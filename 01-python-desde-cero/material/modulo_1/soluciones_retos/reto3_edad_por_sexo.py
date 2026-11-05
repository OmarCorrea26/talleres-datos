# reto3_edad_por_sexo.py
# Reto 3: Calcular la edad promedio por sexo.

import pandas as pd

df = pd.read_csv("../datos_ejemplo.csv")

print("Edad promedio por sexo:")
print(df.groupby("sexo")["edad"].mean().round(1))

# Variante util: edad promedio y desviacion estandar al tiempo
print()
print("Edad promedio y desviacion estandar por sexo:")
print(df.groupby("sexo")["edad"].agg(["mean", "std"]).round(1))
