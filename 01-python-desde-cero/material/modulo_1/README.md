# Material complementario — Módulo 1

Esta carpeta contiene los archivos que la guía te pide escribir en el Módulo 1. Sirven como respaldo: si algo no te funciona o quieres comparar contra una versión de referencia, aquí los tienes.

## Qué hay adentro

`hola.py` es el primer script de la sección 1.8. `generar_datos.py` y `analisis.py` corresponden al ejercicio práctico de la sección 1.10. En la subcarpeta `soluciones_retos/` están las cuatro soluciones de los retos opcionales de la sección 1.12.

## La idea no es copiar

La guía está hecha para que escribas tú mismo cada script siguiendo las instrucciones paso a paso. Equivocarte y corregir es parte del aprendizaje. Estos archivos los puedes usar para tres cosas:

Si algo no te funciona, compara tu código contra esta versión para encontrar la diferencia.

Si te quieres adelantar o ver el resultado esperado, ejecútalos directamente.

Si vuelves al taller meses después, puedes regenerar todo rápido sin tener que volver a escribir desde cero.

## Cómo ejecutarlos

Asumiendo que ya completaste el Módulo 0 y la sección 1.7 del Módulo 1:

```powershell
cd ruta\a\tu\proyecto
.venv\Scripts\activate
python hola.py
python generar_datos.py
python analisis.py
```

Si todavía no tienes entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install pandas openpyxl
```

## Si algo falla

Consulta la sección 1.11 (Troubleshooting del Módulo 1) en la guía principal. Los errores más comunes están documentados con su solución.
