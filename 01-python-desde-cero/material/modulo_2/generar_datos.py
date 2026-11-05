# generar_datos.py
# Crea un CSV sintetico con 100 personas para los ejercicios del taller
# Taller de Python para Analistas Estadisticos - Modulo 1

import pandas as pd
import numpy as np

# Semilla para reproducibilidad: los numeros aleatorios saldran iguales cada vez
np.random.seed(42)

n = 100

datos = pd.DataFrame({
    "id":      range(1, n + 1),
    "edad":    np.random.randint(18, 75, size=n),
    "sexo":    np.random.choice(["H", "M"], size=n),
    "ingreso": np.random.randint(500000, 5000000, size=n),
    "area":    np.random.choice(["Urbana", "Rural"], size=n, p=[0.7, 0.3]),
})

datos.to_csv("datos_ejemplo.csv", index=False)
print(f"Archivo creado con {len(datos)} filas")
