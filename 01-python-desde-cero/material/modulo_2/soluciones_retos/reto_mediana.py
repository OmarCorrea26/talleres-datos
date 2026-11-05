# reto_mediana.py
# Reto del Modulo 2: Agregar una funcion mediana_por_grupo() al codigo,
# llamarla desde main() y exportarla al mismo Excel en una hoja distinta.

import pandas as pd
from analisis_v2 import cargar_datos, promedio_por_grupo, exportar_a_excel


def mediana_por_grupo(df, variable, grupo):
    """Calcula la mediana de una variable, agrupada por una o varias columnas.

    Mismo patron que promedio_por_grupo() pero usando .median() en lugar de .mean().
    """
    return df.groupby(grupo)[variable].median().round(0)


def main_extendido():
    df = cargar_datos("../datos_ejemplo.csv")

    # Calcular promedio y mediana
    promedio = promedio_por_grupo(df, "ingreso", ["sexo", "area"])
    mediana = mediana_por_grupo(df, "ingreso", ["sexo", "area"])

    print("Promedio por sexo y area:")
    print(promedio)
    print()
    print("Mediana por sexo y area:")
    print(mediana)

    # Exportar ambas a un mismo Excel en hojas distintas
    # Aqui usamos ExcelWriter directamente porque queremos varias hojas.
    promedio_df = promedio.reset_index()
    mediana_df = mediana.reset_index()
    promedio_df.columns = ["sexo", "area", "ingreso_promedio"]
    mediana_df.columns = ["sexo", "area", "ingreso_mediana"]

    with pd.ExcelWriter("resumen_extendido.xlsx") as writer:
        promedio_df.to_excel(writer, sheet_name="Promedio", index=False)
        mediana_df.to_excel(writer, sheet_name="Mediana", index=False)

    print("\nArchivo resumen_extendido.xlsx creado con dos hojas: Promedio y Mediana.")


if __name__ == "__main__":
    main_extendido()
