# Módulo 3 — Calidad y entrega: pruebas, repositorio y empaquetado

Objetivo: que el proyecto tenga pruebas automáticas que cualquiera pueda correr, que viva en un repositorio de GitHub con un README útil y que se pueda instalar en otra máquina. Hora y media.

### Lo que necesitas antes de empezar

- Los dos pipelines del Módulo 2 corriendo con `kedro run` y los siete nodos completos.
- Git configurado con tu nombre y correo, y tu cuenta de GitHub (Módulo 3 del Taller 1).

## 3.1 Por qué probar un pipeline

En el monolito, la única prueba posible era correrlo entero y mirar el Excel. Si el resultado se veía razonable, se daba por bueno. Esa forma de verificar tiene dos problemas: es lenta, y no te dice dónde está el error cuando lo hay.

Los nodos cambian eso. Como cada uno es una función que recibe un DataFrame y devuelve otro, puedes llamarlo con cinco filas inventadas en las que sabes exactamente qué debe pasar: dos duplicados que deben desaparecer, un ocupado sin ingreso que debe recibir la mediana, dos departamentos cuyos factores deben sumar un total conocido. Si el nodo hace lo que debe con cinco filas, lo hará con un millón.

> [!NOTE]
> **📘 Concepto**
>
> Hay dos niveles de prueba y conviene tener ambos. La prueba de nodo verifica una función aislada con datos mínimos: es rápida y señala con precisión qué se rompió. La prueba de pipeline corre varios nodos encadenados, también con datos mínimos y en memoria, y verifica que el ensamble sea correcto: que los nombres de entradas y salidas encajen y que el resultado final tenga lo esperado. Ninguna de las dos toca `data/`.

## 3.2 Preparar pytest

Cuando creaste el proyecto con `--tools=test`, Kedro dejó pytest configurado en `pyproject.toml`. Falta un ajuste. Abre el archivo, busca la sección `[tool.pytest.ini_options]` y déjala así:

```toml
[tool.pytest.ini_options]
addopts = "-ra"
pythonpath = ["src"]
```

La línea `pythonpath` le dice a pytest dónde está el paquete `encuesta_hogares`, de manera que las pruebas puedan importarlo sin instalar el proyecto. La opción original incluía cobertura de código con un plugin que no instalamos; si más adelante quieres medir cobertura, `pip install pytest-cov` y la restauras.

## 3.3 Prueba de nodo

Kedro creó `tests/pipelines/preparacion/test_pipeline.py` como marcador. Déjalo por ahora y crea al lado `tests/pipelines/preparacion/test_nodes.py`:

```python
"""Pruebas de los nodos de preparación.

Cada prueba arma un DataFrame pequeño a mano, llama al nodo como a cualquier
función de Python y verifica una sola cosa. No hace falta Kedro para esto.
"""

import pandas as pd
import pytest

from encuesta_hogares.pipelines.preparacion.nodes import calibrar, limpiar, validar


@pytest.fixture
def encuesta_minima() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id_persona": [1, 2, 3, 3, 4],
            "id_hogar": [1, 1, 2, 2, 3],
            "departamento": ["Bogota", "Bogota", "Valle", "Valle", "Valle"],
            "area": ["Urbana", "Urbana", "Rural", "Rural", "Rural"],
            "sexo": ["H", "M", "H", "H", "M"],
            "edad": [30, 40, 25, 25, 10],
            "ocupado": [1, 1, 1, 1, None],
            "ingreso": [1_000_000, None, 2_000_000, 2_000_000, None],
            "factor_expansion": [100.0, 100.0, 50.0, 50.0, 50.0],
        }
    )


def test_validar_falla_si_falta_una_columna(encuesta_minima):
    sin_columna = encuesta_minima.drop(columns=["ingreso"])
    with pytest.raises(ValueError, match="ingreso"):
        validar(sin_columna)


def test_validar_cuenta_nulos(encuesta_minima):
    _, resumen = validar(encuesta_minima)
    assert resumen["n_filas"] == 5
    assert resumen["n_nulos_por_columna"]["ingreso"] == 2
    assert resumen["n_nulos_por_columna"]["ocupado"] == 1


def test_limpiar_elimina_duplicados_e_imputa(encuesta_minima):
    validada, _ = validar(encuesta_minima)
    parametros = {"percentil_atipicos": 0.99, "grupos_imputacion": ["area", "sexo"]}
    limpia, resumen = limpiar(validada, parametros)

    assert resumen["n_duplicados_eliminados"] == 1
    assert len(limpia) == 4
    assert resumen["n_imputados"] == 1
    assert limpia["ingreso_imputado"].sum() == 1
    # El ocupado sin ingreso era mujer urbana: la mediana de su grupo es la suya misma,
    # y como no hay otra, la imputación queda vacía. Eso también se verifica.
    assert limpia.loc[limpia["id_persona"] == 2, "ingreso"].isna().all()


def test_calibrar_reproduce_la_poblacion_objetivo(encuesta_minima):
    validada, _ = validar(encuesta_minima)
    limpia, _ = limpiar(validada, {"percentil_atipicos": 0.99, "grupos_imputacion": ["area", "sexo"]})
    objetivo = {"Bogota": 1000, "Valle": 500}

    calibrada, resumen = calibrar(limpia, objetivo)

    totales = calibrada.groupby("departamento")["factor_calibrado"].sum()
    assert totales["Bogota"] == pytest.approx(1000)
    assert totales["Valle"] == pytest.approx(500)
    assert resumen["razon_de_ajuste"]["Bogota"] == pytest.approx(5.0)
```

Fíjate en el patrón de cada prueba: preparar datos mínimos, llamar al nodo, afirmar una cosa concreta. El `fixture` evita repetir el DataFrame en cada prueba. Y mira la tercera prueba con atención: documenta un caso límite real, el de un grupo donde no hay con qué imputar. Una prueba también es documentación.

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `4 passed`. Si ves `ModuleNotFoundError: No module named 'encuesta_hogares'`, falta la línea `pythonpath` de la sección 3.2.

## 3.4 Prueba de pipeline con `SequentialRunner`

Ahora el segundo nivel. Reemplaza el contenido de `tests/pipelines/preparacion/test_pipeline.py`:

```python
"""Prueba del pipeline de preparación completo, de nodo en nodo, sin tocar disco.

Se arma un catálogo en memoria con la entrada y los parámetros, y se corre el
pipeline con SequentialRunner. Lo que se verifica es la salida final.
"""

import pandas as pd
from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner

from encuesta_hogares.pipelines.preparacion import create_pipeline


def test_pipeline_preparacion_deja_una_base_calibrada():
    encuesta = pd.DataFrame(
        {
            "id_persona": [1, 2, 3, 4],
            "id_hogar": [1, 1, 2, 2],
            "departamento": ["Bogota", "Bogota", "Valle", "Valle"],
            "area": ["Urbana", "Urbana", "Rural", "Rural"],
            "sexo": ["H", "M", "H", "M"],
            "edad": [30, 40, 25, 50],
            "ocupado": [1, 0, 1, 1],
            "ingreso": [1_000_000, None, 2_000_000, 1_500_000],
            "factor_expansion": [100.0, 100.0, 50.0, 50.0],
        }
    )
    catalogo = DataCatalog(
        {
            "encuesta_cruda": MemoryDataset(encuesta),
            "params:limpieza": MemoryDataset({"percentil_atipicos": 0.99, "grupos_imputacion": ["area", "sexo"]}),
            "params:poblacion_objetivo": MemoryDataset({"Bogota": 2000, "Valle": 300}),
        }
    )

    # El runner devuelve las salidas libres del pipeline como datasets en memoria
    salida = SequentialRunner().run(create_pipeline(), catalogo)

    calibrada = salida["encuesta_calibrada"].load()
    assert "factor_calibrado" in calibrada.columns
    assert calibrada.groupby("departamento")["factor_calibrado"].sum().round(6).to_dict() == {
        "Bogota": 2000.0,
        "Valle": 300.0,
    }
    assert salida["resumen_limpieza"].load()["n_duplicados_eliminados"] == 0
```

Aquí el catálogo no sale del YAML sino que se arma en memoria, con `MemoryDataset` para la entrada y para cada bloque de parámetros. El runner corre los tres nodos en orden y devuelve lo que no consumió nadie: la base calibrada y los resúmenes. Observa el `.load()`: el runner entrega datasets, no DataFrames, y hay que pedirles el contenido.

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `5 passed`. Acabas de verificar el pipeline completo en menos de dos segundos y sin escribir un solo archivo.

## 3.5 El repositorio del proyecto

Tal como aprendiste en el Taller 1, un proyecto que no está en Git no existe. Kedro ya dejó un `.gitignore` pensado para esto. Ábrelo y busca tres cosas: `data/**` seguido de `!data/**/` (se ignoran los datos pero no las carpetas vacías), `conf/local/**` (se ignora lo local) y `.viz` (la caché de Kedro-Viz). Es exactamente lo que no debe subirse.

> [!NOTE]
> **📘 Concepto**
>
> ¿Por qué no subir los datos? Porque el repositorio es para el proceso, no para sus insumos. La encuesta puede pesar gigas, puede ser confidencial y en todo caso no cambia con el código. Lo que sí sube es el catálogo, que dice dónde se espera cada dato. Quien clone el repositorio copia la encuesta a `data/01_raw` y todo funciona. En el Taller 3 vas a ver cómo se comparten datos de prueba pequeños cuando sí hacen falta.

Desde la raíz del proyecto:

```powershell
git init
git add .
git status
```

Revisa el `status` antes de confirmar: no debe aparecer nada de `data/` salvo los `.gitkeep`, ni nada de `conf/local`. Si aparece, detente y revisa el `.gitignore`.

```powershell
git commit -m "Proyecto Kedro de la encuesta de hogares: preparación y estimación"
```

Crea el repositorio en GitHub con el nombre `kedro-encuesta-<tu-nombre>`, vacío, sin README ni licencia, y conéctalo:

```powershell
git remote add origin https://github.com/<tu-usuario>/kedro-encuesta-<tu-nombre>.git
git branch -M main
git push -u origin main
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> En GitHub se ven `conf`, `src`, `tests`, `pyproject.toml` y `requirements.txt`. En `data/` solo hay carpetas con `.gitkeep`. No hay archivos `.parquet`, `.xlsx` ni `credentials.yml`.

## 3.6 Un README que sirva

Reemplaza el `README.md` que Kedro generó, que habla de Kedro en general, por uno que hable de tu proyecto. Lo mínimo que debe responder, en este orden: qué hace el proyecto en dos frases, cómo instalarlo, de dónde sacar la encuesta y dónde ponerla, cómo correrlo y cómo probarlo. Si lo tienes a la mano, un diagrama del linaje exportado desde Kedro-Viz vale más que tres párrafos.

Usa de guía el README del proyecto de referencia en `material/encuesta-hogares`, pero escríbelo con tus palabras y con tus rutas.

```powershell
git add README.md
git commit -m "Documentar instalación, corrida y pruebas"
git push
```

## 3.7 Empaquetar (opcional)

Kedro puede construir el proyecto como un paquete instalable, de manera que un servidor o un compañero lo instale con `pip` y lo corra sin clonar nada:

```powershell
pip install build
kedro package
```

Deja dos archivos en `dist/`: una rueda de Python con el código y un comprimido con la configuración de `conf/base`. No lo vas a necesitar en este taller, sin embargo conviene saber que existe: es el puente entre "corre en mi máquina" y "corre en producción", y es el camino que el taller de Docker retoma.

## 3.8 Ejercicio práctico: una prueba para tu nodo

Escribe una prueba para el nodo `contar_hogares` del ejercicio 2.12. Arma un DataFrame con tres o cuatro filas donde un hogar se repita, y afirma que el conteo no lo cuente dos veces. Agrégala a `test_nodes.py`, corre `pytest` y haz commit con un mensaje que diga qué probaste.

## 3.9 Troubleshooting del Módulo 3

| Síntoma | Causa probable | Solución |
|----|----|----|
| `ModuleNotFoundError: No module named 'encuesta_hogares'` | Falta `pythonpath = ["src"]` | Sección 3.2 |
| `unrecognized arguments: --cov` | `addopts` quedó con la opción de cobertura | Déjalo en `"-ra"` o instala `pytest-cov` |
| `AttributeError: 'MemoryDataset' object has no attribute 'columns'` | Olvidaste el `.load()` sobre la salida del runner | Sección 3.4 |
| `git status` muestra archivos `.parquet` | El `.gitignore` se dañó o corriste `git init` en otra carpeta | Verifica que estás en la raíz del proyecto y que `.gitignore` tiene `data/**` |
| `kedro package` falla con `No module named build` | Falta el paquete `build` | `pip install build` |

## 3.10 Para profundizar (opcional)

- Agrega pruebas para los nodos de estimación. El más interesante es `_error_estandar`: con pesos iguales debe coincidir con la fórmula clásica del error estándar de la media.
- En el Taller 3 vas a ver GitHub Actions corriendo `pytest` en cada Pull Request. Si quieres adelantarte, busca "GitHub Actions python pytest" y arma un flujo mínimo para este repositorio.
