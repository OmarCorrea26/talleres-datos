# Módulo 4 — IA en el IDE aplicada a Kedro

Objetivo: usar un asistente de IA para extender el pipeline con un indicador nuevo, revisando cada línea con los criterios de este taller, y cerrar con el Issue de entrega. Una hora.

### Lo que necesitas antes de empezar

- El asistente que instalaste en el Módulo 4 del Taller 1, funcionando en VSCode.
- El proyecto del Módulo 3 con las pruebas en verde y subido a GitHub.

## 4.1 Dónde ayuda más la IA en un proyecto Kedro

En el Taller 1 la regla fue "la IA propone, tú decides". En Kedro esa regla se vuelve más fácil de aplicar, y vale la pena entender por qué. Un nodo es una función con una firma clara, entradas con nombre y una salida con forma conocida. Eso es exactamente lo que un asistente necesita para proponer algo útil, y exactamente lo que tú necesitas para evaluar si lo que propuso sirve.

Donde la IA rinde más: escribir el cuerpo de un nodo a partir de una firma y una descripción precisa, proponer casos de prueba para un nodo que ya existe, explicar un error de Kedro que no entiendes, y redactar una entrada del catálogo para un tipo de dataset que no has usado.

Donde rinde menos y hay que vigilarla: decidir la estructura de los pipelines, elegir qué va en parámetros y qué va en código, y cualquier decisión metodológica. Un asistente te va a proponer con la misma seguridad una mediana ponderada correcta y una incorrecta. La estadística la pones tú.

## 4.2 Buenos prompts para pedir un nodo

Compara estas dos formas de pedir lo mismo.

Un prompt pobre:

```text
Haz una función que calcule el ingreso mediano por área.
```

Un prompt que respeta el contexto del proyecto:

```text
Estoy en un proyecto Kedro. Necesito un nodo para el pipeline de estimación,
en el archivo src/encuesta_hogares/pipelines/estimacion/nodes.py.

Firma: def estimar_ingreso_mediano(encuesta: pd.DataFrame) -> pd.DataFrame

Entrada: la encuesta calibrada, con columnas ocupado (Int64), ingreso (float),
area (str) y factor_calibrado (float).

Salida: un DataFrame con una fila por área y columnas indicador (siempre
"ingreso_mediano"), area, valor, n_muestra y poblacion_estimada, con los mismos
nombres y tipos que usa la función estimar_indicadores del mismo archivo.

Reglas: solo ocupados (ocupado == 1); la mediana debe ser ponderada con
factor_calibrado, no la mediana simple; sin leer ni escribir archivos; sin
variables globales. Incluye una función auxiliar _mediana_ponderada separada,
para poder probarla sola.
```

El segundo prompt dice dónde va el código, qué recibe, qué devuelve, con qué debe ser consistente y qué está prohibido. Nota que la decisión metodológica (ponderar) la tomaste tú y se la impusiste. Si no lo haces, el asistente va a usar `median()` de pandas, que ignora los factores, y el resultado va a parecer razonable y estar mal.

> [!TIP]
> **💡 Tip**
>
> Abre `nodes.py` en el editor antes de pedir. La mayoría de los asistentes usan los archivos abiertos como contexto, y así van a imitar el estilo de las funciones que ya existen: nombres en español, docstrings, `float()` e `int()` en las salidas.

## 4.3 Lista de verificación antes de aceptar código en un pipeline

Pasa cada propuesta por estas preguntas, en orden. Si alguna falla, no la aceptes todavía.

1. ¿La función lee o escribe archivos, o usa rutas? Si sí, está mal: eso es del catálogo.
2. ¿Depende de algo que no venga por sus argumentos? Variables globales, parámetros leídos de un YAML a mano, el reloj del sistema sin que se lo pidas.
3. ¿La salida tiene la forma que pediste? Nombres de columna, tipos, una fila por grupo.
4. ¿La estadística es la que tú decidiste? Ponderada o no, sobre qué población, con qué filtro.
5. ¿Entiendes cada línea? Si hay una que no, pide que la explique. Si después de la explicación sigues sin entenderla, no la uses.
6. ¿Se puede probar con cinco filas? Si la función es tan enredada que no sabes qué DataFrame mínimo armarle, pide que la divida.

## 4.4 Ejercicio práctico: el ingreso mediano con ayuda de IA

Vas a agregar el indicador `ingreso_mediano` por área al pipeline de estimación. El flujo es el mismo del Módulo 2, con la IA escribiendo el cuerpo de la función y tú haciendo todo lo demás.

1. Pide el nodo con el prompt de la sección 4.2, o con tu propia versión. Revísalo con la lista de la sección 4.3. Corrígelo o vuelve a pedirlo hasta que pase.
2. Agrégalo a `pipeline.py` del pipeline de estimación como un nodo que recibe `encuesta_calibrada` y produce `ingreso_mediano`.
3. Registra `ingreso_mediano` en el catálogo como CSV en `data/07_model_output/`.
4. Corre `kedro run --pipeline estimacion` y abre el archivo.
5. Pídele al asistente una prueba para `_mediana_ponderada` con tres valores y pesos muy desiguales, de modo que la mediana ponderada sea distinta de la simple. Revísala, agrégala a `tests/pipelines/estimacion/test_nodes.py` y corre `pytest`.
6. Haz commit y push.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `data/07_model_output/ingreso_mediano.csv` tiene dos filas, Rural y Urbana, y los valores son distintos de los promedios del Módulo 2. `pytest` reporta una prueba más en verde. Kedro-Viz muestra el nodo nuevo colgando de `encuesta_calibrada`, al lado de `estimar_indicadores` y sin depender de él.

Si te atascas, en `material/encuesta-hogares` no está la solución a propósito. Está en la carpeta del facilitador, y la idea es que la pidas solo después de haber intentado.

## 4.5 Cuándo no usar IA

Hay tres momentos de este taller en los que el asistente estorba más de lo que ayuda. Cuando estás decidiendo la estructura (qué pipelines, qué nodos, qué va en parámetros): eso requiere entender el proceso estadístico y la IA no lo entiende. Cuando un error de Kedro te resulta incomprensible: antes de pegárselo, lee el mensaje completo y busca el nombre del dataset o del nodo que menciona, porque el ochenta por ciento de las veces es un nombre mal escrito y lo encuentras más rápido tú. Y cuando estás aprendiendo algo por primera vez: si la IA escribe el primer nodo, el segundo y el tercero, al cuarto no vas a saber escribirlo sin ella.

### Reflexión final del taller

Vuelve a abrir `material/modulo_1/proceso_monolito.py` y ponlo al lado de tu proyecto. Hacen lo mismo. El tuyo tiene más archivos, y sin embargo cada uno responde una sola pregunta: dónde están los datos, qué hace cada paso, qué decisiones se pueden cambiar, cómo se prueba. Esa es la diferencia entre un script y un proceso, y es lo que te llevas de este taller.

## 4.6 Entregable: Issue de validación

Crea un Issue en tu repositorio `kedro-encuesta-<tu-nombre>` con el título `Entrega Taller 2 — [tu nombre]` y este contenido:

```markdown
## Entrega Taller 2

- Repositorio: <enlace>
- `kedro run` completa 9 tareas (7 de la guía, más `contar_hogares` e `ingreso_mediano`): sí / no
- `pytest`: N pruebas en verde
- Pipelines registrados (`kedro registry list`): preparacion, estimacion, estimacion_rural

## Lo que más me costó

(dos o tres líneas)

## Lo que cambiaría del proceso de mi trabajo después de esto

(dos o tres líneas)
```

Asigna el Issue a quien facilita el taller. Con eso queda entregado.

## 4.7 Para profundizar (opcional)

- Pídele al asistente que te explique, línea por línea, el `pipeline_registry.py` de la sección 2.9. Compara su explicación con la de la guía y anota dónde difieren.
- Kedro tiene su propia extensión para VSCode, con navegación entre catálogo, nodos y Viz integrado. Búscala en el mercado de extensiones como "Kedro".
