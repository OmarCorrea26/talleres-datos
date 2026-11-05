# analisis_v2.py
# Version migrada del notebook analisis.ipynb a un script .py modular.
# Taller de Python para Analistas Estadisticos - Modulo 2
#
# Diferencias clave con la version del Modulo 1 (analisis.py):
#   - El codigo esta organizado en funciones reutilizables
#   - Cada funcion tiene un docstring (entre comillas triples)
#   - Una funcion main() orquesta todo
#   - El bloque "if __name__ == '__main__':" permite que este archivo
#     funcione como script (correrlo) o como modulo (importar sus funciones)

import pandas as pd


def cargar_datos(ruta_csv):
    """Carga el archivo CSV y devuelve un DataFrame.

    Parametros
    ----------
    ruta_csv : str
        Ruta al archivo CSV de entrada.

    Devuelve
    --------
    pandas.DataFrame
        El DataFrame con los datos cargados.
    """
    df = pd.read_csv(ruta_csv)
    print(f"Cargadas {len(df)} filas desde {ruta_csv}")
    return df


def promedio_por_grupo(df, variable, grupo):
    """Calcula el promedio de una variable, agrupada por una o varias columnas.

    Parametros
    ----------
    df : pandas.DataFrame
        El DataFrame con los datos.
    variable : str
        Nombre de la columna numerica sobre la que calcular el promedio.
    grupo : str o list
        Columna o lista de columnas por las que agrupar.

    Devuelve
    --------
    pandas.Series
        Promedios redondeados al entero mas cercano.

    Ejemplo
    -------
    >>> promedio_por_grupo(df, "ingreso", "sexo")
    >>> promedio_por_grupo(df, "ingreso", ["sexo", "area"])
    """
    return df.groupby(grupo)[variable].mean().round(0)


def conteo_por_categoria(df, columna):
    """Cuenta los valores de una columna categorica.

    Parametros
    ----------
    df : pandas.DataFrame
        El DataFrame con los datos.
    columna : str
        Nombre de la columna categorica.

    Devuelve
    --------
    pandas.Series
        Conteo de cada categoria.
    """
    return df[columna].value_counts()


def exportar_a_excel(resultado, ruta_salida, hoja="Resumen"):
    """Exporta un resultado (Series o DataFrame) a un archivo Excel.

    Parametros
    ----------
    resultado : pandas.Series o pandas.DataFrame
        El objeto a exportar. Si es Series, se convierte a DataFrame primero.
    ruta_salida : str
        Ruta del archivo Excel de salida.
    hoja : str, opcional
        Nombre de la hoja dentro del archivo. Por defecto "Resumen".
    """
    if isinstance(resultado, pd.Series):
        resultado = resultado.reset_index()

    resultado.to_excel(ruta_salida, index=False, sheet_name=hoja)
    print(f"Archivo {ruta_salida} creado en la hoja '{hoja}'.")


def main():
    """Punto de entrada: orquesta la carga, el analisis y la exportacion."""

    # 1. Cargar
    df = cargar_datos("datos_ejemplo.csv")

    # 2. Conteos
    print("\nConteo por sexo:")
    print(conteo_por_categoria(df, "sexo"))

    # 3. Promedios por distintos grupos (reusando la MISMA funcion)
    print("\nIngreso promedio por sexo:")
    print(promedio_por_grupo(df, "ingreso", "sexo"))

    print("\nIngreso promedio por area:")
    print(promedio_por_grupo(df, "ingreso", "area"))

    print("\nIngreso promedio por sexo y area:")
    cruzado = promedio_por_grupo(df, "ingreso", ["sexo", "area"])
    print(cruzado)

    print("\nEdad promedio por area:")
    print(promedio_por_grupo(df, "edad", "area"))

    # 4. Exportar
    exportar_a_excel(cruzado, "resumen.xlsx", hoja="ingreso_por_sexo_area")


# Este bloque hace que main() solo se ejecute si corres "python analisis_v2.py"
# directamente, pero NO si alguien importa funciones desde este archivo.
# Es una convencion estandar de Python.
if __name__ == "__main__":
    main()
