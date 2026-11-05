# Módulo 2 — Pipelines: de la encuesta cruda a los tabulados

Objetivo: convertir el monolito en dos pipelines, preparación y estimación, que corran con un solo comando, lean sus decisiones metodológicas de un archivo de parámetros y se vean en Kedro-Viz. Es el módulo más largo del taller: unas tres horas, repartidas en dos sesiones si hace falta.

### Lo que necesitas antes de empezar

- El proyecto del Módulo 1 con `encuesta_cruda` en el catálogo y la encuesta en `data/01_raw`.
- El entorno activo y la terminal ubicada en la raíz del proyecto, donde está `pyproject.toml`.

## 2.1 Anatomía de un nodo

Un nodo es una función de Python como las que escribiste en el Taller 1, con dos reglas que la hacen apta para un pipeline. Primera: recibe datos por sus argumentos y devuelve datos con `return`. Nunca abre ni guarda archivos. Segunda: no depende de nada que esté fuera de ella, ni variables globales ni estado anterior. Si la llamas dos veces con lo mismo, devuelve lo mismo.

Esas dos reglas tienen una consecuencia práctica enorme: un nodo se puede probar llamándolo con un DataFrame de cinco filas armado a mano. Lo vas a hacer en el Módulo 3.

El primer nodo del proceso es `validar`. Recibe la encuesta cruda y devuelve dos cosas: la encuesta con los tipos correctos y un resumen de lo que encontró. Mira primero la firma y después el cuerpo:

```python
def validar(encuesta: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
```

Un DataFrame entra, y salen un DataFrame y un diccionario. Kedro va a mapear cada salida a un nombre del catálogo. Todavía no escribas nada: primero vamos a crear la carpeta donde este nodo va a vivir.

## 2.2 Crear el pipeline de preparación

Kedro tiene un comando que arma la estructura de un pipeline nuevo:

```powershell
kedro pipeline create preparacion
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Aparecen tres archivos nuevos en `src/encuesta_hogares/pipelines/preparacion/`: `__init__.py`, `nodes.py` y `pipeline.py`. También aparecen `conf/base/parameters_preparacion.yml` y una carpeta `tests/pipelines/preparacion/` con un archivo de prueba vacío.

Esa es la convención que vas a repetir con cada pipeline: los nodos en `nodes.py`, el ensamble en `pipeline.py`, los parámetros en un YAML con el mismo nombre, las pruebas en `tests/`.

Abre `nodes.py`, borra el comentario de plantilla y escribe el nodo de validación:

```python
"""Nodos del pipeline de preparación.

Cada función recibe DataFrames o parámetros y devuelve DataFrames o
diccionarios. Ninguna lee ni escribe archivos: de eso se encarga el catálogo.
"""

import pandas as pd

COLUMNAS = [
    "id_persona",
    "id_hogar",
    "departamento",
    "area",
    "sexo",
    "edad",
    "ocupado",
    "ingreso",
    "factor_expansion",
]


def validar(encuesta: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Verifica columnas, fija los tipos y cuenta nulos.

    Devuelve la encuesta tipada y un resumen con lo encontrado.
    """
    faltan = [c for c in COLUMNAS if c not in encuesta.columns]
    if faltan:
        raise ValueError(f"Faltan columnas obligatorias: {faltan}")

    df = encuesta[COLUMNAS].copy()
    df["id_persona"] = df["id_persona"].astype(int)
    df["id_hogar"] = df["id_hogar"].astype(int)
    df["edad"] = df["edad"].astype(int)
    df["ocupado"] = df["ocupado"].astype("Int64")
    df["ingreso"] = pd.to_numeric(df["ingreso"], errors="coerce")
    df["factor_expansion"] = df["factor_expansion"].astype(float)
    for columna in ["departamento", "area", "sexo"]:
        df[columna] = df[columna].astype(str).str.strip()

    resumen = {
        "n_filas": int(len(df)),
        "columnas": COLUMNAS,
        "n_nulos_por_columna": {c: int(df[c].isna().sum()) for c in COLUMNAS},
    }
    return df, resumen
```

Dos detalles merecen atención. `Int64` con mayúscula es el entero de pandas que admite vacíos, y es la forma de que `ocupado` deje de ser un `float64` con decimales que no significan nada. Y el resumen convierte cada conteo con `int()` porque más adelante lo vamos a guardar como JSON, y JSON no sabe qué hacer con los enteros de numpy.

## 2.3 Ensamblar el pipeline y registrar sus salidas

Abre `pipeline.py` y reemplaza el contenido de plantilla:

```python
"""Ensamble del pipeline de preparación."""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import validar


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=validar,
                inputs="encuesta_cruda",
                outputs=["encuesta_validada", "resumen_validacion"],
                name="validar",
            ),
        ]
    )
```

Lee el `node(...)` como una frase: la función `validar` toma `encuesta_cruda` del catálogo y produce `encuesta_validada` y `resumen_validacion`. Los nombres de `inputs` y `outputs` son nombres de datasets, no de variables de Python. Si existen en el catálogo, Kedro los lee o escribe en disco; si no existen, los mantiene en memoria durante la corrida y los descarta al final.

Queremos que `encuesta_validada` quede en disco. Agrega al catálogo:

```yaml
# --- Capa 02_intermediate: pasos de preparación -----------------------------
encuesta_validada:
  type: pandas.ParquetDataset
  filepath: data/02_intermediate/encuesta_validada.parquet
```

> [!NOTE]
> **📘 Concepto**
>
> ¿Por qué Parquet y no CSV para los pasos intermedios? Porque Parquet guarda los tipos. Si escribieras `encuesta_validada` como CSV, el siguiente nodo la leería con `ocupado` otra vez en `float64` y todo el trabajo del validador se perdería en el camino. Parquet además es más compacto y más rápido. El CSV queda para la entrada, que llega así, y para lo que se publica, que la gente abre en Excel.

Corre el pipeline por primera vez:

```powershell
kedro run
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El registro termina con `Completed 1 out of 1 tasks` y `Pipeline execution completed successfully`. En `data/02_intermediate/` apareció `encuesta_validada.parquet`. No apareció nada para `resumen_validacion`, porque todavía no está en el catálogo: vivió en memoria y se descartó. Lo arreglamos en la sección 2.7.

## 2.4 Parametrizar: `limpiar` y `calibrar`

Los dos nodos que siguen necesitan decisiones metodológicas: el percentil para recortar atípicos, los grupos para imputar y los totales poblacionales para calibrar. En el monolito eran números sueltos. Aquí van a `conf/base/parameters_preparacion.yml`:

```yaml
# Parámetros del pipeline de preparación.
# Son decisiones metodológicas, no datos: por eso viven en conf/ y no en data/.

limpieza:
  # Todo ingreso por encima de este percentil se recorta a ese valor (winsorización)
  percentil_atipicos: 0.99
  # Los ocupados sin ingreso reciben la mediana de su grupo
  grupos_imputacion: ["area", "sexo"]

# Totales poblacionales conocidos por departamento, a los que se calibran
# los factores de expansión (posestratificación simple)
poblacion_objetivo:
  Antioquia: 90000
  Bogota: 110000
  Narino: 35000
  Santander: 55000
  Valle: 70000
```

Ahora los dos nodos, a continuación de `validar` en `nodes.py`:

```python
def limpiar(encuesta: pd.DataFrame, parametros: dict) -> tuple[pd.DataFrame, dict]:
    """Elimina duplicados, recorta atípicos e imputa ingresos faltantes."""
    n_entrada = len(encuesta)
    df = encuesta.drop_duplicates(subset="id_persona").reset_index(drop=True)
    n_duplicados = n_entrada - len(df)

    percentil = df["ingreso"].quantile(parametros["percentil_atipicos"])
    atipicos = df["ingreso"] > percentil
    df.loc[atipicos, "ingreso"] = percentil

    grupos = parametros["grupos_imputacion"]
    df["ingreso_imputado"] = False
    faltantes = (df["ocupado"] == 1) & df["ingreso"].isna()
    mediana = df[df["ocupado"] == 1].groupby(grupos)["ingreso"].transform("median")
    df.loc[faltantes, "ingreso"] = mediana[faltantes]
    df.loc[faltantes, "ingreso_imputado"] = True

    resumen = {
        "n_entrada": int(n_entrada),
        "n_duplicados_eliminados": int(n_duplicados),
        "n_salida": int(len(df)),
        "n_atipicos_ajustados": int(atipicos.sum()),
        "n_imputados": int(faltantes.sum()),
        "metodo": (
            f"atípicos recortados al percentil {parametros['percentil_atipicos']:.0%}; "
            f"imputación por mediana de ocupados según {' x '.join(grupos)}"
        ),
    }
    return df, resumen


def calibrar(encuesta: pd.DataFrame, poblacion_objetivo: dict) -> tuple[pd.DataFrame, dict]:
    """Ajusta los factores de expansión a los totales conocidos por departamento."""
    df = encuesta.copy()
    suma_cruda = df.groupby("departamento")["factor_expansion"].sum()
    razon = {d: poblacion_objetivo[d] / suma_cruda[d] for d in poblacion_objetivo}
    df["factor_calibrado"] = df["factor_expansion"] * df["departamento"].map(razon)

    totales = df.groupby("departamento")["factor_calibrado"].sum().round(2)
    resumen = {
        "razon_de_ajuste": {d: round(float(r), 4) for d, r in razon.items()},
        "totales_calibrados": {d: float(t) for d, t in totales.items()},
        "poblacion_objetivo": {d: float(p) for d, p in poblacion_objetivo.items()},
    }
    return df, resumen
```

Fíjate en que `limpiar` recibe `parametros` como un diccionario cualquiera y `calibrar` recibe `poblacion_objetivo` igual. Las funciones no saben que eso viene de un YAML, y así debe ser.

Ahora el ensamble. En `pipeline.py` amplía la importación y agrega los dos nodos:

```python
from .nodes import calibrar, limpiar, validar
```

```python
            node(
                func=limpiar,
                inputs=["encuesta_validada", "params:limpieza"],
                outputs=["encuesta_limpia", "resumen_limpieza"],
                name="limpiar",
            ),
            node(
                func=calibrar,
                inputs=["encuesta_limpia", "params:poblacion_objetivo"],
                outputs=["encuesta_calibrada", "resumen_calibracion"],
                name="calibrar",
            ),
```

El prefijo `params:` es la forma de pedir un bloque del archivo de parámetros como si fuera un dataset más. `params:limpieza` entrega el diccionario completo que está bajo la clave `limpieza`.

Falta registrar las dos salidas nuevas en el catálogo:

```yaml
encuesta_limpia:
  type: pandas.ParquetDataset
  filepath: data/02_intermediate/encuesta_limpia.parquet

# --- Capa 03_primary: la base lista para estimar ----------------------------
encuesta_calibrada:
  type: pandas.ParquetDataset
  filepath: data/03_primary/encuesta_calibrada.parquet
```

## 2.5 Correr, leer el registro y correr por partes

```powershell
kedro run
```

Lee el registro de arriba abajo. Verás que Kedro carga `encuesta_cruda`, corre `validar`, guarda `encuesta_validada`, la vuelve a cargar para `limpiar`, y así hasta `calibrar`. El orden lo dedujo de las entradas y salidas; tú nunca lo escribiste.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `Completed 3 out of 3 tasks`. En `data/02_intermediate/` están `encuesta_validada.parquet` y `encuesta_limpia.parquet`, y en `data/03_primary/` está `encuesta_calibrada.parquet`.

Ahora prueba lo que el monolito no podía hacer. Correr un solo nodo:

```powershell
kedro run --nodes limpiar
```

Correr desde un punto en adelante, reutilizando lo que ya está en disco:

```powershell
kedro run --from-nodes limpiar
```

Y cambiar un parámetro para una sola corrida, sin tocar el YAML:

```powershell
kedro run --params "limpieza.percentil_atipicos=0.95"
```

> [!TIP]
> **💡 Tip**
>
> `kedro run --help` lista todas las opciones. Las que más vas a usar son `--pipeline`, `--nodes`, `--from-nodes`, `--to-nodes` y `--params`. Con ellas puedes rehacer solo la parte del proceso que cambió, que en una encuesta grande es la diferencia entre dos minutos y dos horas.

## 2.6 Ver el pipeline en Kedro-Viz

```powershell
kedro viz run
```

Se abre el navegador en `http://127.0.0.1:4141` con el grafo del proyecto: los datasets como círculos, los nodos como cuadrados y los parámetros aparte. Haz clic en `limpiar` para ver sus entradas y salidas, y en `encuesta_calibrada` para ver dónde está guardada. Cuando termines, vuelve a la terminal y detén el servidor con Ctrl + C.

> [!NOTE]
> **📘 Concepto**
>
> Este grafo se llama linaje de datos. Responde la pregunta "¿de dónde salió este número?" sin leer código, y es lo primero que un revisor, un auditor o un compañero nuevo quiere ver. Kedro lo dibuja a partir del mismo `pipeline.py` que corre el proceso, así que nunca está desactualizado.

## 2.7 Dataset factories: un patrón para muchos resúmenes

Los tres nodos devuelven un resumen y ninguno llega a disco. Podrías agregar tres entradas al catálogo, una por resumen, pero hay una forma mejor. Agrega esto al final del catálogo:

```yaml
# --- Dataset factory: un patrón que cubre varios datasets -------------------
# Cualquier salida llamada resumen_<algo> se guarda como JSON en 02_intermediate
# sin necesidad de declararla una por una.
"resumen_{etapa}":
  type: json.JSONDataset
  filepath: data/02_intermediate/resumen_{etapa}.json
  save_args:
    indent: 2
    ensure_ascii: false
  fs_args:
    open_args_save:
      encoding: utf-8
```

Las llaves `{etapa}` definen un comodín. Cuando un nodo produce `resumen_limpieza`, Kedro busca una entrada con ese nombre exacto, no la encuentra, prueba los patrones y descubre que `resumen_{etapa}` encaja con `etapa = limpieza`. El archivo queda en `resumen_limpieza.json`.

> [!WARNING]
> **⚠️ Atención**
>
> El bloque `fs_args` no es decorativo. Sin él, en Windows el JSON se escribe con la codificación del sistema y las tildes de "atípicos" o "imputación" quedan corruptas al abrirlo desde otro programa. Es el tipo de detalle que no aparece en los tutoriales porque los escriben en inglés y en Linux.

Corre de nuevo y verifica:

```powershell
kedro run
kedro catalog list-patterns
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> En `data/02_intermediate/` hay tres JSON: `resumen_validacion`, `resumen_limpieza` y `resumen_calibracion`. Abre el de limpieza: dice 15 duplicados eliminados y 27 imputados. `list-patterns` muestra `resumen_{etapa}`.

## 2.8 El pipeline de estimación

Ahora la segunda mitad del proceso. Es más código, pero la mecánica es la misma que acabas de hacer: crear, escribir nodos, ensamblar, registrar, correr.

```powershell
kedro pipeline create estimacion
```

Parámetros, en `conf/base/parameters_estimacion.yml`:

```yaml
# Parámetros del pipeline de estimación.

estimacion:
  # La ocupación solo se pregunta a personas de esta edad en adelante
  edad_minima_ocupacion: 15
  # Nivel de confianza de los intervalos
  nivel_confianza: 0.95

# Clasificación de calidad según el coeficiente de variación (en %)
umbrales_cv:
  buena: 7.5
  aceptable: 15.0
```

Nodos, en `src/encuesta_hogares/pipelines/estimacion/nodes.py`:

```python
"""Nodos del pipeline de estimación."""

import math
from datetime import date

import pandas as pd

DOMINIOS = ["departamento", "sexo", "area"]
CUANTIL_NORMAL = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}


def _estimar_por_grupo(df: pd.DataFrame, variable: str, grupos: list[str], nombre: str) -> pd.DataFrame:
    filas = []
    for claves, g in df.groupby(grupos):
        if not isinstance(claves, tuple):
            claves = (claves,)
        pesos = g["factor_calibrado"]
        fila = {"indicador": nombre}
        fila.update(dict(zip(grupos, (str(c) for c in claves))))
        fila.update(
            {
                "valor": float((g[variable] * pesos).sum() / pesos.sum()),
                "n_muestra": int(len(g)),
                "poblacion_estimada": float(pesos.sum()),
            }
        )
        filas.append(fila)
    return pd.DataFrame(filas)


def estimar_indicadores(encuesta: pd.DataFrame, parametros: dict) -> pd.DataFrame:
    """Tasa de ocupación por departamento y sexo, e ingreso promedio por área.

    Ambos ponderados con el factor calibrado. Devuelve una tabla plana con una
    columna por dominio; las que no aplican quedan vacías.
    """
    edad_minima = parametros["edad_minima_ocupacion"]

    en_edad = encuesta[encuesta["edad"] >= edad_minima].copy()
    en_edad["ocupado"] = en_edad["ocupado"].astype(float)
    tasas = _estimar_por_grupo(en_edad, "ocupado", ["departamento", "sexo"], "tasa_ocupacion")

    ocupados = encuesta[encuesta["ocupado"] == 1].copy()
    ingresos = _estimar_por_grupo(ocupados, "ingreso", ["area"], "ingreso_promedio")

    columnas = ["indicador", *DOMINIOS, "valor", "n_muestra", "poblacion_estimada"]
    return pd.concat([tasas, ingresos], ignore_index=True).reindex(columns=columnas)


def _error_estandar(g: pd.DataFrame, variable: str) -> float:
    pesos = g["factor_calibrado"]
    x = g[variable].astype(float)
    media = (x * pesos).sum() / pesos.sum()
    varianza = (pesos * (x - media) ** 2).sum() / pesos.sum()
    n_efectivo = pesos.sum() ** 2 / (pesos**2).sum()
    return math.sqrt(varianza / n_efectivo)


def calcular_precision(encuesta: pd.DataFrame, indicadores: pd.DataFrame, parametros: dict) -> pd.DataFrame:
    """Error estándar, coeficiente de variación e intervalo de confianza por fila."""
    z = CUANTIL_NORMAL[parametros["nivel_confianza"]]
    edad_minima = parametros["edad_minima_ocupacion"]
    resultado = indicadores.copy()

    errores = []
    for _, fila in indicadores.iterrows():
        if fila["indicador"] == "tasa_ocupacion":
            base, variable = encuesta[encuesta["edad"] >= edad_minima], "ocupado"
        else:
            base, variable = encuesta[encuesta["ocupado"] == 1], "ingreso"
        mascara = pd.Series(True, index=base.index)
        for dominio in DOMINIOS:
            if pd.notna(fila[dominio]):
                mascara &= base[dominio].astype(str) == fila[dominio]
        errores.append(_error_estandar(base[mascara], variable))

    resultado["error_estandar"] = errores
    resultado["cv"] = 100 * resultado["error_estandar"] / resultado["valor"]
    resultado["limite_inferior"] = resultado["valor"] - z * resultado["error_estandar"]
    resultado["limite_superior"] = resultado["valor"] + z * resultado["error_estandar"]
    return resultado


def clasificar_calidad(indicadores: pd.DataFrame, umbrales: dict) -> pd.DataFrame:
    """Etiqueta cada estimación como buena, aceptable o poco confiable según su CV."""

    def etiqueta(cv: float) -> str:
        if cv <= umbrales["buena"]:
            return "buena"
        if cv <= umbrales["aceptable"]:
            return "aceptable"
        return "poco confiable"

    tabulados = indicadores.copy()
    tabulados["calidad"] = tabulados["cv"].apply(etiqueta)
    return tabulados


def generar_metadatos(tabulados: pd.DataFrame, umbrales: dict, parametros: dict) -> dict:
    """Ficha que acompaña a los tabulados publicados."""
    return {
        "titulo": "Tabulados de ocupación e ingreso. Encuesta sintética de hogares",
        "fuente": "Taller 2. Datos ficticios generados con generar_encuesta.py",
        "fecha_proceso": date.today().isoformat(),
        "n_indicadores": int(len(tabulados)),
        "nivel_confianza": parametros["nivel_confianza"],
        "nota_metodologica": (
            "Estimaciones ponderadas con factores calibrados por departamento. "
            f"Calidad según coeficiente de variación: buena (<= {umbrales['buena']} %), "
            f"aceptable (hasta {umbrales['aceptable']} %), poco confiable (mayor)."
        ),
    }
```

Si vienes de la estadística oficial reconoces cada pieza: estimación ponderada por dominio, error estándar con tamaño de muestra efectivo de Kish, coeficiente de variación y clasificación de calidad por umbrales. Lo nuevo no es la estadística sino que cada pieza es una función aparte, con sus decisiones en parámetros.

Ensamble, en `pipeline.py` del mismo pipeline:

```python
"""Ensamble del pipeline de estimación."""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import calcular_precision, clasificar_calidad, estimar_indicadores, generar_metadatos


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=estimar_indicadores,
                inputs=["encuesta_calibrada", "params:estimacion"],
                outputs="indicadores",
                name="estimar_indicadores",
            ),
            node(
                func=calcular_precision,
                inputs=["encuesta_calibrada", "indicadores", "params:estimacion"],
                outputs="indicadores_con_precision",
                name="calcular_precision",
            ),
            node(
                func=clasificar_calidad,
                inputs=["indicadores_con_precision", "params:umbrales_cv"],
                outputs="tabulados",
                name="clasificar_calidad",
            ),
            node(
                func=generar_metadatos,
                inputs=["tabulados", "params:umbrales_cv", "params:estimacion"],
                outputs="metadatos",
                name="generar_metadatos",
            ),
        ]
    )
```

Y las salidas en el catálogo:

```yaml
# --- Capa 07_model_output: resultados numéricos -----------------------------
indicadores:
  type: pandas.CSVDataset
  filepath: data/07_model_output/indicadores.csv
  save_args:
    index: false

indicadores_con_precision:
  type: pandas.CSVDataset
  filepath: data/07_model_output/indicadores_con_precision.csv
  save_args:
    index: false

# --- Capa 08_reporting: lo que se publica -----------------------------------
tabulados:
  type: pandas.ExcelDataset
  filepath: data/08_reporting/tabulados.xlsx
  save_args:
    sheet_name: tabulados
    index: false

metadatos:
  type: json.JSONDataset
  filepath: data/08_reporting/metadatos.json
  save_args:
    indent: 2
    ensure_ascii: false
  fs_args:
    open_args_save:
      encoding: utf-8
```

Antes de correr, mira `pipeline_registry.py`. La función `find_pipelines()` descubre sola los dos pipelines por sus carpetas, y la línea `pipelines["__default__"] = sum(pipelines.values())` los une en el pipeline por defecto. Por eso `kedro run` sin opciones va a correr los siete nodos seguidos, y Kedro va a saber que `estimar_indicadores` necesita `encuesta_calibrada`, que la produce `calibrar`.

```powershell
kedro run
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `Completed 7 out of 7 tasks`. Abre `data/08_reporting/tabulados.xlsx`. Tiene doce filas. La tasa de ocupación de hombres en Antioquia es 0.5724 con un CV de 8.68 % y calidad "aceptable"; el ingreso promedio rural es 1.457.536 con CV de 4.08 % y calidad "buena". Si tus números coinciden, el proceso completo está reproducido.

Vuelve a abrir Kedro-Viz y mira el grafo completo: siete nodos, dos pipelines que puedes filtrar en el panel de la izquierda, y la línea que va de `calibrar` a `estimar_indicadores` uniendo los dos.

## 2.9 Pipelines modulares y namespaces

Imagina que te piden la misma estimación, pero solo para el área rural. La tentación es copiar los cuatro nodos y cambiarles el nombre. Kedro tiene algo mejor: reutilizar el pipeline completo bajo un espacio de nombres, con otra entrada.

Primero un nodo pequeño que filtra, al final de `estimacion/nodes.py`:

```python
def filtrar_area(encuesta: pd.DataFrame, area: str) -> pd.DataFrame:
    """Se queda con las personas de un área (Urbana o Rural)."""
    return encuesta[encuesta["area"] == area].reset_index(drop=True)
```

Un parámetro, al final de `parameters_estimacion.yml`:

```yaml
# Área que usa el pipeline estimacion_rural
area_de_interes: Rural
```

Y ahora el registro. Reemplaza `pipeline_registry.py` completo por esto:

```python
"""Registro de pipelines del proyecto.

Kedro puede descubrir solo los pipelines de src/encuesta_hogares/pipelines/
con find_pipelines(). Aquí se registran a mano porque, además de los dos
pipelines base, se arma una variante (la estimación solo para el área rural)
que no corresponde a ninguna carpeta.
"""

from __future__ import annotations

from kedro.pipeline import Pipeline, node, pipeline

from encuesta_hogares.pipelines import estimacion, preparacion
from encuesta_hogares.pipelines.estimacion.nodes import filtrar_area


def register_pipelines() -> dict[str, Pipeline]:
    pipeline_preparacion = preparacion.create_pipeline()
    pipeline_estimacion = estimacion.create_pipeline()

    # La misma estimación, bajo el espacio de nombres "rural", alimentada con un
    # subconjunto de la base. Los parámetros se comparten con la versión nacional.
    pipeline_rural = pipeline(
        [
            node(
                func=filtrar_area,
                inputs=["encuesta_calibrada", "params:area_de_interes"],
                outputs="encuesta_rural",
                name="filtrar_rural",
            )
        ]
    ) + pipeline(
        pipeline_estimacion,
        namespace="rural",
        inputs={"encuesta_calibrada": "encuesta_rural"},
        parameters={"params:estimacion", "params:umbrales_cv"},
    )

    return {
        "preparacion": pipeline_preparacion,
        "estimacion": pipeline_estimacion,
        "estimacion_rural": pipeline_rural,
        "__default__": pipeline_preparacion + pipeline_estimacion,
    }
```

Lo importante está en la segunda llamada a `pipeline(...)`. Toma el pipeline de estimación entero y le pone el namespace `rural`: todos sus nodos y datasets internos pasan a llamarse `rural.estimar_indicadores`, `rural.tabulados`, etcétera. El argumento `inputs` dice que donde el original esperaba `encuesta_calibrada` ahora entra `encuesta_rural`. Y `parameters` lista los parámetros que se comparten sin prefijo, porque son los mismos para la versión nacional y la rural.

Las salidas con prefijo necesitan a dónde ir. Dos patrones más en el catálogo resuelven todas las variantes que se te ocurran después:

```yaml
# Las salidas de un pipeline con namespace llegan con prefijo: rural.tabulados,
# rural.metadatos. Este patrón las guarda en su propia carpeta.
"{namespace}.tabulados":
  type: pandas.ExcelDataset
  filepath: data/08_reporting/{namespace}/tabulados.xlsx
  save_args:
    sheet_name: tabulados
    index: false

"{namespace}.metadatos":
  type: json.JSONDataset
  filepath: data/08_reporting/{namespace}/metadatos.json
  save_args:
    indent: 2
    ensure_ascii: false
  fs_args:
    open_args_save:
      encoding: utf-8
```

```powershell
kedro registry list
kedro run --pipeline estimacion_rural
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `registry list` muestra cuatro pipelines. La corrida completa cinco tareas y deja `data/08_reporting/rural/tabulados.xlsx` con once filas, porque en el área rural el ingreso promedio urbano no existe. Casi todas las tasas salen "poco confiable": con la cuarta parte de la muestra, la precisión se desploma. Es un resultado correcto y un buen recordatorio de para qué sirve el CV.

> [!WARNING]
> **⚠️ Atención**
>
> Al registrar los pipelines a mano, `find_pipelines()` desaparece. Si en el futuro creas un tercer pipeline con `kedro pipeline create`, tienes que agregarlo tú al diccionario que devuelve `register_pipelines`. Es el precio de tener variantes; a cambio, todo lo que corre está escrito en un solo lugar.

## 2.10 Hooks: engancharse al ciclo de vida de una corrida

Hay cosas que quieres que pasen en cada corrida sin ensuciar los nodos: medir cuánto tardó, registrar cuántas filas produjo cada paso, avisar si algo quedó vacío. Para eso existen los hooks: clases con métodos que Kedro llama en momentos fijos, antes y después de cada nodo o del pipeline entero.

Crea `src/encuesta_hogares/hooks.py`:

```python
"""Hooks del proyecto: código que Kedro ejecuta en momentos fijos de la corrida.

Este hook registra cuántas filas produce cada nodo. No cambia el resultado,
solo observa. Se activa en settings.py con HOOKS = (RegistroDeFilas(),).
"""

import logging
import time

import pandas as pd
from kedro.framework.hooks import hook_impl

logger = logging.getLogger(__name__)


class RegistroDeFilas:
    def __init__(self):
        self._inicio = None

    @hook_impl
    def before_pipeline_run(self, run_params):
        self._inicio = time.perf_counter()
        logger.info("Arranca la corrida del pipeline '%s'", run_params.get("pipeline_name") or "__default__")

    @hook_impl
    def after_node_run(self, node, outputs):
        for nombre, valor in outputs.items():
            if isinstance(valor, pd.DataFrame):
                logger.info("%s -> %s: %d filas, %d columnas", node.name, nombre, len(valor), valor.shape[1])

    @hook_impl
    def after_pipeline_run(self, run_params):
        segundos = time.perf_counter() - self._inicio
        logger.info("Corrida terminada en %.1f segundos", segundos)
```

Los nombres de los métodos no son libres: `before_pipeline_run`, `after_node_run` y `after_pipeline_run` son puntos de enganche que Kedro conoce, y el decorador `@hook_impl` los marca. Actívalo en `settings.py` descomentando y ajustando las dos líneas que Kedro dejó preparadas:

```python
from encuesta_hogares.hooks import RegistroDeFilas

HOOKS = (RegistroDeFilas(),)
```

```powershell
kedro run
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El registro ahora tiene líneas como `validar -> encuesta_validada: 1215 filas, 9 columnas` y `limpiar -> encuesta_limpia: 1200 filas, 10 columnas`, y termina con `Corrida terminada en X segundos`. Esas quince filas de diferencia son los duplicados, y las ves sin abrir un solo archivo.

## 2.11 Runners: secuencial, en hilos, en procesos

Hasta ahora Kedro corrió los nodos uno tras otro con el `SequentialRunner`. Cuando dos nodos no dependen entre sí, se pueden correr a la vez:

```powershell
kedro run --runner ThreadRunner
```

En este proyecto no vas a notar diferencia, porque cada nodo depende del anterior. Sin embargo, en cuanto tengas dos ramas independientes, por ejemplo la estimación nacional y la rural partiendo de la misma base calibrada, el `ThreadRunner` o el `ParallelRunner` las despachan en paralelo sin que cambies una línea de código. Esa es la ventaja de haber declarado las dependencias: Kedro sabe qué puede ir junto.

## 2.12 Ejercicio práctico: un nodo más en la preparación

Agrega al pipeline de preparación un nodo `contar_hogares` que reciba `encuesta_limpia` y devuelva un diccionario con el número de hogares distintos por departamento. Debe llamarse `resumen_hogares` como salida, de manera que el dataset factory de la sección 2.7 lo guarde solo.

Pistas: `groupby("departamento")["id_hogar"].nunique()` hace el conteo, y recuerda convertir cada valor con `int()` antes de devolverlo. Cuando corras `kedro run --pipeline preparacion`, debe aparecer `data/02_intermediate/resumen_hogares.json` y Kedro-Viz debe mostrar el nodo colgando de `encuesta_limpia`.

Guarda la solución: en el Módulo 3 le vas a escribir una prueba.

## 2.13 Troubleshooting del Módulo 2

| Síntoma | Causa probable | Solución |
|----|----|----|
| `ValueError: Pipeline input(s) {'params:limpieza'} not found` | El YAML de parámetros no tiene ese bloque o está mal indentado | Revisa `parameters_preparacion.yml`; el nombre después de `params:` debe ser una clave de primer nivel |
| `KeyError: 'grupos_imputacion'` después de crear un archivo en `conf/local` | Sobreescribiste el bloque `limpieza` con una sola línea | En `conf/local` repite el bloque completo con todos sus valores, o borra el archivo |
| `DatasetError: ... encuesta_validada` no se encuentra, aunque está en el catálogo | Error de indentación en el catálogo, o el `type` escrito distinto | Cada entrada son dos espacios; `pandas.ParquetDataset` con mayúsculas exactas |
| `ImportError: pyarrow` al guardar Parquet | Falta `pyarrow` | `pip install pyarrow` y repite |
| `Pipeline contains no nodes` | `register_pipelines` devolvió un pipeline vacío | Revisa que `create_pipeline` devuelva la lista de nodos y que el registro los incluya |
| `kedro viz run` abre pero el grafo está vacío | Lo corriste desde otra carpeta | Siempre desde la raíz del proyecto |
| Los JSON muestran tildes rotas | Falta el bloque `fs_args` con `encoding: utf-8` | Agrégalo a cada dataset JSON, tal como en la sección 2.7 |
| `An error occurred while importing the ... estimacion_rural module` | Dejaste `find_pipelines()` en el registro junto con la variante | Usa el registro manual completo de la sección 2.9 |

## 2.14 Para profundizar (opcional)

- Versionado de datasets: agregar `versioned: true` a una entrada del catálogo hace que cada corrida guarde una copia con marca de tiempo. Útil para comparar dos publicaciones.
- Tags: cada `node(...)` acepta `tags=["mensual"]`, y `kedro run --tags mensual` corre solo esos. Es la forma de tener subconjuntos del proceso sin crear pipelines nuevos.
- Lee el código del `SequentialRunner` en la documentación. Son pocas líneas y muestran con claridad qué hace Kedro con tu lista de nodos.
