# Módulo 2 — Tu etapa del proceso

Objetivo: implementar la etapa que te corresponde de modo que cumpla el contrato en tu máquina: `probar` en OK, `pytest` en verde y tu parte del muñeco derecha. Entre tres y cinco horas según la etapa; no se hace de una sentada.

### Lo que necesitas antes de empezar

- Módulos 0 y 1 completados.
- Saber qué etapa te corresponde.
- Manejo básico de pandas: `groupby`, `merge`, filtros booleanos, `fillna`, `drop_duplicates` (Taller 1).

## 2.1 La encuesta y sus problemas deliberados

`datos/encuesta_hogares.csv` tiene 1.215 filas y nueve columnas. Ábrelo con pandas y mira las primeras filas antes de seguir; nunca proceses datos que no has visto.

| Columna | Tipo | Descripción |
|----|----|----|
| `id_persona` | entero | Identificador único de la persona. Es la llave |
| `id_hogar` | entero | Hogar al que pertenece |
| `departamento` | texto | Uno de: Antioquia, Bogota, Narino, Santander, Valle (sin tildes, a propósito) |
| `area` | texto | Urbana o Rural |
| `sexo` | texto | H o M |
| `edad` | entero | 0 a 89 |
| `ocupado` | entero o nulo | 1 ocupado, 0 no ocupado. **Nulo para menores de 15**: a ellos no se les pregunta |
| `ingreso` | decimal o nulo | Ingreso mensual en pesos. Nulo para no ocupados y menores. **También nulo en algunos ocupados**: esa es la no respuesta |
| `factor_expansion` | decimal | Factor de expansión crudo, sin calibrar |

El generador introduce a propósito tres problemas, porque son los que aparecen en cualquier operación estadística real:

- **15 filas duplicadas exactas** (mismo `id_persona`), como cuando un formulario se transmite dos veces.
- **6 ingresos con un cero de más** (errores de digitación), que disparan cualquier promedio.
- **28 ocupados sin ingreso** (no respuesta parcial), que hay que imputar antes de estimar.

Los factores de expansión no suman la población conocida de cada departamento: hay que calibrarlos. Y por diseño, la proporción de ocupados es distinta entre hombres y mujeres, así que la tasa de ocupación por sexo tiene algo que mostrar.

> [!TIP]
> **💡 Tip**
>
> Explora en un notebook antes de escribir código en `app.py`. `pd.read_csv("datos/encuesta_hogares.csv")`, `df.info()`, `df.describe()`, `df.duplicated().sum()`, `df[df.ocupado == 1].ingreso.isna().sum()`. Diez minutos de exploración te evitan una hora de depuración.

## 2.2 Cómo leer el contrato

Antes de escribir una línea de tu etapa, lee tres archivos. En este orden.

### contrato/esquemas.py — la forma

Busca `EntradaN` y `SalidaN` para tu número. Cada uno es un modelo Pydantic; sigue la herencia hacia arriba para ver los campos. Por ejemplo, para la etapa 3: `Entrada3 = Salida2`, que tiene `registros: list[RegistroLimpio]` y `resumen: ResumenLimpieza`; y `Salida3` tiene `registros: list[RegistroCalibrado]` (un `RegistroLimpio` más `factor_calibrado`) y `resumen: ResumenCalibracion`.

> [!WARNING]
> **⚠️ Atención**
>
> Los modelos tienen `extra="forbid"`. Si devuelves un campo que no está declarado (por ejemplo dejas una columna auxiliar `_tmp` en los registros), la validación de estructura falla y tu parte sale chueca. El error dirá `Extra inputs are not permitted`.

### contrato/validaciones.py — las reglas

Busca `validar_etapa_N`. Ahí está, en código legible, cada regla que el ensamblador aplica a tu salida y el mensaje exacto que te va a mostrar si falla. Léela como una lista de requisitos: cada `errores.append(...)` es una condición que tu etapa debe cumplir. Algunas comparan contra la salida de referencia con tolerancia; eso significa que no tienes que obtener el mismo decimal, pero sí el mismo método.

### fixtures/etapa_N_entrada.json y etapa_N_salida.json — los datos

La entrada es lo que tu servicio va a recibir en las pruebas. La salida es una solución de referencia: no para copiarla, sino para entender la forma del resultado y verificar tus cifras con tolerancia. Ábrelos con un visor de JSON en VSCode (clic derecho, "Format Document") o desde Python:

```python
import json
with open("fixtures/etapa_3_entrada.json", encoding="utf-8") as f:
    entrada = json.load(f)
print(entrada.keys())
print(entrada["resumen"])
print(entrada["registros"][0])
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Puedes decir, para tu etapa, con tus palabras: qué llaves tiene el JSON de entrada, qué llaves debe tener el de salida, y cuáles son las tres reglas de validación que más probablemente te fallen.

## 2.3 El ciclo de trabajo de una etapa

Todo el módulo se reduce a repetir este ciclo hasta que salga OK:

1. Editar `etapas/etapa_N_nombre/app.py`: escribir la función `procesar`.
1. Terminal 1: levantar el servicio con `uvicorn etapas.etapa_N_nombre.app:app --port 800N --reload`.
1. Terminal 2: probar con `python -m ensamblador.probar --etapa N`. Leer los errores. Volver al paso 1.
1. Cuando salga `[OK]`: correr `pytest -k etapa_N` para confirmar que la prueba automática también pasa.
1. Opcional: levantar el ensamblador en una tercera terminal (`uvicorn ensamblador.app:app --port 8000`) y ver tu parte del muñeco en verde.

Empieza ahora mismo con el esqueleto tal cual está, sin cambiarlo, para ver cómo se ve cada mensaje:

```powershell
uvicorn etapas.etapa_3_calibrar.app:app --port 8003 --reload
```

Y en otra terminal (con el entorno activado):

```powershell
python -m ensamblador.probar --etapa 3
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `[AUSENTE] Etapa 3 (calibrar, brazo_izquierdo) en http://localhost:8003` con el detalle "El servicio corre pero procesar() aun lanza NotImplementedError". Ya sabes qué se siente el estado ausente. Ahora reemplaza el `raise` por `return {}` y vuelve a probar: `[CHUECO]` con errores de estructura. Ese es el estado chueco. Todo lo que sigue es pasar de ahí a `[OK]`.

> [!TIP]
> **💡 Tip**
>
> Usa la terminal integrada de VSCode dividida en dos (icono "Split Terminal" o `Ctrl + Shift + 5`). Izquierda uvicorn, derecha probar. Con `--reload`, cada vez que guardas, la izquierda reinicia y solo tienes que repetir el comando de la derecha (flecha arriba, Enter).

## 2.4 De JSON a pandas y de vuelta: las trampas

Tu función recibe un diccionario y debe devolver un diccionario. Casi siempre querrás pasar por un DataFrame en el medio. El patrón general es:

```python
import pandas as pd

def procesar(entrada: dict) -> dict:
    df = pd.DataFrame(entrada["registros"])      # JSON -> DataFrame

    # ... aquí tu trabajo estadístico ...

    registros = df.astype(object).where(df.notna(), None).to_dict(orient="records")
    resumen = {...}                              # lo que pida tu SalidaN
    return {"registros": registros, "resumen": resumen}
```

La línea de vuelta es fea a propósito; cada pieza evita una trampa concreta:

| Trampa | Qué pasa si la ignoras | Cómo se evita |
|----|----|----|
| `NaN` no existe en JSON | `to_dict` deja `float('nan')`; al serializar aparece `NaN` sin comillas, que no es JSON válido, o Pydantic rechaza el campo | `.astype(object).where(df.notna(), None)` convierte todo nulo a `None`, que sí es `null` en JSON |
| Enteros con nulos se vuelven `float` | Una columna `ocupado` con nulos pasa a `1.0`/`0.0`; el esquema pide `int` | Usa el tipo nullable de pandas: `df["ocupado"] = df["ocupado"].astype("Int64")` antes de exportar |
| Tipos de numpy no son tipos de Python | `np.int64(5)` o `np.float64(0.5)` fallan al serializar | Envuelve con `int(...)` y `float(...)` cualquier escalar que pongas en `resumen`; el `astype(object)` de arriba resuelve las columnas |
| Columnas de más | Dejas una columna auxiliar y `extra="forbid"` la rechaza | Elimina auxiliares con `df.drop(columns=[...])` antes de exportar |
| Orden y nombres de columnas | La etapa 1 debe reportar `columnas` en el orden exacto del contrato | No dependas de `df.columns`; usa la lista del contrato |
| Claves de `groupby` no son texto | Si agrupas por una columna numérica, la llave sale como `int`; el esquema de `desagregacion` pide `str` | `str(v)` al construir cada diccionario |

> [!WARNING]
> **⚠️ Atención**
>
> No modifiques la entrada in place y la devuelvas "tal cual" pensando que ahorras trabajo. Las etapas 3 y 4 deben devolver **todos** los registros que reciben, pero con columnas adicionales. Y las etapas 5 y 6 deben devolver solo indicadores, sin registros. Léelo en el esquema, no lo adivines.

## 2.5 Fichas de las seis etapas

Cada ficha dice qué recibes, qué devuelves, las reglas que más fallan y una pista técnica. No es la solución: es el enunciado bien delimitado. La decisión de cómo resolverlo es tuya y debes poder defenderla en la revisión de código.

### Etapa 1 — validar (cabeza, puerto 8001)

|  |  |
|----|----|
| Recibes | `{"registros": [...]}` con las filas crudas del CSV. Pueden venir nulos en `ocupado` e `ingreso` y algún tipo mal inferido |
| Devuelves | `{"registros": [...], "resumen": {"n_filas", "columnas", "n_nulos_por_columna"}}` con tipos garantizados según `RegistroValidado` |
| Reglas clave | No eliminas filas (eso es la etapa 2). `columnas` es exactamente la lista de nueve nombres en su orden. Ningún mayor de 15 puede quedar sin `ocupado`. Departamento, sexo y área dentro de catálogo |
| Pista | Tipa columna por columna: `astype(int)` para llaves y edad, `astype("Int64")` para `ocupado`, `pd.to_numeric(..., errors="coerce")` para ingreso. Si faltara una columna obligatoria, lanza `ValueError` con un mensaje claro: un 500 con buen mensaje vale más que un 200 mentiroso |

Esta etapa parece la más simple y por eso es traicionera: es la que **define** los tipos con los que trabajan todas las demás. Un `ocupado` que sale como decimal aquí es un error en la etapa 4.

### Etapa 2 — limpiar (torso, puerto 8002)

|  |  |
|----|----|
| Recibes | La salida de la etapa 1 |
| Devuelves | `registros` sin duplicados y con la columna nueva `ingreso_imputado` (booleano), más `resumen` con `n_entrada`, `n_duplicados_eliminados`, `n_salida`, `n_imputados`, `n_atipicos_ajustados` y `metodo_imputacion` (texto que documenta lo que hiciste) |
| Reglas clave | Los duplicados se detectan por `id_persona`; el validador calcula cuántos hay y espera ese número exacto. Ningún ocupado puede quedar sin ingreso. `n_imputados` debe coincidir con la cuenta de `ingreso_imputado == True`. Después del tratamiento no puede quedar un ingreso mayor a 20 millones |
| Decisiones tuyas | El método de imputación (mediana por grupo, media, hot-deck) y el tratamiento de atípicos (recorte a un percentil, eliminación marcada, regla de rango intercuartílico). Documéntalo en `metodo_imputacion` y en comentarios |
| Pista | `drop_duplicates(subset="id_persona")`. Para imputar por grupo, `groupby([...])["ingreso"].transform("median")` te da una serie alineada con el DataFrame. Trata los atípicos **antes** de calcular medianas para imputar, o los atípicos contaminan la imputación |

### Etapa 3 — calibrar (brazo izquierdo, puerto 8003)

|  |  |
|----|----|
| Recibes | La salida de la etapa 2 |
| Devuelves | `registros` con la columna nueva `factor_calibrado`, y `resumen` con `totales_por_departamento` (suma del factor calibrado por departamento) y `poblacion_objetivo` (copia de `contrato/poblacion_objetivo.json`) |
| Reglas clave | Para cada departamento, la suma de `factor_calibrado` debe coincidir con la población objetivo con una tolerancia del 0,5 %. No cambia el número de registros. Todo factor calibrado es positivo |
| Concepto | Esto es **posestratificación**: la forma más simple de calibración. Para cada departamento se calcula la razón entre la población conocida y la suma de los factores crudos, y se multiplica el factor de cada persona por esa razón. Con un solo criterio de calibración es una división; con varios (departamento y sexo, por ejemplo) necesitarías raking o calibración lineal, que es lo que hacen paquetes como `survey` en R |
| Pista | `df.groupby("departamento")["factor_expansion"].sum()` te da la suma cruda; construye un diccionario de razones y aplícalo con `df["departamento"].map(razones)`. Lee el JSON de población desde la ruta del repositorio, no desde una ruta absoluta de tu máquina |

### Etapa 4 — indicadores (brazo derecho, puerto 8004)

|  |  |
|----|----|
| Recibes | La salida de la etapa 3 |
| Devuelves | `registros` **intactos** (la etapa 5 los necesita) e `indicadores`: una lista de doce estimaciones, cada una con `indicador`, `desagregacion`, `valor`, `n_muestra` y `poblacion_estimada` |
| Definiciones | **Tasa de ocupación**: ocupados sobre población de 15 años o más, ponderada por `factor_calibrado`, por departamento y sexo (10 dominios). **Ingreso promedio**: media ponderada del ingreso de los ocupados, por área (2 dominios) |
| Reglas clave | Tasas entre 0 y 1 (proporción, no porcentaje). Exactamente 10 + 2 dominios. Los valores se comparan con la referencia: tasas con tolerancia de 1 punto porcentual, ingresos con 2 % relativo. `n_muestra` es el número de personas en el dominio; `poblacion_estimada` es la suma de sus factores |
| Pista | Filtra primero la población de referencia (edad ≥ 15 para la tasa; ocupados para el ingreso), luego agrupa. Una media ponderada es `(x * w).sum() / w.sum()`. Las llaves de `desagregacion` son los nombres de columna (`departamento`, `sexo`, `area`) y los valores deben ser texto |

### Etapa 5 — precision (pierna izquierda, puerto 8005)

|  |  |
|----|----|
| Recibes | La salida de la etapa 4 (registros e indicadores) |
| Devuelves | Solo `indicadores`, cada uno con los campos originales más `error_estandar`, `cv` (en **porcentaje**), `limite_inferior` y `limite_superior` |
| Método | Aproximación por **tamaño de muestra efectivo** (Kish): para cada dominio, varianza ponderada de la variable, dividida por n_ef = (Σw)² / Σw². Error estándar = raíz de eso. CV = 100 · EE / valor. Intervalo al 95 %: valor ± 1,96 · EE. Es una aproximación que ignora la estructura de diseño (conglomerados, estratos); en producción se usa linealización de Taylor o replicación. Aquí basta para el propósito |
| Reglas clave | Mismo número de indicadores que entraron. El valor queda dentro de su intervalo. `cv` debe ser consistente con `error_estandar` y `valor` (el validador lo recalcula). Se compara con la referencia con 20 % de tolerancia relativa en el CV |
| Pista | Para cada indicador, reconstruye el subconjunto de registros del dominio: filtra por edad u ocupación según el indicador y luego por cada par de `desagregacion`. Compara los valores de `desagregacion` como texto: `df[k].astype(str) == v` |

### Etapa 6 — publicar (pierna derecha, puerto 8006)

|  |  |
|----|----|
| Recibes | La salida de la etapa 5 |
| Devuelves | `metadatos` (`titulo`, `fuente`, `fecha_proceso` en ISO, `n_indicadores`, `nota_metodologica`), `tabulados` (cada indicador más el campo `calidad`) y `archivo_excel` (ruta relativa del `.xlsx` que escribes en `salida/`) |
| Reglas clave | `calidad` sigue los umbrales del contrato: CV ≤ 7,5 % buena; ≤ 15 % aceptable; mayor, poco confiable. Usa la función `clasificar_calidad` de `contrato/validaciones.py`, no reescribas los umbrales. La nota metodológica tiene al menos 40 caracteres y explica cómo se clasificó. `fecha_proceso` con `date.today().isoformat()` |
| Pista | Para Excel, aplana `desagregacion` en columnas (`departamento`, `sexo`, `area`) antes de `to_excel`. Crea `salida/` si no existe con `Path(...).mkdir(exist_ok=True)`. La ruta que devuelves es relativa al repositorio y con barras `/`, no la ruta absoluta de tu disco |

> [!NOTE]
> **📘 Concepto**
>
> Los umbrales de CV son una convención pedagógica inspirada en la práctica de difusión de estadísticas oficiales, donde las estimaciones con coeficiente de variación alto se marcan o se suprimen. El punto no es el número exacto sino la práctica: **publicar una cifra sin su precisión es publicar media cifra.**

## 2.6 Ejemplo guiado: el esqueleto de una etapa bien escrita

Para que veas la forma final sin que te resuelva ninguna etapa, este es el esqueleto de una etapa imaginaria "7" que calculara una mediana ponderada. Fíjate en la organización, no en la estadística:

```python
# etapas/etapa_7_ejemplo/app.py
from contrato.servicio import crear_app
import pandas as pd

NUMERO = 7

def _mediana_ponderada(x: pd.Series, w: pd.Series) -> float:
    """Mediana ponderada: primer valor donde la suma acumulada de pesos supera la mitad."""
    orden = x.sort_values().index
    acumulado = w[orden].cumsum()
    return float(x[orden][acumulado >= w.sum() / 2].iloc[0])

def _a_registros(df: pd.DataFrame) -> list[dict]:
    """DataFrame -> lista de dicts serializable en JSON (nulos como None)."""
    return df.astype(object).where(df.notna(), None).to_dict(orient="records")

def procesar(entrada: dict) -> dict:
    df = pd.DataFrame(entrada["registros"])

    # Decision estadistica documentada: solo ocupados, ponderado por factor calibrado
    ocupados = df[df["ocupado"] == 1]
    mediana = _mediana_ponderada(ocupados["ingreso"], ocupados["factor_calibrado"])

    return {
        "registros": _a_registros(df),
        "resumen": {"mediana_ingreso": mediana, "n": int(len(ocupados))},
    }

app = crear_app(NUMERO, procesar)
```

- Funciones auxiliares pequeñas, con nombre que empieza en `_` (convención: uso interno) y un docstring de una línea.
- `procesar` se lee de arriba abajo como una receta: cargar, decidir, calcular, empaquetar.
- Los escalares que van al `resumen` se convierten con `float` e `int`.
- Un comentario donde hay una **decisión** (a quién se le calcula, con qué peso), no donde el código es obvio.

## 2.7 Buenas prácticas de código para tu etapa

- **No leas el CSV dentro de tu etapa.** Tu entrada es el JSON que recibes. Si lees el archivo, tu servicio funciona con tus datos y no con los que le envían.
- **Nada de rutas absolutas.** `C:\Users\tu-nombre\...` no existe en la máquina de tu compañero ni en GitHub Actions. Construye rutas desde `Path(__file__)`.
- **Sin **`print`** de depuración en la versión final.** Si necesitas rastrear, usa `import logging` y `logging.info(...)`; uvicorn lo muestra en su terminal.
- **Una función, una responsabilidad.** Si `procesar` supera 40 líneas, extrae funciones auxiliares.
- **No cambies el contrato desde tu etapa.** Si crees que un esquema está mal, abre un Issue. Puede que tengas razón; la corrección se hace donde corresponde.
- **Prueba con el fixture, pero también con el CSV completo.** `pytest` usa el fixture; `ensamblador.encadenar` (Módulo 4) usa el CSV real pasando por las etapas anteriores. Ambos deben pasar.
- **Escribe el **`Responsable:`** en la cabecera del archivo.** Es la única línea del esqueleto que tienes obligación de cambiar además de `procesar`.

## 2.8 Troubleshooting del Módulo 2

| Síntoma (lo que dice probar o pytest) | Causa probable | Solución |
|----|----|----|
| `[estructura] registros -> 0 -> ocupado: Input should be a valid integer` | Columna con nulos convertida a float | `astype("Int64")` antes de exportar; verifica que los nulos salgan como `None` |
| `[estructura] ... Extra inputs are not permitted` | Devuelves un campo o columna que no está en el esquema | Elimina columnas auxiliares; compara tus llaves con `SalidaN` en `esquemas.py` |
| `[estructura] resumen -> n_filas: Field required` | Falta un campo obligatorio en `resumen` | Lee el modelo de `resumen` de tu etapa; todos los campos sin valor por defecto son obligatorios |
| `HTTP 500: ValueError: Out of range float values are not JSON compliant` | Hay un `NaN` o `inf` en la salida | Aplica `.where(df.notna(), None)`; revisa divisiones por cero en dominios vacíos |
| `HTTP 500: KeyError: 'factor_calibrado'` | Tu etapa espera una columna que solo existe en etapas posteriores | Mira el fixture de **entrada** de tu etapa: esas son las columnas que tienes |
| `Tasa fuera de [0,1]` | Devolviste porcentaje | El contrato pide proporción; el porcentaje es cosa de la publicación |
| `se aleja de la referencia` | Método distinto al especificado (sin ponderar, población base equivocada) | Relee la definición en la ficha; compara tus valores con `fixtures/etapa_N_salida.json` |
| `pytest` pasa pero `probar` da AUSENTE | El servicio no corre, o corre otro archivo | Verifica la terminal de uvicorn; el módulo debe ser el de **tu** etapa y el puerto el de tu etapa |
| `probar` pasa pero `pytest` falla | Tu `procesar` depende de algo que solo existe con el servidor corriendo (una variable global, un archivo generado antes) | `procesar` debe ser una función pura: entrada → salida, sin depender de llamadas anteriores |

## Cierre del Módulo 2

Cuando `probar` diga `[OK]` y `pytest -k etapa_N` esté en verde, tu etapa está lista **en tu máquina**. Todavía no existe para nadie más. El Módulo 3 es llevarla al repositorio compartido de forma que otros la puedan revisar, mezclar y usar.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `python -m ensamblador.probar --etapa N` imprime `[OK]` y `Cumple el contrato`. `pytest -k etapa_N` imprime `1 passed`. Y si levantas el ensamblador, tu parte del muñeco está verde.
