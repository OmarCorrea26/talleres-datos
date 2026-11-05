# ejercicio_ia.py
# Ejercicio del Modulo 4: usar IA para extender analisis_v2.py.
#
# Este archivo es el PUNTO DE PARTIDA. Tu mision es extenderlo con ayuda
# de tu asistente de IA preferido (Copilot, Cursor, Continue, Cline, etc.)
# para agregar las funcionalidades descritas mas abajo.
#
# Recomendacion: trabajalo en TU REPO de GitHub para que quede commit
# de cada mejora. Asi puedes ver tu progreso y cuanto del codigo final
# fue generado por IA vs escrito por ti.

import pandas as pd
from analisis_v2 import cargar_datos, promedio_por_grupo, exportar_a_excel


# ============================================================================
# TAREAS PARA HACER CON AYUDA DE IA
# ============================================================================
#
# Tarea 1 (FACIL):
#   Agrega una funcion percentil_por_grupo(df, variable, grupo, p) que
#   devuelva el percentil p (entre 0 y 100) de la variable, agrupado por
#   las columnas especificadas. Documentala con docstring.
#
# Tarea 2 (MEDIA):
#   Agrega validacion al inicio de main(): si datos_ejemplo.csv no existe,
#   imprime un mensaje claro indicando que el usuario debe correr primero
#   generar_datos.py. Termina la ejecucion limpiamente sin un traceback.
#
# Tarea 3 (MEDIA):
#   Agrega logging basico a las funciones existentes. Que cada funcion
#   imprima un mensaje cuando empieza y cuando termina, con un timestamp.
#   Pista: from datetime import datetime
#
# Tarea 4 (DIFICIL):
#   Refactoriza main() para que reciba como argumento la ruta del CSV
#   de entrada. Si se llama sin argumentos, usa "datos_ejemplo.csv" por
#   defecto. Pista: investiga el modulo sys.argv o argparse.
#
# ============================================================================


def main():
    df = cargar_datos("datos_ejemplo.csv")

    print("\nIngreso promedio por sexo y area:")
    print(promedio_por_grupo(df, "ingreso", ["sexo", "area"]))

    # TODO: usar la funcion que generes en la Tarea 1
    # TODO: aplicar manejo de errores de la Tarea 2
    # TODO: agregar logging de la Tarea 3
    # TODO: si hiciste la Tarea 4, lee el argumento de la linea de comandos


if __name__ == "__main__":
    main()


# ============================================================================
# REFLEXION AL FINAL
# ============================================================================
#
# Al terminar las 4 tareas, dedica 10 minutos a estas preguntas (escribe
# tus respuestas como comentarios en este mismo archivo o como un Issue
# en tu repo):
#
# 1. Cual tarea te resulto mas dificil de pedirle a la IA?
#    Que termino haciendo IA y que terminaste haciendo tu?
#
# 2. Cuantas veces la IA propuso algo INCORRECTO o subóptimo y tuviste
#    que pedirle que lo ajustara?
#
# 3. En que parte sentiste que la IA te ahorro mas tiempo? En que parte
#    sentiste que te lo hizo perder?
#
# 4. Si vuelves a hacer este mismo ejercicio mañana, que harias diferente
#    en como pides ayuda?
#
# ============================================================================
