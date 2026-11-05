# Módulo 1 — Del script que creció al proyecto Kedro

Objetivo: entender en carne propia por qué un script deja de alcanzar, crear tu proyecto Kedro, registrar la encuesta en el catálogo y cargarla sin escribir una sola ruta en código. Hora y media.

### Lo que necesitas antes de empezar

- El entorno `.venv-kedro` activo y `kedro --version` respondiendo 1.7.
- La carpeta del material a la mano, en especial `material/datos/encuesta_hogares.csv` y `material/modulo_1/proceso_monolito.py`.

## 1.1 El script que creció

Antes de crear nada, corre el "antes". Desde la carpeta `material/` del taller:

```powershell
python modulo_1/proceso_monolito.py
```

Funciona. Imprime las tasas de ocupación por departamento y sexo, con su coeficiente de variación y su calidad, y guarda un Excel. Ahora ábrelo en VSCode y léelo con calma, porque ese archivo es el retrato de un problema que seguramente ya tienes en tu trabajo.

Fíjate en lo siguiente. La ruta del CSV está escrita a mano en la línea 14, y la de salida en la última. El percentil de recorte, la edad mínima, los totales poblacionales y los umbrales de calidad son números sueltos en medio del código. Los seis pasos van de corrido, de modo que si quieres repetir solo la estimación tienes que volver a cargar y limpiar todo. Y si un compañero quiere probar la calibración con otros totales, tiene que editar tu archivo.

> [!NOTE]
> **📘 Concepto**
>
> Nada de esto es "código mal escrito". Es código que creció sin estructura, que es lo que le pasa a cualquier análisis exitoso. La diferencia entre un script y un proceso no está en la calidad de cada línea sino en cuatro preguntas: ¿de dónde entra cada dato y a dónde sale?, ¿qué valores son decisiones metodológicas que alguien querrá cambiar?, ¿qué pasos dependen de cuáles?, y ¿cómo pruebo uno solo? Kedro obliga a responderlas, y ese es su valor.

## 1.2 Qué resuelve Kedro, en cuatro piezas

Kedro organiza cualquier proyecto de datos alrededor de cuatro ideas. Las vas a ver una y otra vez, así que conviene nombrarlas desde ya.

El **catálogo de datos** es un archivo YAML donde cada conjunto de datos tiene un nombre, un tipo y una ubicación. Tu código nunca más abre un archivo: pide `encuesta_cruda` y Kedro sabe que eso es un CSV en tal ruta.

Un **nodo** es una función de Python normal, con entradas y salidas con nombre. Recibe DataFrames o parámetros, devuelve DataFrames o diccionarios, y no sabe nada de archivos.

Un **pipeline** es una lista de nodos. Kedro mira qué produce cada uno y qué consume el siguiente, y a partir de eso deduce el orden. Tú no escribes "primero validar, después limpiar": lo escribes una vez al declarar entradas y salidas, y el orden sale solo.

Los **parámetros** son otro YAML con los valores que un analista querría cambiar sin tocar código: umbrales, totales, niveles de confianza. Los nodos los reciben como argumentos.

Tal como lo viste en el glosario del Módulo 0, nada de esto es ajeno a lo que ya haces en SAS o en R. Lo nuevo es que queda explícito y en un lugar fijo.

## 1.3 Crear el proyecto

Ve a tu carpeta de proyectos, con el entorno activo, y crea el proyecto:

```powershell
cd C:\Users\tu-usuario\Documentos\proyectos
kedro new --name encuesta_hogares --tools=test,data --example=n
```

Kedro te preguntará si permites enviar estadísticas de uso; responde lo que prefieras. En unos segundos aparece una carpeta nueva.

> [!WARNING]
> **⚠️ Atención**
>
> La carpeta se llama `encuesta-hogares`, con guion, mientras que el paquete de Python de adentro se llama `encuesta_hogares`, con guion bajo. No es un error: los nombres de paquetes de Python no admiten guiones. Vas a ver las dos grafías todo el taller; la carpeta es con guion, el código es con guion bajo.

Las dos opciones que pasamos no son decorativas. `--tools=test,data` le pide a Kedro que prepare la configuración de pytest y la estructura de carpetas de datos. `--example=n` evita que incluya un proyecto de ejemplo: lo vamos a construir nosotros.

Entra a la carpeta y ábrela en VSCode:

```powershell
cd encuesta-hogares
code .
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El explorador de VSCode muestra, como mínimo, las carpetas `conf`, `data`, `notebooks`, `src` y `tests`, y los archivos `pyproject.toml`, `requirements.txt` y `README.md`.

## 1.4 Recorrido por la estructura

Dedica diez minutos a esto. Cada carpeta tiene un propósito, y saber cuál evita que pongas las cosas donde no van.

| Carpeta o archivo | Para qué es | ¿La tocas en el taller? |
|----|----|----|
| `conf/base/` | Configuración compartida: catálogo y parámetros. Va al repositorio | Sí, constantemente |
| `conf/local/` | Configuración de tu máquina: credenciales y sobreescrituras. No va al repositorio | Poco |
| `data/01_raw` a `data/08_reporting` | Datos por capa, de crudo a publicado. No van al repositorio | Solo para copiar la encuesta |
| `src/encuesta_hogares/pipelines/` | Aquí viven los nodos y los pipelines, uno por carpeta | Sí, es el corazón |
| `src/encuesta_hogares/pipeline_registry.py` | Dice qué pipelines existen y cuál corre por defecto | En el Módulo 2 |
| `src/encuesta_hogares/settings.py` | Ajustes del proyecto, como los hooks | En el Módulo 2 |
| `tests/` | Pruebas con pytest | En el Módulo 3 |
| `notebooks/` | Exploración libre con Jupyter | No |
| `pyproject.toml` | Metadatos del proyecto y configuración de herramientas | En el Módulo 3 |
| `requirements.txt` | Dependencias del proyecto | Ahora mismo |

Abre `requirements.txt`. Trae solo `kedro` y algunas cosas de Jupyter. Reemplaza su contenido por la lista real de lo que el proyecto necesita, que es lo mismo que instalaste en el Módulo 0:

```text
kedro~=1.7.0
kedro-viz
kedro-datasets[pandas-csvdataset,pandas-parquetdataset,pandas-exceldataset,json-jsondataset]
pandas
openpyxl
pyarrow
pytest
```

> [!NOTE]
> **📘 Concepto**
>
> Ya lo viste en el Taller 1 y en el Módulo 0 de este: `requirements.txt` existe para que otra persona, o tú en otro computador, instale exactamente lo mismo con `pip install -r requirements.txt`. Kedro genera uno mínimo; mantenerlo completo es responsabilidad tuya.

## 1.5 Las capas de `data/`

Las ocho carpetas numeradas no son un capricho. Representan la madurez del dato, y en un proyecto de estadística oficial casi siempre se usan así:

| Capa | Qué va ahí | En este taller |
|----|----|----|
| `01_raw` | Lo que llega, tal como llega. Nunca se modifica | La encuesta cruda |
| `02_intermediate` | Pasos de preparación: validada, limpia | Las salidas de validar y limpiar, y sus resúmenes |
| `03_primary` | La base lista para análisis, una sola versión de la verdad | La encuesta calibrada |
| `04_feature` y `05_model_input` | Variables derivadas e insumos de modelos | No se usan |
| `06_models` | Modelos entrenados | No se usa |
| `07_model_output` | Resultados numéricos | Los indicadores con su precisión |
| `08_reporting` | Lo que se publica | Los tabulados en Excel y sus metadatos |

Los nombres vienen del mundo de la ciencia de datos y por eso hablan de modelos. No te distraigas con eso: lo que importa es la idea de que un dato avanza de capa en capa y que nunca se escribe hacia atrás.

Copia la encuesta a la primera capa:

```powershell
copy ..\ruta\al\material\datos\encuesta_hogares.csv data\01_raw\
```

Ajusta la ruta al lugar donde descomprimiste el material. En macOS o Linux el comando es `cp`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `dir data\01_raw` muestra `encuesta_hogares.csv` junto al archivo `.gitkeep` que ya estaba.

## 1.6 Registrar la encuesta en el catálogo

Abre `conf/base/catalog.yml`. Está vacío, salvo por comentarios. Escribe esto:

```yaml
# Catálogo de datos del proyecto encuesta_hogares.
#
# Cada entrada es un dataset con nombre. Los nodos reciben y devuelven
# DataFrames; Kedro se encarga de leerlos y escribirlos en la ruta indicada.

# --- Capa 01_raw: lo que llega, tal como llega ------------------------------
encuesta_cruda:
  type: pandas.CSVDataset
  filepath: data/01_raw/encuesta_hogares.csv
```

Tres líneas que valen una explicación. `encuesta_cruda` es el nombre con el que todo el proyecto va a referirse a este dato. `type` dice qué conector lo lee, en este caso el de CSV con pandas, que instalaste con `kedro-datasets`. `filepath` es la ruta relativa a la raíz del proyecto, y es el único lugar del proyecto donde esa ruta va a aparecer.

> [!TIP]
> **💡 Tip**
>
> YAML es sensible a la indentación: dos espacios, nunca tabulaciones. VSCode te marca en rojo la mayoría de los errores de formato. Si algo no carga y no entiendes por qué, lo primero que debes revisar es la indentación del catálogo.

## 1.7 Cargar datos de forma interactiva

Todavía no hay nodos ni pipelines, pero el catálogo ya sirve. Kedro trae una consola interactiva que arranca con el proyecto cargado:

```powershell
kedro ipython
```

Dentro de la consola tienes a la mano una variable `catalog`. Prueba:

```python
catalog.keys()
df = catalog.load("encuesta_cruda")
df.info()
df.head()
```

Mira el `df.info()` con atención: `ocupado` llegó como `float64` porque el CSV no distingue un entero de un vacío. Es uno de los detalles que el nodo de validación va a corregir en el Módulo 2.

Sal de la consola con `exit`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `catalog.keys()` incluye `encuesta_cruda` y `parameters`. `df.info()` reporta 1215 entradas y 9 columnas.

> [!NOTE]
> **📘 Concepto**
>
> Esto que acabas de hacer es la primera ganancia concreta de Kedro: cargaste un archivo sin escribir su ruta. Cuando la encuesta cambie de carpeta, o cuando pase a vivir en una base de datos, cambias una línea del catálogo y todo el proyecto sigue funcionando. En el monolito tendrías que buscar la ruta en el código, y en un proyecto grande eso significa buscarla en veinte archivos.

## 1.8 Configuración por entornos: `conf/base` y `conf/local`

Fíjate en que dentro de `conf/` hay dos carpetas. Todo lo que escribiste va en `conf/base`, que es la configuración compartida y la que se sube al repositorio. `conf/local` es para lo que solo aplica en tu máquina y nunca debería subirse: contraseñas, rutas a discos de red, o valores de prueba que quieres usar sin alterar la configuración oficial. El `.gitignore` que Kedro generó ya la excluye.

Kedro lee primero `base`, después `local`, y lo que encuentra en `local` manda. Abre `conf/local/credentials.yml` para ver el ejemplo que Kedro deja con comentarios: así se declararían las credenciales de una base de datos, y así se referenciarían desde el catálogo sin que queden escritas en él.

> [!WARNING]
> **⚠️ Atención**
>
> La sobreescritura de `local` sobre `base` ocurre por bloque de primer nivel, no valor por valor. Si en el Módulo 2 quieres cambiar en `local` un solo parámetro de un bloque, tienes que copiar el bloque completo con el valor cambiado. Si copias solo la línea, Kedro reemplaza el bloque entero y los demás valores desaparecen. Lo vas a ver en el troubleshooting del Módulo 2 porque es el error más frecuente de todo el taller.

## 1.9 Ejercicio práctico: registrar y guardar un dataset nuevo

El objetivo es que registres un dataset en el catálogo y lo escribas a través de él, sin `to_csv` ni rutas.

Agrega al catálogo una entrada para una muestra de la encuesta:

```yaml
encuesta_muestra:
  type: pandas.CSVDataset
  filepath: data/01_raw/encuesta_muestra.csv
  save_args:
    index: false
```

Después, en `kedro ipython`, carga la encuesta, toma cien filas con `df.sample(100, random_state=1)` y guárdalas con `catalog.save("encuesta_muestra", muestra)`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El archivo `data/01_raw/encuesta_muestra.csv` existe, tiene cien filas y no tiene una columna de índice sin nombre al inicio. Si la tiene, revisa el `save_args`.

Cuando termines, borra el archivo y la entrada del catálogo: no los vamos a necesitar y conviene que el catálogo describa solo lo que el proyecto usa.

## 1.10 Troubleshooting del Módulo 1

| Síntoma | Causa probable | Solución |
|----|----|----|
| `kedro new` dice que ya existe la carpeta | Lo corriste dos veces | Borra `encuesta-hogares` y repite, o entra a la que ya existe |
| `kedro ipython` falla con `No module named IPython` | IPython no está en el entorno | `pip install ipython` con el entorno activo |
| `DatasetError: ... encuesta_cruda not found in the DataCatalog` | Nombre mal escrito o indentación rota en el YAML | Compara contra la sección 1.6 letra por letra |
| `FileNotFoundError` al cargar | El CSV no está en `data/01_raw` o lo corriste desde otra carpeta | Todos los comandos `kedro` van desde la raíz del proyecto, donde está `pyproject.toml` |
| `ImportError` mencionando `pandas.CSVDataset` | `kedro-datasets` sin el extra de pandas | Repite el `pip install` del Módulo 0 con los corchetes completos |

## 1.11 Para profundizar (opcional)

- La sección "Data Catalog" de la documentación de Kedro lista todos los argumentos que acepta cada conector: `load_args`, `save_args`, versionado y credenciales.
- Prueba a registrar la misma encuesta con `type: pandas.ParquetDataset` apuntando a otro archivo y guárdala desde `kedro ipython`. Vas a usar Parquet en el Módulo 2 y conviene que veas la diferencia de tamaño y de tipos frente al CSV.
