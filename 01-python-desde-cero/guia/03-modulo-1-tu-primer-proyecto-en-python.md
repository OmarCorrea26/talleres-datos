# Módulo 1 — Tu primer proyecto en Python

Con Python y VSCode listos, vas a montar tu primer proyecto: una carpeta, un entorno virtual aislado, pandas instalado y un par de scripts corriendo desde la terminal. El flujo que aprendes acá es el que vas a repetir el resto de tu vida con Python — vale la pena entenderlo bien desde el principio.

Calcula entre una hora y hora y media, trabajando con calma.

### Lo que necesitas antes de empezar

Python instalado (Módulo 0), VSCode con la extensión Python (Módulo 0), PowerShell funcionando dentro de VSCode (Ctrl + ñ), y permisos de escritura en alguna carpeta de tu equipo. Importante: no trabajes dentro de C:\Program Files\, ese directorio es problemático.

## 1.1 Conocer la interfaz de VSCode

Cuando abres VSCode encuentras cuatro zonas principales:

| Zona | Ubicación | Para qué sirve |
|----|----|----|
| Barra de actividades | Extrema izquierda, iconos verticales | Cambia entre vistas: archivos, búsqueda, control de versiones, ejecución, extensiones |
| Panel lateral | Segunda columna desde la izquierda | Muestra el contenido de la vista seleccionada (típicamente el explorador de archivos) |
| Editor | Centro | Donde editas tus archivos. Puede mostrar varios en pestañas |
| Panel inferior | Abajo (se abre/cierra) | Contiene la terminal integrada, la consola de salida y los problemas detectados |

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> Si vienes de RStudio: el panel inferior con la terminal cumple el rol de la pestaña Console, pero ojo, en la terminal no escribes Python, escribes comandos del sistema operativo (PowerShell). Para ejecutar Python desde ahí, llamas a python archivo.py.

## 1.2 La terminal integrada y comandos básicos

Para abrir la terminal:

- Atajo: Ctrl + ñ
- O por menú: Ver → Terminal

Por defecto se abre PowerShell. La terminal te permite ejecutar comandos del sistema: navegar carpetas, listar archivos, ejecutar scripts e instalar paquetes.

Comandos de PowerShell que vas a usar en todo el taller:

| Comando | Qué hace |
|----|----|
| `pwd` | Muestra la ruta de la carpeta actual |
| `ls` | Lista los archivos de la carpeta actual |
| `cd nombre_carpeta` | Entra a una subcarpeta |
| `cd ..` | Sube un nivel |
| `mkdir nombre` | Crea una carpeta nueva |
| `python archivo.py` | Ejecuta un script de Python |
| `pip install paquete` | Instala un paquete de Python en el entorno activo |
| `pip list` | Muestra los paquetes instalados |

> [!TIP]
> **💡 Tip**
>
> PowerShell distingue entre rutas con espacios. Si tu carpeta se llama "mis documentos" (con espacio), debes envolverla en comillas: cd "mis documentos". La buena práctica es no usar espacios en nombres de carpetas de proyectos.

## 1.3 Crear una carpeta para tu proyecto

Usando el Explorador de Windows, navega a una ubicación cómoda (por ejemplo C:\Users\TuUsuario\Documentos\) y crea una carpeta llamada:

```text
taller_python
```

En VSCode: Archivo → Abrir carpeta → seleccionar taller_python.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> En la barra lateral izquierda, vista "Explorador", debes ver el nombre TALLER_PYTHON con la carpeta vacía debajo.

> [!WARNING]
> **⚠️ Atención**
>
> No uses espacios, tildes ni la letra ñ en el nombre de la carpeta. Aunque Python y Windows los aceptan, generan problemas inesperados con algunas herramientas (incluyendo Git en el Módulo 3). Usa snake_case (palabras_separadas_por_guion_bajo).

## 1.4 ¿Qué es un entorno virtual y por qué lo necesitas?

Un entorno virtual es una instalación aislada de Python con sus propios paquetes, atada solo al proyecto donde lo creaste. No afecta a otros proyectos ni a la instalación general de Python.

La analogía que sirve: cada proyecto Python es como una cocina. Cada cocina tiene sus propios ingredientes (paquetes) y herramientas (versión de Python). Si todas las cocinas compartieran los mismos ingredientes, cambiar uno podría dañar las recetas de las otras. Un entorno virtual mantiene cada cocina independiente, y te permite que un proyecto use pandas 2.1 y otro pandas 1.5 sin que choquen.

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> SAS no tiene un equivalente nativo: todo lo que instalas queda global. R sí lo tiene a través del paquete renv. Si usaste renv::init() en R, .venv es exactamente el primo de Python. Su existencia es señal de un proyecto bien organizado, no un capricho técnico.

Reglas de oro:

- Un entorno virtual por proyecto
- Nunca se sube a GitHub (lo verás en el Módulo 3)
- Se crea con un comando, se activa cada vez que vas a trabajar

## 1.5 Crear tu primer entorno virtual

Con la terminal abierta y la carpeta taller_python como contexto, primero verifica:

```text
pwd
```

La ruta que devuelve debe terminar en \taller_python. Si no, navega con cd hasta la ubicación correcta.

Crear el entorno:

```powershell
python -m venv .venv
```

> [!TIP]
> **💡 Tip**
>
> El comando se lee así: "Python, ejecuta el módulo venv (que viene incluido) y crea un entorno llamado .venv". El punto al inicio del nombre lo marca como oculto en sistemas Unix y se conserva por convención. Otros nombres válidos serían env o venv, pero .venv es el estándar más usado.

Esto tarda algunos segundos. Cuando termine, el prompt regresa sin mostrar mensajes adicionales.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> En el panel Explorador de VSCode aparece una nueva carpeta .venv dentro de tu proyecto. Contiene la instalación aislada de Python y los paquetes que vayas instalando. Nunca edites nada adentro de esa carpeta.

## 1.6 Activar el entorno virtual

Crear el entorno no es suficiente: hay que activarlo para que los comandos python y pip operen dentro de él, no en la instalación general.

En PowerShell:

```powershell
.venv\Scripts\activate
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El prompt cambia y muestra (.venv) al inicio. Por ejemplo: (.venv) PS C:\Users\TuUsuario\Documentos\taller_python>

> [!WARNING]
> **⚠️ Atención**
>
> Si recibes un error del tipo "no se puede cargar el archivo Activate.ps1 porque la ejecución de scripts está deshabilitada en este sistema", PowerShell tiene una política de seguridad activa que bloquea scripts. Solución (ejecutar UNA sola vez):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Confirmar con Y y la tecla Enter. Luego repite la activación.

Para desactivar el entorno cuando termines de trabajar:

```powershell
deactivate
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El entorno está activo si ves (.venv) al inicio del prompt. Cada vez que abras VSCode y vayas a trabajar en este proyecto, tendrás que repetir el comando de activación. Sin activarlo, los paquetes que instalaste no estarán disponibles.

## 1.7 Instalar paquetes con pip

pip es el gestor de paquetes de Python, equivalente a install.packages() en R.

Con el entorno activo (debes ver (.venv) en el prompt), instala los dos primeros paquetes:

```powershell
pip install pandas openpyxl
```

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> Equivale a install.packages(c("dplyr", "readxl")) en R, aunque pandas es más amplio que dplyr: combina la funcionalidad de dplyr, tidyr y readr en un solo paquete. openpyxl es el lector/escritor de archivos Excel (.xlsx).

Verás varias líneas mientras pip descarga e instala los paquetes (incluye también sus dependencias automáticamente). Al final:

```text
Successfully installed pandas-2.x.x openpyxl-3.x.x numpy-1.x.x ...
```

Para ver lo instalado:

```powershell
pip list
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver pandas y openpyxl en la lista, junto con paquetes auxiliares como numpy, python-dateutil y pytz que se instalaron automáticamente.

## 1.8 Tu primer script .py

En VSCode, en el panel Explorador, haz clic derecho sobre el nombre de tu proyecto y elige "New File". Nómbralo:

```text
hola.py
```

En el editor central, escribe el siguiente contenido:

```python
# hola.py
# Mi primer script en Python

print("Hola, mundo!")
print("Estoy aprendiendo Python.")

# Una operacion simple
x = 5
y = 3
suma = x + y
print(f"La suma de {x} y {y} es {suma}")
```

Guarda el archivo con Ctrl + S.

### Línea por línea

| Elemento | Significado | Equivalente en SAS / R |
|----|----|----|
| `# texto` | Comentario. Python lo ignora | `* texto;  en SAS  \|  # texto  en R` |
| `print("x")` | Imprime en pantalla | `put 'x';  en SAS  \|  print("x")  en R` |
| `x = 5` | Crea una variable | `x = 5;  dentro de DATA step  \|  x <- 5  en R` |
| `f"texto {var}"` | f-string: inserta el valor de una variable | `cats(...)  o  paste0(...)  en R` |

## 1.9 Ejecutar el script desde la terminal

En la terminal, con (.venv) activo:

```powershell
python hola.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver exactamente esta salida: Hola, mundo! Estoy aprendiendo Python. La suma de 5 y 3 es 8

Felicitaciones: acabas de ejecutar tu primer script en Python. Este es el flujo profesional que vas a usar para correr cualquier programa Python en el futuro.

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> En SAS abres SAS Studio y le das Run al programa. En R abres RStudio y haces Run script. En Python — al menos en su forma más profesional — escribes python archivo.py en la terminal. Existen otras formas (correr celda por celda en VSCode, usar Jupyter), pero entender este flujo desde el inicio te ahorra problemas más adelante.

## 1.10 Ejercicio práctico — Generar y analizar un CSV

Para no depender de un archivo externo, vamos a generar nuestros propios datos sintéticos y luego cargarlos. El ejercicio tiene dos partes.

### Parte 1 — Generar el archivo de datos

Crear un nuevo archivo en VSCode llamado generar_datos.py con este contenido:

```python
# generar_datos.py
# Crea un CSV sintetico con 100 personas para los ejercicios del taller

import pandas as pd
import numpy as np

# Semilla para reproducibilidad: los numeros aleatorios saldran iguales cada vez
np.random.seed(42)

n = 100

datos = pd.DataFrame({
    "id": range(1, n + 1),
    "edad": np.random.randint(18, 75, size=n),
    "sexo": np.random.choice(["H", "M"], size=n),
    "ingreso": np.random.randint(500000, 5000000, size=n),
    "area": np.random.choice(["Urbana", "Rural"], size=n, p=[0.7, 0.3]),
})

datos.to_csv("datos_ejemplo.csv", index=False)
print(f"Archivo creado con {len(datos)} filas")
```

Ejecutar:

```powershell
python generar_datos.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver: Archivo creado con 100 filas. En el panel Explorador aparece el archivo datos_ejemplo.csv junto a los .py.

> [!TIP]
> **💡 Tip**
>
> Puedes hacer clic sobre datos_ejemplo.csv en VSCode para abrirlo y ver el contenido. Verás cinco columnas: id, edad, sexo, ingreso, area, separadas por comas.

### Parte 2 — Cargar y analizar

Crear un nuevo archivo analisis.py:

```python
# analisis.py
# Carga el CSV y hace un analisis estadistico basico

import pandas as pd

# Cargar el archivo
df = pd.read_csv("datos_ejemplo.csv")

# 1. Primeras 5 filas
print("Primeras 5 filas:")
print(df.head())
print()

# 2. Resumen estadistico de las variables numericas
print("Resumen estadistico:")
print(df.describe())
print()

# 3. Conteo de personas por sexo
print("Conteo por sexo:")
print(df["sexo"].value_counts())
print()

# 4. Promedio de ingreso por sexo
print("Promedio de ingreso por sexo:")
print(df.groupby("sexo")["ingreso"].mean().round(0))
print()

# 5. Promedio de ingreso por sexo y area
print("Promedio de ingreso por sexo y area:")
print(df.groupby(["sexo", "area"])["ingreso"].mean().round(0))
```

Ejecutar:

```powershell
python analisis.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver cinco bloques de salida: las primeras filas, el resumen estadístico, el conteo por sexo, el promedio de ingreso por sexo y el promedio cruzado por sexo y área.

Detente un segundo aquí: acabas de hacer un análisis estadístico completo. Cargaste datos, los exploraste, los resumiste, los agrupaste por dos variables, todo en un archivo de unas 25 líneas. En SAS necesitarías tres PROCs separados con sus respectivas RUN. En R serían unas líneas con dplyr. La gran diferencia es que ahora tienes un archivo que puedes correr cuantas veces quieras con resultado idéntico, y que cualquier otra persona (o tú mismo en seis meses) puede leer y entender. Esa reproducibilidad es la razón principal por la que el análisis serio se hace en scripts y no en interfaces de clic.

## 1.11 Troubleshooting del Módulo 1

| Síntoma | Causa probable | Solución |
|----|----|----|
| No se puede cargar el archivo Activate.ps1 porque la ejecución de scripts está deshabilitada | Política de seguridad de PowerShell | Ejecutar: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned. Confirmar con Y. |
| El prompt no muestra (.venv) después de activar | El comando se ejecutó en otra carpeta, o se usó .venv/Scripts/activate (con / en vez de \) | Verificar con pwd que estás en taller_python. En PowerShell usar barra invertida: .venv\Scripts\activate |
| ModuleNotFoundError: No module named 'pandas' | El entorno virtual no está activo, o pandas se instaló en otro entorno | Verifica que veas (.venv) en el prompt. Ejecuta pip list para confirmar que pandas aparece. |
| FileNotFoundError: 'datos_ejemplo.csv' | El script se ejecuta desde otra carpeta, o el CSV no se generó | Ejecutar pwd  y  ls  para confirmar que estás en taller_python y que el CSV existe. Si no existe, correr de nuevo generar_datos.py |
| SyntaxError: invalid syntax al ejecutar el script | Error de escritura: comilla mal cerrada, falta dos puntos, indentación incorrecta | Lee con cuidado la línea que el error indica (Python siempre la señala). Compara con el código de la guía. |
| El script corre pero no imprime nada | Te falta llamar a print() en cada resultado, o el script terminó por una excepción silenciosa | Verifica que cada línea de salida tenga print(...)  envolviendo la expresión |
| VSCode abre el archivo .py con otra aplicación | Asociación de archivos en Windows apuntando a otro programa | Clic derecho sobre el .py → Abrir con → Elegir otra aplicación → Visual Studio Code → marcar "Usar siempre" |

## 1.12 Para profundizar (opcional)

Si terminaste cómodo y quieres reforzar antes de continuar al Módulo 2, prueba estos retos sobre analisis.py:

1. Modifica el script para agrupar por area en lugar de por sexo. ¿Cuál tiene mayor ingreso promedio, Urbana o Rural?
1. Cambia .mean() por .median() para calcular la mediana en lugar del promedio. Compara los dos resultados.
1. Calcula la edad promedio por sexo agregando una línea similar a las del script.
1. Exporta el resultado del groupby a un archivo Excel usando .to_excel("resumen.xlsx"). Pista: primero guarda el resultado en una variable, luego llama .to_excel.

Recursos para profundizar por tu cuenta:

- Documentación oficial de pandas: https://pandas.pydata.org/docs/
- Tutorial interactivo gratuito: https://www.learnpython.org/
- Cheat sheet de pandas para usuarios de R: buscar "pandas vs R" en su documentación
- Curso introductorio en español: "Python para análisis de datos" en datacamp.com / freecodecamp.org

## Cierre del Módulo 1

Antes de avanzar al Módulo 2, revisa que tienes funcionando: la carpeta taller_python con un entorno virtual .venv adentro; pandas y openpyxl instalados en ese entorno (verifica con pip list); los tres scripts hola.py, generar_datos.py y analisis.py creados; el archivo datos_ejemplo.csv generado; y los tres scripts ejecutándose sin errores con python archivo.py.

Si todo eso funciona, estás listo. En el Módulo 2 vas a aprender a estructurar el código en funciones reutilizables y a migrar un notebook Jupyter completo a un script organizado y mantenible.
