# Módulo 2 — El dominio en el centro

Objetivo: extraer las reglas de limpieza a un paquete que no sepa nada del exterior, probarlas con cinco filas, declarar lo que necesitan como puertos y escribir el caso de uso que las orquesta. Dos horas.

### Lo que necesitas antes de empezar

- El diagnóstico del Módulo 1 fresco: sabes qué líneas son reglas y cuáles no.
- El entorno `.venv-arquitectura` activo.

## 2.1 Un proyecto instalable

Crea la carpeta del proyecto en tu carpeta de proyectos y entra a ella:

```powershell
mkdir etapa-limpiar
cd etapa-limpiar
code .
```

Crea `pyproject.toml` en la raíz:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "limpieza"
version = "1.0.0"
description = "Etapa de limpieza de la encuesta de hogares, con el dominio separado de sus adaptadores"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.0",
]

[project.optional-dependencies]
http = ["fastapi>=0.110", "uvicorn>=0.27", "httpx>=0.27"]
dev = ["pytest>=8"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
addopts = "-ra"
testpaths = ["tests"]
filterwarnings = ["ignore::DeprecationWarning"]
```

Mira la sección `dependencies`: el paquete, como tal, solo depende de pandas. FastAPI y uvicorn son opcionales, bajo el nombre `http`. Eso no es un detalle de empaquetado: es la primera decisión de arquitectura escrita en un archivo. Quien quiera la limpieza para Kedro no tiene por qué instalar un servidor web.

> [!NOTE]
> **📘 Concepto**
>
> En los talleres anteriores el código vivía en carpetas que Python encontraba por estar en la ruta de trabajo. Aquí vamos a instalar el proyecto en modo editable con `pip install -e .`, de modo que `import limpieza` funcione desde cualquier carpeta y pytest, uvicorn y Kedro lo encuentren sin trucos. "Editable" significa que pip apunta a tu carpeta `src/` en vez de copiarla: cada cambio que guardes se ve de inmediato.

Crea la estructura de carpetas. Fíjate en los nombres: dicen de qué trata el proyecto antes de abrir un archivo.

```text
etapa-limpiar/
  pyproject.toml
  src/limpieza/
    __init__.py
    dominio/
      __init__.py
    aplicacion/
      __init__.py
    adaptadores/
      __init__.py
  tests/
    __init__.py
    conftest.py
    dominio/__init__.py
    aplicacion/__init__.py
    adaptadores/__init__.py
```

Los `__init__.py` de `aplicacion` y `adaptadores` pueden quedar vacíos por ahora. Instala el proyecto:

```powershell
pip install -e ".[http,dev]"
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `python -c "import limpieza; print(limpieza.__file__)"` imprime la ruta a tu carpeta `src/limpieza/__init__.py`. Si imprime otra ruta, hay otro paquete con el mismo nombre en el entorno.

## 2.2 Las decisiones, con nombre

Antes que las reglas, lo que las reglas necesitan decidido. En `app_acoplada.py` eran dos constantes. Aquí van a ser una clase pequeña e inmutable, en `src/limpieza/dominio/politica.py`:

```python
"""Las decisiones metodológicas de la limpieza, con nombre y valor por defecto."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PoliticaDeLimpieza:
    """Qué se considera atípico y cómo se imputa.

    Es inmutable a propósito: una política se decide una vez por corrida y
    ningún paso del proceso debería poder cambiarla por el camino.
    """

    percentil_atipicos: float = 0.99
    grupos_imputacion: tuple[str, ...] = ("area", "sexo")

    def __post_init__(self):
        if not 0 < self.percentil_atipicos <= 1:
            raise ValueError("percentil_atipicos debe estar entre 0 y 1")
        if not self.grupos_imputacion:
            raise ValueError("grupos_imputacion no puede estar vacío")

    @classmethod
    def desde_dict(cls, valores: dict) -> "PoliticaDeLimpieza":
        """Construye la política a partir de un diccionario, como el que viene de un YAML o de JSON."""
        return cls(
            percentil_atipicos=float(valores.get("percentil_atipicos", cls.percentil_atipicos)),
            grupos_imputacion=tuple(valores.get("grupos_imputacion", cls.grupos_imputacion)),
        )

    @property
    def descripcion(self) -> str:
        grupos = " x ".join(self.grupos_imputacion)
        return (
            f"mediana del ingreso de ocupados por {grupos}; "
            f"atipicos recortados al percentil {self.percentil_atipicos:.0%}".replace("%", "")
        )
```

Tres cosas que esta clase hace y una constante no puede. Valida: un percentil de 1.5 falla al construirse, no tres funciones después. Se construye desde un diccionario, que es la forma en que va a llegar desde Kedro o desde una petición. Y se describe a sí misma, de manera que el resumen diga exactamente qué política se aplicó, en vez de un texto fijo que miente en cuanto alguien cambia el percentil.

## 2.3 Las reglas, una por una

Ahora `src/limpieza/dominio/reglas.py`. Las tres reglas que en el Módulo 1 estaban entrelazadas, cada una en su función, y una cuarta que las compone:

```python
"""Las reglas de limpieza de la encuesta.

Tres reglas pequeñas y una función que las compone. Todas reciben un DataFrame
y devuelven otro, junto con el número que describe lo que hicieron. Ninguna
abre archivos, ninguna sabe de HTTP ni de Kedro, ninguna lee configuración.
"""

from dataclasses import asdict, dataclass

import pandas as pd

from .politica import PoliticaDeLimpieza


@dataclass(frozen=True)
class ResumenLimpieza:
    n_entrada: int
    n_duplicados_eliminados: int
    n_salida: int
    n_imputados: int
    n_atipicos_ajustados: int
    metodo_imputacion: str

    def como_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ResultadoLimpieza:
    encuesta: pd.DataFrame
    resumen: ResumenLimpieza


def eliminar_duplicados(encuesta: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Conserva la primera aparición de cada id_persona."""
    sin_duplicados = encuesta.drop_duplicates(subset="id_persona").reset_index(drop=True)
    return sin_duplicados, len(encuesta) - len(sin_duplicados)


def recortar_atipicos(encuesta: pd.DataFrame, percentil: float) -> tuple[pd.DataFrame, int]:
    """Todo ingreso por encima del percentil se recorta a ese valor (winsorización)."""
    df = encuesta.copy()
    tope = df["ingreso"].quantile(percentil)
    atipicos = df["ingreso"] > tope
    df.loc[atipicos, "ingreso"] = tope
    return df, int(atipicos.sum())


def imputar_ingresos(encuesta: pd.DataFrame, grupos: tuple[str, ...]) -> tuple[pd.DataFrame, int]:
    """Los ocupados sin ingreso reciben la mediana de su grupo y quedan marcados."""
    df = encuesta.copy()
    ocupados = df["ocupado"] == 1
    faltantes = ocupados & df["ingreso"].isna()
    mediana = df[ocupados].groupby(list(grupos))["ingreso"].transform("median")
    df["ingreso_imputado"] = False
    df.loc[faltantes, "ingreso"] = mediana[faltantes]
    df.loc[faltantes, "ingreso_imputado"] = True
    return df, int(faltantes.sum())


def limpiar(encuesta: pd.DataFrame, politica: PoliticaDeLimpieza) -> ResultadoLimpieza:
    """Aplica las tres reglas en orden y devuelve la base limpia con su resumen."""
    n_entrada = len(encuesta)
    df, n_duplicados = eliminar_duplicados(encuesta)
    df, n_atipicos = recortar_atipicos(df, politica.percentil_atipicos)
    df, n_imputados = imputar_ingresos(df, politica.grupos_imputacion)
    df["ocupado"] = df["ocupado"].astype("Int64")

    resumen = ResumenLimpieza(
        n_entrada=int(n_entrada),
        n_duplicados_eliminados=int(n_duplicados),
        n_salida=int(len(df)),
        n_imputados=n_imputados,
        n_atipicos_ajustados=n_atipicos,
        metodo_imputacion=politica.descripcion,
    )
    return ResultadoLimpieza(encuesta=df, resumen=resumen)
```

Compara con `app_acoplada.py`. Las operaciones de pandas son las mismas, línea por línea. Lo que cambió es que cada regla tiene nombre, firma y docstring, que el resumen es una clase y no un diccionario armado a mano, y que no hay una sola importación que no sea pandas o la biblioteca estándar.

Deja `src/limpieza/dominio/__init__.py` exponiendo lo que el resto del proyecto va a usar:

```python
"""El dominio: reglas de limpieza puras, sin frameworks ni archivos."""

from .politica import PoliticaDeLimpieza
from .reglas import ResultadoLimpieza, ResumenLimpieza, limpiar

__all__ = ["PoliticaDeLimpieza", "ResultadoLimpieza", "ResumenLimpieza", "limpiar"]
```

> [!WARNING]
> **⚠️ Atención**
>
> El dominio devuelve `ResultadoLimpieza`, no un diccionario con `registros`. Esa palabra, `registros`, es del contrato del Taller 3, es decir, del transporte. Si la escribes en `reglas.py`, el dominio empieza a saber cómo lo llaman desde afuera, y ese es el primer paso de vuelta al acoplamiento.

## 2.4 Probar el dominio con cinco filas

Esta es la recompensa inmediata de la separación. Crea `tests/conftest.py` con un DataFrame mínimo que todas las pruebas van a compartir:

```python
import pandas as pd
import pytest


@pytest.fixture
def encuesta_minima() -> pd.DataFrame:
    """Cinco personas: un duplicado, un atípico evidente y un ocupado sin ingreso."""
    return pd.DataFrame(
        {
            "id_persona": [1, 2, 3, 3, 4],
            "id_hogar": [1, 1, 2, 2, 3],
            "departamento": ["Bogota", "Bogota", "Valle", "Valle", "Valle"],
            "area": ["Urbana", "Urbana", "Urbana", "Urbana", "Rural"],
            "sexo": ["H", "H", "H", "H", "M"],
            "edad": [30, 40, 25, 25, 50],
            "ocupado": pd.array([1, 1, 1, 1, 0], dtype="Int64"),
            "ingreso": [1_000_000.0, None, 50_000_000.0, 50_000_000.0, None],
            "factor_expansion": [100.0, 100.0, 50.0, 50.0, 50.0],
        }
    )
```

Y `tests/dominio/test_reglas.py`:

```python
"""Pruebas del dominio: sin archivos, sin HTTP, sin Kedro. Solo DataFrames y reglas."""

import pandas as pd
import pytest

from limpieza.dominio import PoliticaDeLimpieza, limpiar
from limpieza.dominio.reglas import eliminar_duplicados, imputar_ingresos, recortar_atipicos


def test_eliminar_duplicados_conserva_la_primera_aparicion(encuesta_minima):
    sin_duplicados, eliminados = eliminar_duplicados(encuesta_minima)
    assert eliminados == 1
    assert sin_duplicados["id_persona"].tolist() == [1, 2, 3, 4]


def test_recortar_atipicos_baja_el_ingreso_al_tope():
    encuesta = pd.DataFrame({"ingreso": [1_000_000.0, 2_000_000.0, 3_000_000.0, 100_000_000.0, None]})
    tope = encuesta["ingreso"].quantile(0.75)

    recortada, ajustados = recortar_atipicos(encuesta, percentil=0.75)

    assert ajustados == 1
    assert recortada["ingreso"].max() == tope
    assert recortada["ingreso"].isna().sum() == 1, "los vacíos no se tocan"


def test_imputar_ingresos_usa_la_mediana_del_grupo(encuesta_minima):
    imputada, n = imputar_ingresos(encuesta_minima, grupos=("area", "sexo"))
    assert n == 1
    fila = imputada.loc[imputada["id_persona"] == 2].iloc[0]
    assert fila["ingreso_imputado"]
    # mediana de los hombres urbanos ocupados con ingreso: 1M, 50M, 50M -> 50M
    assert fila["ingreso"] == 50_000_000.0


def test_limpiar_compone_las_tres_reglas(encuesta_minima):
    resultado = limpiar(encuesta_minima, PoliticaDeLimpieza(percentil_atipicos=0.5))
    resumen = resultado.resumen
    assert (resumen.n_entrada, resumen.n_salida) == (5, 4)
    assert resumen.n_duplicados_eliminados == 1
    assert resumen.n_imputados == 1
    assert "percentil 50" in resumen.metodo_imputacion
    assert str(resultado.encuesta["ocupado"].dtype) == "Int64"


def test_la_politica_rechaza_valores_imposibles():
    with pytest.raises(ValueError):
        PoliticaDeLimpieza(percentil_atipicos=1.5)
    with pytest.raises(ValueError):
        PoliticaDeLimpieza(grupos_imputacion=())


def test_la_politica_se_construye_desde_un_diccionario():
    politica = PoliticaDeLimpieza.desde_dict({"percentil_atipicos": 0.95, "grupos_imputacion": ["area"]})
    assert politica.percentil_atipicos == 0.95
    assert politica.grupos_imputacion == ("area",)
```

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `6 passed` en menos de un segundo. Acabas de probar las tres reglas estadísticas y la política sin levantar un servidor ni leer un archivo. En el Módulo 1 esto era imposible.

> [!TIP]
> **💡 Tip**
>
> Mira la prueba de imputación: su comentario explica de dónde sale el 50M. Las pruebas del dominio son el mejor lugar para dejar escrito un caso que un revisor metodológico quiera verificar a mano. Son documentación que se ejecuta.

## 2.5 Puertos: lo que el dominio necesita, dicho en su idioma

Las reglas ya no saben de archivos. Sin embargo, en algún momento alguien tiene que entregarles una encuesta y recibir el resultado. La pregunta es cómo pedirlo sin decir "un CSV" o "una petición HTTP". La respuesta es un puerto: una interfaz, escrita desde el punto de vista del dominio.

`src/limpieza/dominio/puertos.py`:

```python
"""Puertos: lo que el dominio necesita del mundo exterior, dicho en su propio idioma.

Un puerto es una interfaz. El dominio dice "necesito algo que me entregue la
encuesta" y "necesito algo que reciba el resultado", sin decir si eso es un
CSV, una tabla de SQL o una petición HTTP. Quien cumpla la interfaz sirve.

Se usan Protocol en vez de clases base para no obligar a heredar: cualquier
objeto con los métodos correctos encaja, incluso uno escrito para una prueba.
"""

from typing import Protocol

import pandas as pd

from .reglas import ResumenLimpieza


class LectorDeEncuesta(Protocol):
    def leer(self) -> pd.DataFrame:
        """Devuelve la encuesta validada, una fila por persona."""


class EscritorDeEncuesta(Protocol):
    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        """Recibe la encuesta limpia y su resumen, y hace con ellos lo que corresponda."""
```

> [!NOTE]
> **📘 Concepto**
>
> `Protocol` es la forma de Python de decir "cualquier cosa que tenga este método". No hace falta heredar de `LectorDeEncuesta`: un objeto con un método `leer()` que devuelva un DataFrame ya lo cumple. Es lo que en otros lenguajes se llama interfaz, y es exactamente lo que el contrato del muñeco hacía con JSON: definir una forma, no una implementación.

Fíjate en que los puertos hablan de "encuesta" y "resumen", nunca de rutas ni de formatos. Los escribió el dominio para sus necesidades, y por eso la dependencia sigue apuntando hacia adentro: quien implemente un puerto va a importar `limpieza.dominio`, nunca al revés.

## 2.6 El caso de uso

Falta la pieza que junta todo: leer con un lector, limpiar, escribir con un escritor. Es poco código y es importante que sea poco. `src/limpieza/aplicacion/limpiar_encuesta.py`:

```python
"""Caso de uso: limpiar una encuesta completa, de donde venga, hacia donde vaya."""

from limpieza.dominio import PoliticaDeLimpieza, ResumenLimpieza, limpiar
from limpieza.dominio.puertos import EscritorDeEncuesta, LectorDeEncuesta


class LimpiarEncuesta:
    """Lee con un lector, aplica las reglas y entrega con un escritor.

    No sabe qué son el lector ni el escritor: solo que cumplen los puertos.
    Por eso el mismo caso de uso sirve para archivos, para una prueba en
    memoria o para lo que aparezca después.
    """

    def __init__(self, lector: LectorDeEncuesta, escritor: EscritorDeEncuesta, politica: PoliticaDeLimpieza):
        self._lector = lector
        self._escritor = escritor
        self._politica = politica

    def ejecutar(self) -> ResumenLimpieza:
        encuesta = self._lector.leer()
        resultado = limpiar(encuesta, self._politica)
        self._escritor.escribir(resultado.encuesta, resultado.resumen)
        return resultado.resumen
```

Y en `src/limpieza/aplicacion/__init__.py`:

```python
"""La capa de aplicación: casos de uso que orquestan el dominio a través de los puertos."""

from .limpiar_encuesta import LimpiarEncuesta

__all__ = ["LimpiarEncuesta"]
```

El caso de uso recibe el lector y el escritor ya construidos. No los crea él. A eso se le llama inyección de dependencias y suena más complicado de lo que es: significa que quien arma el caso de uso decide con qué lo arma, y por eso el mismo `LimpiarEncuesta` sirve para archivos de verdad o para dos objetos falsos en una prueba.

## 2.7 Probar el caso de uso con puertos falsos

`tests/aplicacion/test_limpiar_encuesta.py`:

```python
"""Prueba del caso de uso con puertos falsos en memoria.

Aquí se ve para qué sirven los puertos: el caso de uso se prueba completo sin
tocar el disco, porque el lector y el escritor son dos clases de diez líneas
escritas para la prueba.
"""

import pandas as pd

from limpieza.aplicacion import LimpiarEncuesta
from limpieza.dominio import PoliticaDeLimpieza, ResumenLimpieza


class LectorEnMemoria:
    def __init__(self, encuesta: pd.DataFrame):
        self._encuesta = encuesta

    def leer(self) -> pd.DataFrame:
        return self._encuesta


class EscritorEnMemoria:
    def __init__(self):
        self.encuesta = None
        self.resumen = None

    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        self.encuesta = encuesta
        self.resumen = resumen


def test_el_caso_de_uso_lee_limpia_y_escribe(encuesta_minima):
    escritor = EscritorEnMemoria()
    caso_de_uso = LimpiarEncuesta(LectorEnMemoria(encuesta_minima), escritor, PoliticaDeLimpieza())

    resumen = caso_de_uso.ejecutar()

    assert resumen is escritor.resumen
    assert len(escritor.encuesta) == 4
    assert resumen.n_duplicados_eliminados == 1
```

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `7 passed`. Las dos clases falsas no heredan de nada y aun así cumplen los puertos. Eso es `Protocol` funcionando.

## 2.8 Ejercicio práctico: una regla nueva sin tocar las otras

Agrega al dominio una cuarta regla, `descartar_edades_imposibles`, que elimine las filas con edad mayor a 120 y devuelva cuántas descartó. Para hacerlo bien tienes que tocar tres lugares, y solo tres: la función nueva en `reglas.py`, su llamada dentro de `limpiar` con el conteo agregado al resumen como `n_edades_descartadas`, y una prueba en `test_reglas.py` con una fila de 150 años. Si tocaste algo más, revisa por qué.

Cuando termines, deja el campo nuevo en el resumen pero vuelve a leer `ResumenLimpieza`: en el Módulo 3 vas a ver qué pasa con el contrato del Taller 3 cuando el resumen tiene un campo que el contrato no conoce, y esa es una conversación de arquitectura, no de código.

## 2.9 Troubleshooting del Módulo 2

| Síntoma | Causa probable | Solución |
|----|----|----|
| `ModuleNotFoundError: No module named 'limpieza'` | No instalaste el proyecto en modo editable, o lo hiciste con otro entorno activo | `pip install -e ".[http,dev]"` desde la raíz, con `.venv-arquitectura` activo |
| `pip install -e` falla diciendo que no encuentra paquetes | Falta `src/limpieza/__init__.py` o la sección `packages.find` del `pyproject.toml` | Compara con la sección 2.1 |
| `FrozenInstanceError` al correr | Intentaste modificar una `PoliticaDeLimpieza` después de crearla | Es a propósito; crea una nueva con el valor que quieres |
| `pytest` no encuentra `encuesta_minima` | `conftest.py` no está en `tests/` o falta `tests/__init__.py` | Revisa la estructura de la sección 2.1 |
| La mediana de la prueba de imputación no da 50M | Cambiaste el fixture | Vuelve al de la sección 2.4 o recalcula el valor esperado y actualiza el comentario |

## 2.10 Para profundizar (opcional)

- Lee sobre `dataclasses` en la documentación de Python. `frozen=True` y `__post_init__` son las dos opciones que más vas a usar para modelar decisiones y resultados.
- La idea de que las reglas no conozcan el exterior tiene muchos nombres: arquitectura hexagonal, de puertos y adaptadores, limpia, cebolla. Son variaciones del mismo principio. Si buscas una sola lectura, el artículo original de Alistair Cockburn sobre hexagonal es corto y está pensado para gente que no es programadora de oficio.
