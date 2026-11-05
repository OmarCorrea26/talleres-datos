# Módulo 4 — Los patrones que ya usaste

Objetivo: ponerle nombre a los patrones de diseño que el proyecto ya aplica, leer los principios SOLID en el código en vez de en definiciones, e implementar dos patrones más resolviendo dos pedidos reales: un método de imputación intercambiable y un formato de archivo elegido sin preguntar. Hora y media.

### Lo que necesitas antes de empezar

- El proyecto del Módulo 3 con `14 passed`.
- Media hora de lectura tranquila antes de tocar código: la primera mitad de este módulo es vocabulario, y vale la pena.

## 4.1 Qué es un patrón y qué no es

Un patrón de diseño es un nombre para una solución que aparece una y otra vez frente al mismo tipo de problema. No es una librería ni una plantilla que se copia: es una forma de organizar dos o tres clases que, una vez que la conoces, reconoces en código ajeno y puedes nombrar en una conversación. "Esto es un adaptador" ahorra diez minutos de explicación, igual que "esto es una posestratificación" se los ahorra a un estadístico.

Hay un catálogo clásico de veintitrés, publicado en 1994 por cuatro autores a los que se conoce como la banda de los cuatro. Varios son de otra época y de lenguajes sin funciones de primera clase; en Python, un par de ellos se reducen a pasar una función como argumento. Por eso este módulo no recorre el catálogo. Recorre tu proyecto, que ya usa ocho patrones sin haberlos nombrado, y después agrega dos más porque hay dos pedidos concretos que los justifican.

> [!WARNING]
> **⚠️ Atención**
>
> El error más común con los patrones no es desconocerlos sino aplicarlos por decoración. Un Singleton para la política, una clase base abstracta con una sola implementación, un Builder para un objeto de cuatro campos. Cada uno agrega archivos y no resuelve nada. La regla de este módulo: un patrón entra cuando hay por lo menos dos variantes reales, o cuando un cambio ya dolió. Nunca antes.

## 4.2 Inventario: los patrones que ya están en el proyecto

Abre el proyecto y busca cada uno. La columna "cuándo no" es tan importante como las otras.

| Patrón | Dónde está | Qué problema resuelve | Cuándo no usarlo |
|----|----|----|----|
| Adapter | `adaptadores/http.py`, `cli.py`, `kedro.py`, `archivos.py` | Hacer que algo con una forma (JSON, argumentos de terminal, un nodo) encaje con otra forma (el dominio) sin cambiar ninguna de las dos | Cuando las dos formas son la misma y el adaptador solo pasa argumentos |
| Repository | `dominio/puertos.py` con `LectorDeEncuesta` y `EscritorDeEncuesta` | Que el dominio pida "dame la encuesta" sin saber si viene de un CSV, una tabla o una prueba | Cuando solo hay una fuente y nunca va a cambiar, ni siquiera para probar |
| Facade | `aplicacion/limpiar_encuesta.py` | Ofrecer una sola llamada (`ejecutar`) que esconde la secuencia leer, limpiar, escribir | Cuando la secuencia es una sola línea |
| Value Object | `PoliticaDeLimpieza`, `ResumenLimpieza` | Agrupar valores que viajan juntos, validarlos al crearlos y hacerlos inmutables | Para datos que cambian durante el proceso; ahí va una clase normal |
| Factory Method | `PoliticaDeLimpieza.desde_dict` | Construir un objeto a partir de una representación externa (YAML, JSON) sin que el constructor sepa de ella | Cuando el constructor ya recibe exactamente lo que llega |
| Pipeline | `reglas.limpiar`, que encadena tres reglas | Componer pasos pequeños y probables por separado en un proceso completo | Cuando el proceso tiene un solo paso |
| Inyección de dependencias | El constructor de `LimpiarEncuesta` recibe lector y escritor | Que quien arma el objeto decida con qué lo arma, de modo que la prueba pueda armarlo con falsos | Cuando el colaborador es una función pura sin estado, como `limpiar` |
| Test Double (fake) | `LectorEnMemoria` y `EscritorEnMemoria` en las pruebas | Reemplazar un puerto por una versión en memoria para probar sin disco | Cuando lo que se prueba es, justamente, el acceso al disco |

Y uno más que viste en el Taller 2 y conviene traer a la lista: los hooks de Kedro son el patrón **Observer**. Tu `RegistroDeFilas` se suscribe a eventos (antes del pipeline, después de cada nodo) y Kedro lo llama sin saber qué hace. Resuelve el problema de agregar comportamiento transversal (medir, registrar, avisar) sin ensuciar los nodos.

> [!NOTE]
> **📘 Concepto**
>
> Fíjate en que ninguno de los ocho fue "aplicado": apareció al separar lo que cambia por razones distintas. Esa es la relación real entre arquitectura y patrones. La arquitectura decide dónde van las fronteras; los patrones son las formas que toma el código justo en esas fronteras. Si conoces los nombres, puedes leer un proyecto ajeno y saber en cinco minutos dónde están sus fronteras y si las respeta.

## 4.3 SOLID, leído en el código

SOLID son cinco principios con nombres que suenan solemnes. En este proyecto cada uno se señala con el dedo.

**S, responsabilidad única.** Una pieza tiene una sola razón para cambiar. Es la tabla del Módulo 1. `reglas.py` cambia cuando cambia la metodología; `http.py` cuando cambia el transporte. En `app_acoplada.py` el mismo archivo cambiaba por cuatro razones.

**O, abierto a extensión, cerrado a modificación.** Agregar una forma de usar la limpieza no toca las existentes. Cuando escribiste `kedro.py`, no modificaste `http.py` ni `reglas.py`. En este módulo lo vas a volver a ver dos veces.

**L, sustitución.** Donde cabe un `LectorDeEncuesta` cabe cualquier cosa que cumpla el puerto, y el caso de uso no distingue. `LectorCSV` y `LectorEnMemoria` son intercambiables porque respetan la misma promesa: `leer()` devuelve una encuesta válida. Si uno devolviera a veces `None`, rompería la sustitución aunque pasara la verificación de tipos.

**I, interfaces pequeñas.** Hay dos puertos de un método cada uno, no un puerto `AlmacenDeEncuestas` con diez. El adaptador HTTP, que no lee ni escribe archivos, no implementa ninguno y no le hace falta.

**D, inversión de dependencias.** El dominio define los puertos y los adaptadores los cumplen. La dependencia apunta del detalle (CSV) hacia la abstracción (puerto), nunca al revés. Es la regla de la dependencia del Módulo 0 con su nombre de catálogo.

> [!TIP]
> **💡 Tip**
>
> Si tienes que quedarte con uno, quédate con la S. Los otros cuatro son, en buena medida, consecuencias de haber separado bien las responsabilidades. Y la S se verifica con una pregunta que ya sabes hacer: ¿cuántas razones para cambiar tiene este archivo?

## 4.4 Strategy: el método de imputación como pieza intercambiable

Llega el pedido real. Metodología quiere comparar la imputación por mediana con la imputación por media, y en algún escenario de simulación necesita imputar un valor fijo. Hoy la mediana está escrita dentro de `imputar_ingresos`, con un `transform("median")`.

La tentación es un `if metodo == "media"` dentro de la regla. Funciona con dos métodos. Con el tercero la función tiene tres ramas, con el cuarto cuatro, y cada método nuevo toca una función que ya estaba probada. Eso es modificar en vez de extender.

El patrón Strategy dice: lo que varía, que es el cálculo del valor de reemplazo, se saca a un objeto pequeño con una forma fija; la regla recibe uno y lo usa sin saber cuál es. Crea `src/limpieza/dominio/imputacion.py`:

```python
"""Estrategias de imputación: cómo se calcula el valor que reemplaza un ingreso faltante.

Es el patrón Strategy. La regla de imputación (a quién se imputa, con qué
grupo) es una sola; lo que cambia es el cálculo del valor de reemplazo. Cada
cálculo es una clase pequeña con la misma forma, y la política elige cuál.
"""

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class EstrategiaDeImputacion(Protocol):
    descripcion: str

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        """Devuelve el valor con el que se imputa a los faltantes de un grupo."""


class MedianaDelGrupo:
    descripcion = "mediana del ingreso"

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        return ingresos_del_grupo.median()


class MediaDelGrupo:
    descripcion = "media del ingreso"

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        return ingresos_del_grupo.mean()


@dataclass(frozen=True)
class ValorFijo:
    valor: float

    @property
    def descripcion(self) -> str:
        return f"valor fijo de {self.valor:,.0f}"

    def calcular(self, ingresos_del_grupo: pd.Series) -> float:
        return self.valor


ESTRATEGIAS = {
    "mediana": MedianaDelGrupo,
    "media": MediaDelGrupo,
}


def estrategia_de_imputacion(nombre: str, valor_fijo: float | None = None) -> EstrategiaDeImputacion:
    """Fábrica: convierte el nombre que viene de la configuración en una estrategia."""
    if nombre == "fijo":
        if valor_fijo is None:
            raise ValueError("la estrategia 'fijo' necesita valor_fijo")
        return ValorFijo(valor_fijo)
    try:
        return ESTRATEGIAS[nombre]()
    except KeyError:
        raise ValueError(f"estrategia de imputación desconocida: {nombre!r}; opciones: {sorted(ESTRATEGIAS)} o 'fijo'") from None
```

Tres estrategias con la misma forma, un `Protocol` que la declara, y al final una fábrica pequeña que traduce el nombre que viene del YAML o del JSON en un objeto. Dos patrones en un archivo, cada uno con su motivo.

Ahora la regla recibe la estrategia. En `reglas.py`, cambia la importación y la función de imputación:

```python
from .imputacion import EstrategiaDeImputacion, MedianaDelGrupo
```

```python
def imputar_ingresos(
    encuesta: pd.DataFrame,
    grupos: tuple[str, ...],
    estrategia: EstrategiaDeImputacion = MedianaDelGrupo(),
) -> tuple[pd.DataFrame, int]:
    """Los ocupados sin ingreso reciben el valor que calcula la estrategia para su grupo."""
    df = encuesta.copy()
    ocupados = df["ocupado"] == 1
    faltantes = ocupados & df["ingreso"].isna()
    reemplazo = df[ocupados].groupby(list(grupos))["ingreso"].transform(estrategia.calcular)
    df["ingreso_imputado"] = False
    df.loc[faltantes, "ingreso"] = reemplazo[faltantes]
    df.loc[faltantes, "ingreso_imputado"] = True
    return df, int(faltantes.sum())
```

El único cambio de fondo es que `transform("median")` se volvió `transform(estrategia.calcular)`. La estrategia por defecto es la mediana, de modo que todo lo que ya funcionaba sigue igual.

La política es quien elige. En `politica.py`, agrega dos campos y dos propiedades:

```python
from .imputacion import EstrategiaDeImputacion, estrategia_de_imputacion
```

```python
    metodo_imputacion: str = "mediana"
    valor_fijo: float | None = None
```

```python
    @property
    def estrategia(self) -> EstrategiaDeImputacion:
        return estrategia_de_imputacion(self.metodo_imputacion, self.valor_fijo)
```

En `__post_init__`, después de las dos validaciones que ya tenías, agrega la línea `self.estrategia`: construir la estrategia al crear la política hace que un nombre inválido falle ahí mismo, no tres funciones después. En `desde_dict`, lee los dos campos nuevos del diccionario con sus valores por defecto. Y en `descripcion`, reemplaza el texto fijo `"mediana del ingreso"` por `f"{self.estrategia.descripcion}"`, de modo que el resumen diga qué método se aplicó.

Por último, en `limpiar`, pásale la estrategia a la regla:

```python
    df, n_imputados = imputar_ingresos(df, politica.grupos_imputacion, politica.estrategia)
```

Compara con `material/etapa-limpiar/src/limpieza/dominio/politica.py` si algo no te cuadra.

Las pruebas, en `tests/dominio/test_imputacion.py`:

```python
"""Pruebas del patrón Strategy: la regla es una, el cálculo del reemplazo es intercambiable."""

import pandas as pd
import pytest

from limpieza.dominio import PoliticaDeLimpieza, limpiar
from limpieza.dominio.imputacion import MediaDelGrupo, MedianaDelGrupo, ValorFijo, estrategia_de_imputacion
from limpieza.dominio.reglas import imputar_ingresos


def test_cada_estrategia_calcula_su_valor():
    grupo = pd.Series([1_000_000.0, 2_000_000.0, 6_000_000.0])
    assert MedianaDelGrupo().calcular(grupo) == 2_000_000.0
    assert MediaDelGrupo().calcular(grupo) == 3_000_000.0
    assert ValorFijo(500_000.0).calcular(grupo) == 500_000.0


def test_imputar_acepta_cualquier_estrategia(encuesta_minima):
    con_media, _ = imputar_ingresos(encuesta_minima, ("area", "sexo"), MediaDelGrupo())
    con_fijo, _ = imputar_ingresos(encuesta_minima, ("area", "sexo"), ValorFijo(1.0))
    fila_media = con_media.loc[con_media["id_persona"] == 2, "ingreso"].iloc[0]
    fila_fijo = con_fijo.loc[con_fijo["id_persona"] == 2, "ingreso"].iloc[0]
    # hombres urbanos ocupados con ingreso: 1M, 50M, 50M -> media 33.67M, mediana 50M
    assert round(fila_media) == 33_666_667
    assert fila_fijo == 1.0


def test_la_fabrica_de_estrategias_entiende_la_configuracion():
    assert isinstance(estrategia_de_imputacion("media"), MediaDelGrupo)
    assert estrategia_de_imputacion("fijo", 7.0) == ValorFijo(7.0)
    with pytest.raises(ValueError, match="desconocida"):
        estrategia_de_imputacion("vecino")
    with pytest.raises(ValueError, match="valor_fijo"):
        estrategia_de_imputacion("fijo")


def test_la_politica_elige_la_estrategia_y_la_describe(encuesta_minima):
    politica = PoliticaDeLimpieza(metodo_imputacion="media")
    resultado = limpiar(encuesta_minima, politica)
    assert resultado.resumen.metodo_imputacion.startswith("media del ingreso de ocupados por area x sexo")
    with pytest.raises(ValueError):
        PoliticaDeLimpieza(metodo_imputacion="inventada")
```

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `18 passed`. Mira cuáles no cambiaron: las cinco del adaptador HTTP siguen en verde y `test_procesar_reproduce_el_resumen_de_referencia` sigue comparando igual contra el fixture, porque el método por defecto es la mediana. Agregaste una capacidad entera sin tocar un adaptador. Eso es la O de SOLID, y es lo que un `if` dentro de la regla no te habría dado.

Hay una consecuencia que vale la pena notar: como la política viaja en la petición HTTP desde el Módulo 3, metodología ya puede pedir `{"politica": {"metodo_imputacion": "media"}}` desde `/docs` y comparar. Nadie escribió una línea en `http.py` para eso.

## 4.5 Factory: el formato de archivo se elige solo

Segundo pedido. El muñeco quiere pasar a Parquet, y la terminal debería aceptar las dos cosas sin que el usuario tenga que decir cuál. Hoy `cli.py` construye `LectorCSV` y `EscritorCSV` a mano.

Primero la pareja nueva, `adaptadores/parquet.py`, que es `archivos.py` con `read_parquet` y `to_parquet` (si hiciste el ejercicio 3.9 ya la tienes). Instala `pyarrow` y agrégalo como extra `parquet` en `pyproject.toml`, junto a `http`.

Ahora la fábrica, `adaptadores/fabrica.py`:

```python
"""Fábrica de adaptadores de archivo: elige el lector y el escritor según la extensión.

Es el patrón Factory. Quien necesita leer o escribir no decide qué clase usar;
le pasa la ruta a la fábrica y recibe un objeto que cumple el puerto. Agregar
un formato es agregar una pareja de clases y una línea en el registro.
"""

from pathlib import Path

from limpieza.adaptadores.archivos import EscritorCSV, LectorCSV
from limpieza.adaptadores.parquet import EscritorParquet, LectorParquet
from limpieza.dominio.puertos import EscritorDeEncuesta, LectorDeEncuesta

FORMATOS = {
    ".csv": (LectorCSV, EscritorCSV),
    ".parquet": (LectorParquet, EscritorParquet),
}


def _pareja(ruta: Path):
    extension = Path(ruta).suffix.lower()
    try:
        return FORMATOS[extension]
    except KeyError:
        raise ValueError(f"formato no soportado: {extension!r}; opciones: {sorted(FORMATOS)}") from None


def crear_lector(ruta: Path) -> LectorDeEncuesta:
    return _pareja(ruta)[0](ruta)


def crear_escritor(ruta: Path) -> EscritorDeEncuesta:
    return _pareja(ruta)[1](ruta)
```

Fíjate en el tipo de retorno: `LectorDeEncuesta`, el puerto, no `LectorCSV`. Quien llama a la fábrica recibe "algo que cumple el puerto" y no sabe más. Eso es lo que permite que el registro `FORMATOS` crezca sin que nadie fuera de este archivo se entere.

Hay una excepción consciente a la regla de la sección 3.7, la de que un adaptador nunca conoce a otro: la fábrica conoce a todos los adaptadores de archivo, porque su único trabajo es elegir entre ellos. Es el lugar donde ese conocimiento se concentra para que no se reparta. Si al repetir el comando de la 3.7 ves que `fabrica.py` importa `archivos` y `parquet`, está bien; si lo ves en `cli.py` o en `http.py`, no.

En `cli.py`, reemplaza la importación de `archivos` por la de `fabrica`, y la línea que arma el caso de uso:

```python
from limpieza.adaptadores.fabrica import crear_escritor, crear_lector
```

```python
    caso_de_uso = LimpiarEncuesta(crear_lector(opciones.entrada), crear_escritor(opciones.salida), politica)
```

De paso, agrega al parser las dos opciones que la política ya sabe recibir, `--metodo` y `--valor-fijo`, y pásalas al construirla. La versión completa está en `material/etapa-limpiar/src/limpieza/adaptadores/cli.py`.

Las pruebas, en `tests/adaptadores/test_fabrica.py`:

```python
"""Pruebas del patrón Factory: la extensión decide el adaptador, y los dos formatos son equivalentes."""

import pandas as pd
import pytest

from limpieza.adaptadores.archivos import EscritorCSV, LectorCSV
from limpieza.adaptadores.cli import main
from limpieza.adaptadores.fabrica import crear_escritor, crear_lector
from limpieza.adaptadores.parquet import EscritorParquet, LectorParquet


def test_la_fabrica_elige_por_extension(tmp_path):
    assert isinstance(crear_lector(tmp_path / "a.csv"), LectorCSV)
    assert isinstance(crear_escritor(tmp_path / "a.CSV"), EscritorCSV)
    assert isinstance(crear_lector(tmp_path / "a.parquet"), LectorParquet)
    assert isinstance(crear_escritor(tmp_path / "a.parquet"), EscritorParquet)
    with pytest.raises(ValueError, match="no soportado"):
        crear_lector(tmp_path / "a.xlsx")


def test_csv_y_parquet_producen_la_misma_limpieza(tmp_path, encuesta_minima):
    entrada_csv = tmp_path / "entrada.csv"
    entrada_parquet = tmp_path / "entrada.parquet"
    encuesta_minima.to_csv(entrada_csv, index=False)
    encuesta_minima.to_parquet(entrada_parquet, index=False)

    main([str(entrada_csv), str(tmp_path / "salida_a.csv"), "--percentil", "0.5"])
    main([str(entrada_parquet), str(tmp_path / "salida_b.parquet"), "--percentil", "0.5"])

    desde_csv = pd.read_csv(tmp_path / "salida_a.csv")
    desde_parquet = pd.read_parquet(tmp_path / "salida_b.parquet")
    # NaN no es igual a NaN: por eso se compara con fillna y no con ==
    assert desde_csv["ingreso"].fillna(-1).tolist() == desde_parquet["ingreso"].fillna(-1).tolist()
    assert desde_csv["id_persona"].tolist() == desde_parquet["id_persona"].tolist()
```

```powershell
pytest
python -m limpieza.adaptadores.cli ..\ruta\al\material\datos\encuesta_hogares.csv salida\limpia.parquet --metodo media
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `20 passed`. La terminal escribió `salida\limpia.parquet` sin que le dijeras el formato, y `salida\limpia_resumen.json` dice `media del ingreso de ocupados por area x sexo`. El pedido "el muñeco pasa a Parquet" de la tabla del Módulo 1 costó un archivo nuevo, un registro de dos líneas y ninguna regla tocada.

## 4.6 Lo que no hay que hacer

Para cerrar el vocabulario, tres cosas que el proyecto no tiene y que alguien va a proponer en algún momento. Un Singleton para la política, "para no pasarla por todos lados": rompe la inyección de dependencias y hace que dos pruebas no puedan usar políticas distintas. Una clase base `Regla` de la que hereden las tres reglas, "para que sean uniformes": las reglas ya son uniformes porque son funciones con la misma firma, y una jerarquía con un solo nivel no aporta nada. Un Builder para `PoliticaDeLimpieza`, "para que sea fluido": tiene cuatro campos con valores por defecto, y `desde_dict` ya cubre el caso real.

La prueba para cualquier patrón propuesto es la misma de la sección 4.1: ¿qué dos variantes reales distingue, o qué cambio que ya dolió evita? Si la respuesta es "ninguna, pero queda más limpio", no entra.

## 4.7 Ejercicio práctico: una estrategia y un formato más

Dos pedidos, uno por patrón. Primero, metodología pide una imputación por media recortada: la media del grupo después de descartar el 5 % más bajo y el 5 % más alto. Escribe la estrategia `MediaRecortada` en `imputacion.py`, regístrala con el nombre `media_recortada` y agrégale una prueba con un grupo donde la media recortada difiera de la media simple. Segundo, alguien del equipo trabaja en Excel: escribe `adaptadores/excel.py` con un lector y un escritor para `.xlsx` (con `openpyxl`), regístralos en la fábrica y prueba que la terminal escribe un `.xlsx`.

Al terminar, repite el comando de la sección 3.7: `dominio/` no debe importar nada nuevo salvo lo de la estrategia, y `fabrica.py` debe ser el único archivo que conozca a `excel.py`.

## 4.8 Troubleshooting del Módulo 4

| Síntoma | Causa probable | Solución |
|----|----|----|
| `ImportError: cannot import name 'EstrategiaDeImputacion'` | `reglas.py` importa de `imputacion.py` y este de `politica.py`, o al revés, en círculo | `imputacion.py` no importa nada del dominio; `politica.py` importa de `imputacion.py`; `reglas.py` importa de ambos |
| `test_procesar_reproduce_el_resumen_de_referencia` deja de pasar | Cambiaste el texto de `descripcion` o el método por defecto | El predeterminado es `"mediana"` y la descripción debe seguir empezando por `mediana del ingreso` |
| `ValueError: estrategia de imputación desconocida` al crear la política | Escribiste el nombre con mayúscula o tilde | Los nombres son `mediana`, `media` y `fijo`, tal cual |
| `ImportError: Unable to find a usable engine` al escribir Parquet | Falta `pyarrow` | `pip install -e ".[http,parquet,dev]"` |
| La fábrica dice formato no soportado con `.CSV` | Versión vieja de la fábrica sin `.lower()` | Compara con la sección 4.5 |

## 4.9 Para profundizar (opcional)

- El sitio refactoring.guru tiene cada patrón del catálogo explicado con un problema, una solución y un ejemplo en Python. Lee Strategy, Factory y Adapter ahí y compáralos con los tuyos.
- La charla "Python Design Patterns" de Brandon Rhodes explica cuáles patrones del catálogo clásico se vuelven triviales en Python y por qué. Es la mejor vacuna contra la decoración.
