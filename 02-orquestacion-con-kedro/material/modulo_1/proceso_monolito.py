# proceso_monolito.py
# El "antes" del taller: el script del Taller 1 seis meses después.
# Hace todo el proceso de la encuesta en un solo archivo, de corrido.
# Funciona, y ese es justamente el problema: mira cuántas rutas, cuántos
# números sueltos y cuánto orden implícito hay que recordar para correrlo.
#
# Ejecutar desde la carpeta material/:  python modulo_1/proceso_monolito.py

import math

import pandas as pd

# --- 1. Cargar (ruta escrita a mano) ---------------------------------------
df = pd.read_csv("datos/encuesta_hogares.csv")

# --- 2. Validar ------------------------------------------------------------
columnas = ["id_persona", "id_hogar", "departamento", "area", "sexo",
            "edad", "ocupado", "ingreso", "factor_expansion"]
faltan = [c for c in columnas if c not in df.columns]
if faltan:
    raise SystemExit(f"Faltan columnas: {faltan}")
df["ocupado"] = df["ocupado"].astype("Int64")
print("filas cargadas:", len(df))

# --- 3. Limpiar ------------------------------------------------------------
df = df.drop_duplicates(subset="id_persona").reset_index(drop=True)
p99 = df["ingreso"].quantile(0.99)                    # umbral escrito a mano
df.loc[df["ingreso"] > p99, "ingreso"] = p99
faltantes = (df["ocupado"] == 1) & df["ingreso"].isna()
mediana = df[df["ocupado"] == 1].groupby(["area", "sexo"])["ingreso"].transform("median")
df.loc[faltantes, "ingreso"] = mediana[faltantes]
print("filas tras limpiar:", len(df), "imputados:", int(faltantes.sum()))

# --- 4. Calibrar (totales escritos a mano) ---------------------------------
objetivo = {"Antioquia": 90000, "Bogota": 110000, "Narino": 35000,
            "Santander": 55000, "Valle": 70000}
suma = df.groupby("departamento")["factor_expansion"].sum()
df["factor_calibrado"] = df["factor_expansion"] * df["departamento"].map(
    {d: objetivo[d] / suma[d] for d in objetivo})

# --- 5. Estimar ------------------------------------------------------------
pet = df[df["edad"] >= 15].copy()                     # otro número suelto
pet["ocupado"] = pet["ocupado"].astype(float)
filas = []
for (dpto, sexo), g in pet.groupby(["departamento", "sexo"]):
    w = g["factor_calibrado"]
    x = g["ocupado"]
    valor = (x * w).sum() / w.sum()
    var = (w * (x - valor) ** 2).sum() / w.sum()
    n_ef = w.sum() ** 2 / (w ** 2).sum()
    ee = math.sqrt(var / n_ef)
    filas.append({"indicador": "tasa_ocupacion", "departamento": dpto, "sexo": sexo,
                  "valor": valor, "cv": 100 * ee / valor})
resultado = pd.DataFrame(filas)
resultado["calidad"] = resultado["cv"].apply(
    lambda cv: "buena" if cv <= 7.5 else "aceptable" if cv <= 15 else "poco confiable")

# --- 6. Publicar (otra ruta escrita a mano) --------------------------------
resultado.to_excel("salida_monolito.xlsx", index=False)
print(resultado.to_string(index=False))
print("guardado en salida_monolito.xlsx")
