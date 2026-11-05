# Módulo 2 — De Jupyter a .py

En el Módulo 1 escribiste scripts cortos donde el código vivía suelto, una instrucción tras otra. En proyectos reales eso no se sostiene: necesitas código modular, funciones reutilizables, y la capacidad de migrar trabajo exploratorio (notebooks) a producción (scripts). Este módulo va por todo eso.

Al final vas a haber reescrito el análisis del Módulo 1 usando funciones, abierto y entendido un notebook Jupyter, y migrado ese notebook a un .py modular. Calcula unas dos horas.

### Lo que necesitas antes de empezar

La carpeta taller_python del Módulo 1, con su .venv funcionando y pandas y openpyxl instalados (verifica con pip list). Y haber hecho los ejercicios del M1 — el análisis que ya tienes es la base sobre la que vamos a construir.

## 2.1 ¿Qué es una función? Por qué importan

Una función es un bloque de código nombrado que recibe entradas (parámetros) y devuelve una salida. Es la unidad básica de organización del código profesional.

¿Para qué tomarse el trabajo de envolver código en funciones? Por cuatro razones que importan en el día a día: el código se vuelve reutilizable (lo escribes una vez, lo usas muchas), el nombre describe la intención mientras el cuerpo describe la implementación, puedes probar una función aisladamente con distintos datos sin tener que correr todo el script, y puedes combinarlas para construir cosas más grandes.

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> Si vienes de SAS, una función en Python es análoga a una MACRO: encapsulas un bloque de código que reutilizas. La diferencia técnica es que las funciones de Python son de primera clase (puedes pasarlas como argumento, asignarlas a variables), lo que las hace más flexibles. Si vienes de R, function(x) { ... } es literalmente lo mismo, solo cambia la sintaxis: en Python se usa def en lugar de function.

## 2.2 Escribir tu primera función desde cero

Crea un archivo nuevo en VSCode llamado primeras_funciones.py y escribe:

```python
# primeras_funciones.py
# Aprendiendo a escribir funciones en Python

def cuadrado(x):
    """Devuelve el cuadrado de un numero."""
    return x * x

def es_mayor_de_edad(edad):
    """Devuelve True si la edad es 18 o mas, False de lo contrario."""
    return edad >= 18

def saludo(nombre, formal=False):
    """Construye un saludo personalizado.

    Si formal=True usa un saludo formal, de lo contrario uno casual.
    """
    if formal:
        return f"Buenos dias, Sr./Sra. {nombre}"
    else:
        return f"Hola, {nombre}!"

# Ejecutar las funciones para ver que devuelven
print(cuadrado(5))
print(cuadrado(12))
print(es_mayor_de_edad(20))
print(es_mayor_de_edad(15))
print(saludo("Ana"))
print(saludo("Ana", formal=True))
```

Ejecutar:

```powershell
python primeras_funciones.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver: 25 144 True False Hola, Ana! Buenos dias, Sr./Sra. Ana

### Anatomía de una función Python

| Elemento | Significado |
|----|----|
| `def` | Palabra clave que indica "defino una función" |
| `cuadrado(x)` | Nombre de la función y sus parámetros |
| `:` | Indica que empieza el cuerpo (obligatorio) |
| `indentación (4 espacios)` | Marca qué líneas pertenecen a la función |
| `docstring` | Cadena triple-comillas que documenta qué hace la función |
| `return` | Devuelve un valor al código que llamó la función |
| `formal=False` | Parámetro con valor por defecto (es opcional) |

## 2.3 Funciones con pandas — parametrizar tu análisis

Ahora viene la parte poderosa: vamos a tomar el análisis del Módulo 1 y convertirlo en funciones. Crea un archivo nuevo analisis_funciones.py:

```python
# analisis_funciones.py
# Reescribiendo el analisis del Modulo 1 usando funciones

import pandas as pd

def cargar_datos(ruta_csv):
    """Carga el CSV y devuelve un DataFrame."""
    df = pd.read_csv(ruta_csv)
    print(f"Cargadas {len(df)} filas desde {ruta_csv}")
    return df

def promedio_por_grupo(df, variable, grupo):
    """Calcula el promedio de una variable agrupada por una o varias columnas.

    Parametros:
        df: el DataFrame
        variable: nombre de la columna numerica (ej: "ingreso")
        grupo: nombre de columna o lista (ej: "sexo" o ["sexo", "area"])
    """
    return df.groupby(grupo)[variable].mean().round(0)

# Cargar una vez, usar la funcion muchas veces
df = cargar_datos("datos_ejemplo.csv")

print("\nIngreso promedio por sexo:")
print(promedio_por_grupo(df, "ingreso", "sexo"))

print("\nIngreso promedio por area:")
print(promedio_por_grupo(df, "ingreso", "area"))

print("\nIngreso promedio por sexo y area:")
print(promedio_por_grupo(df, "ingreso", ["sexo", "area"]))

print("\nEdad promedio por sexo:")
print(promedio_por_grupo(df, "edad", "sexo"))
```

Ejecutar:

```powershell
python analisis_funciones.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver cuatro bloques de resultados: ingreso por sexo, ingreso por área, ingreso cruzado por sexo y área, edad por sexo.

Fíjate en algo: la misma función promedio_por_grupo aparece cuatro veces con argumentos distintos. Esa es la razón por la que valen la pena las funciones — escribes la lógica una vez y la reutilizas. Si mañana decides calcular cualquier otra estadística agrupada (por nivel educativo, por estrato, por lo que sea), agregas una línea de llamada y listo, no escribes lógica nueva.

## 2.4 ¿Qué es un notebook Jupyter?

Un notebook Jupyter (extensión .ipynb) es un documento interactivo que combina código ejecutable, texto explicativo (Markdown), tablas, gráficos y resultados en un mismo archivo.

Internamente es un archivo JSON con dos tipos de celdas:

- Celdas de código — ejecutables, una por una
- Celdas de Markdown — texto formateado para documentación

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> Si vienes de R, un notebook Jupyter es el primo de R Markdown (.Rmd). Misma filosofía: literate programming. Mismo riesgo: la facilidad de ir saltando entre celdas te puede llevar a un estado donde el código no funciona si lo corres de arriba a abajo en orden.

### Cuándo usar notebook, cuándo .py

No es que uno sea mejor que el otro — son herramientas distintas. Jupyter sirve para explorar datos por primera vez, prototipar rápido, mostrar resultados con gráficos al lado del código, y comunicar análisis paso a paso. El .py sirve cuando el análisis ya está estable, vas a automatizar la ejecución, vas a versionar en Git, o vas a importar funciones desde otros archivos. La regla simple: empieza en notebook, termina en .py.

### Abrir un notebook en VSCode

En la carpeta del Módulo 2 (que recibiste como material complementario) está el archivo analisis.ipynb. Copia ese archivo a tu carpeta taller_python para trabajar con él.

Al abrirlo en VSCode:

1. Haz doble clic en analisis.ipynb
1. VSCode te puede pedir seleccionar un kernel. Elige el de tu .venv (busca el path que contenga .venv\Scripts\python.exe).
1. Ejecuta la primera celda con Shift + Enter o el botón de play.
1. Continúa ejecutando celda por celda en orden.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Las celdas deben ejecutarse sin errores y mostrar resultados después de cada una (tablas, conteos, descripciones).

> [!WARNING]
> **⚠️ Atención**
>
> Si la primera celda te da un error como ModuleNotFoundError: pandas, significa que VSCode escogió el intérprete equivocado. Haz clic en la esquina superior derecha donde dice "Select Kernel" y elige el de .venv.

## 2.5 Migrar un notebook a .py

El notebook que abriste está bien para exploración. Pero tiene problemas que el mismo notebook documenta al final: código repetido, difícil de reusar, difícil de revisar en Git. Vamos a migrarlo a un .py modular.

### Flujo de migración

1. Identifica las celdas de código (las de Markdown se convierten en comentarios).
1. Detecta bloques que se repiten o que tienen lógica reutilizable — esos se vuelven funciones.
1. Estructura final del .py: imports → funciones → función main() que orquesta → bloque if __name__ == "__main__":

### El archivo analisis_v2.py — versión migrada

En la carpeta de materiales del Módulo 2 tienes analisis_v2.py, que es exactamente la migración del notebook. Cópialo a tu carpeta taller_python y ábrelo en VSCode.

Estructura del archivo:

```python
# 1. Imports al inicio
import pandas as pd

# 2. Funciones (con docstrings que las documentan)
def cargar_datos(ruta_csv):
    """..."""
    ...

def promedio_por_grupo(df, variable, grupo):
    """..."""
    ...

def exportar_a_excel(resultado, ruta_salida, hoja="Resumen"):
    """..."""
    ...

# 3. Funcion main() que orquesta el flujo
def main():
    df = cargar_datos("datos_ejemplo.csv")
    ...
    exportar_a_excel(...)

# 4. Bloque que ejecuta main() solo si corres el archivo directamente
if __name__ == "__main__":
    main()
```

Sobre el bloque `if __name__ == "__main__":` que ves al final: es una convención estándar de Python que quizás te parezca rara la primera vez. Significa: "si me ejecutas directamente con `python analisis_v2.py`, corre main(). Pero si alguien me importa desde otro archivo (`from analisis_v2 import promedio_por_grupo`), no corras main() automáticamente — déjame disponible como librería". Es lo que separa un script de una librería reutilizable, y casi todo .py serio en Python lo tiene.

Ejecuta el archivo:

```powershell
python analisis_v2.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Verás los mismos resultados que en el notebook, pero ahora en un script estructurado, reutilizable y versionable en Git. También se crea resumen.xlsx con el cruzado de ingreso por sexo y área.

### Importar funciones desde otro archivo

La gran ventaja del .py modular: puedes reutilizar sus funciones desde cualquier otro script. Crea un archivo nuevo prueba_import.py:

```python
# prueba_import.py
# Demostracion: importar funciones del analisis_v2.py

from analisis_v2 import cargar_datos, promedio_por_grupo

df = cargar_datos("datos_ejemplo.csv")
print("\nEdad promedio por sexo (calculado importando funciones):")
print(promedio_por_grupo(df, "edad", "sexo"))
```

```powershell
python prueba_import.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Funcionan las funciones importadas. Eso significa que analisis_v2.py ahora sirve a la vez como script ejecutable y como módulo importable. Es la base sobre la que se construyen aplicativos más complejos.

## 2.6 Ejercicio práctico — Extender el script

Modifica analisis_v2.py para agregar nueva funcionalidad. Esto te entrena en la habilidad que más vas a usar en la vida real: leer código que ya existe y extenderlo.

### Reto principal

Agrega una función mediana_por_grupo(df, variable, grupo) con la misma firma que promedio_por_grupo, pero que calcule la mediana en lugar del promedio. Luego:

1. Agrega la nueva función en analisis_v2.py
1. Llámala desde main() para calcular la mediana del ingreso por sexo y área
1. Exporta tanto el promedio como la mediana al MISMO archivo Excel resumen.xlsx pero en dos hojas distintas ("Promedio" y "Mediana")

> [!TIP]
> **💡 Tip**
>
> Para escribir múltiples hojas en un mismo Excel necesitas pd.ExcelWriter. Investiga su uso en la documentación de pandas, o en la carpeta soluciones_retos del material de M2 hay una solución de referencia.

### Validación

Cuando termines, ejecuta tu archivo modificado y verifica:

- Imprime tanto promedio como mediana por sexo y área
- Se crea resumen.xlsx con dos hojas: "Promedio" y "Mediana"
- Las dos hojas contienen las cuatro combinaciones sexo×area

## 2.7 Troubleshooting del Módulo 2

| Síntoma | Causa probable | Solución |
|----|----|----|
| Al abrir el notebook me pide instalar la extensión Jupyter | No instalaste la extensión en el Módulo 0 | Acepta la instalación o ve a la barra de extensiones e instala "Jupyter" de Microsoft |
| ModuleNotFoundError: pandas al ejecutar una celda del notebook | VSCode escogió un kernel (intérprete) que no es el de tu .venv | Haz clic en "Select Kernel" arriba a la derecha y elige el del .venv |
| Mi función no devuelve nada (None) | Olvidaste el return en el cuerpo de la función | Agrega return seguido del valor que quieres devolver |
| ImportError al usar from analisis_v2 import ... | El archivo analisis_v2.py no está en la misma carpeta que el script que lo importa | Verifica con pwd y ls que ambos archivos están en taller_python |
| El script se ejecuta dos veces al importarlo | Olvidaste el bloque if __name__ == "__main__": al final del archivo | Envuelve la llamada a main() dentro de ese bloque |
| IndentationError: expected an indented block | La línea después de def ... : no está indentada con 4 espacios | Python usa la indentación como parte de la sintaxis. Indenta el cuerpo de la función |

## 2.8 Para profundizar (opcional)

Retos opcionales para reforzar funciones y modularidad:

1. Agrega una función conteo_y_porcentaje(df, columna) que devuelva una tabla con el conteo y el porcentaje de cada categoría.
1. Agrega un parámetro opcional decimales (por defecto 0) a promedio_por_grupo, para controlar cuántos decimales muestra.
1. Crea un módulo aparte llamado utilidades.py con tus funciones más usadas e impórtalas desde otros scripts.

Recursos para profundizar:

- Documentación de funciones en Python: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Tutorial de Jupyter en VSCode: https://code.visualstudio.com/docs/datascience/jupyter-notebooks
- Buenas prácticas de docstrings (PEP 257): https://peps.python.org/pep-0257/
