# analisis.py
# Carga el CSV y hace un analisis estadistico basico
# Taller de Python para Analistas Estadisticos - Modulo 1

import pandas as pd

# Cargar el archivo
df = pd.read_csv("datos_ejemplo.csv")

# 1. Primeras 5 filas
#    Equivalente a: PROC PRINT(OBS=5) en SAS  |  head(df) en R
print("Primeras 5 filas:")
print(df.head())
print()

# 2. Resumen estadistico de las variables numericas
#    Equivalente a: PROC MEANS en SAS  |  summary(df) en R
print("Resumen estadistico:")
print(df.describe())
print()

# 3. Conteo de personas por sexo
#    Equivalente a: PROC FREQ en SAS  |  table(df$sexo) en R
print("Conteo por sexo:")
print(df["sexo"].value_counts())
print()

# 4. Promedio de ingreso por sexo
#    Equivalente a: PROC MEANS CLASS=sexo en SAS  |  group_by + summarise en R
print("Promedio de ingreso por sexo:")
print(df.groupby("sexo")["ingreso"].mean().round(0))
print()

# 5. Promedio de ingreso por sexo y area
print("Promedio de ingreso por sexo y area:")
print(df.groupby(["sexo", "area"])["ingreso"].mean().round(0))
