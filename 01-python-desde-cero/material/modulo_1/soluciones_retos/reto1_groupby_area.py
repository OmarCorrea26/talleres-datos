# reto1_groupby_area.py
# Reto 1: Agrupar por area en lugar de por sexo.
# Pregunta: Cual tiene mayor ingreso promedio, Urbana o Rural?

import pandas as pd

df = pd.read_csv("../datos_ejemplo.csv")

print("Promedio de ingreso por area:")
print(df.groupby("area")["ingreso"].mean().round(0))

# Nota: como los datos son sinteticos con seed=42, el resultado es siempre
# el mismo. Con esta semilla, el ingreso promedio Rural es mayor que el
# Urbano. Si cambias la semilla en generar_datos.py el resultado cambia.
