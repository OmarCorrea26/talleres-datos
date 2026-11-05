# Módulo 3 — Adaptadores: la misma limpieza por cuatro caminos

Objetivo: escribir un adaptador por cada forma de usar la limpieza (archivos, terminal, HTTP y Kedro), comprobar que ninguno contiene reglas, y cerrar con el probador del muñeco diciendo "cumple el contrato". Dos horas.

### Lo que necesitas antes de empezar

- El dominio y el caso de uso del Módulo 2 con `7 passed`.
- Los fixtures de la etapa 2 del Taller 3: `etapa_2_entrada.json` y `etapa_2_salida.json`. Están en `material/etapa-limpiar/tests/fixtures/` y en tu clon del muñeco.

## 3.1 Qué es y qué no es un adaptador

Un adaptador hace exactamente dos cosas. Traduce lo que recibe del exterior al idioma del dominio, y traduce lo que el dominio devuelve al idioma de quien llamó. Nada más. Si en un adaptador aparece un `groupby` que calcula algo, o una constante como `0.99`, se coló una regla o una decisión donde no va.

Vas a escribir cuatro, y cada uno te va a mostrar un ángulo distinto. Los de archivos implementan los puertos. El de terminal arma el caso de uso con esos adaptadores. El de HTTP no usa el caso de uso, porque no lee ni escribe nada: traduce JSON y llama al dominio directo. Y el de Kedro es una función de cinco líneas, porque un nodo ya es casi un dominio.

Deja `src/limpieza/adaptadores/__init__.py` con el mapa de lo que viene:

```python
"""Adaptadores: cada forma de entrar y salir del dominio, una por archivo.

    archivos.py        CSV de entrada, CSV y JSON de salida (cumplen los puertos)
    contrato_json.py   traducción entre el JSON del contrato del Taller 3 y DataFrames
    http.py            el servicio FastAPI con las rutas del muñeco
    kedro.py           la función lista para usarse como nodo en el Taller 2
    cli.py             la línea de comandos

Ninguno contiene reglas de limpieza. Si encuentras una aquí, está en el lugar
equivocado.
"""
```

## 3.2 Archivos: implementar los puertos

`src/limpieza/adaptadores/archivos.py`:

```python
"""Adaptadores de archivos: leen y escriben en disco cumpliendo los puertos del dominio."""

import json
from pathlib import Path

import pandas as pd

from limpieza.dominio import ResumenLimpieza


class LectorCSV:
    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def leer(self) -> pd.DataFrame:
        df = pd.read_csv(self._ruta)
        df["ocupado"] = df["ocupado"].astype("Int64")
        return df


class EscritorCSV:
    """Escribe la encuesta limpia como CSV y el resumen como JSON al lado."""

    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def escribir(self, encuesta: pd.DataFrame, resumen: ResumenLimpieza) -> None:
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        encuesta.to_csv(self._ruta, index=False)
        ruta_resumen = self._ruta.with_name(self._ruta.stem + "_resumen.json")
        ruta_resumen.write_text(json.dumps(resumen.como_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
```

`LectorCSV` tiene un método `leer()` que devuelve un DataFrame: cumple `LectorDeEncuesta`. `EscritorCSV` tiene `escribir(encuesta, resumen)`: cumple `EscritorDeEncuesta`. Ninguno hereda de nada y ninguno importa los puertos; los cumple por tener la forma correcta.

Observa la línea del `astype("Int64")` en el lector. Es traducción, no regla: el CSV no sabe de enteros con vacíos y el dominio los necesita. Esa es la frontera exacta entre un formato y las reglas.

## 3.3 Terminal: armar el caso de uso

`src/limpieza/adaptadores/cli.py`:

```python
"""Adaptador de línea de comandos: limpiar un CSV y dejar otro al lado.

Ejecutar:  python -m limpieza.adaptadores.cli entrada.csv salida.csv --percentil 0.99
"""

import argparse
from pathlib import Path

from limpieza.adaptadores.archivos import EscritorCSV, LectorCSV
from limpieza.aplicacion import LimpiarEncuesta
from limpieza.dominio import PoliticaDeLimpieza


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Limpia la encuesta de hogares: duplicados, atípicos e imputación.")
    parser.add_argument("entrada", type=Path, help="CSV con la encuesta validada")
    parser.add_argument("salida", type=Path, help="CSV donde dejar la encuesta limpia")
    parser.add_argument("--percentil", type=float, default=0.99, help="percentil para recortar atípicos")
    parser.add_argument("--grupos", nargs="+", default=["area", "sexo"], help="columnas que definen el grupo de imputación")
    return parser


def main(argumentos: list[str] | None = None) -> int:
    opciones = construir_parser().parse_args(argumentos)
    politica = PoliticaDeLimpieza(percentil_atipicos=opciones.percentil, grupos_imputacion=tuple(opciones.grupos))
    caso_de_uso = LimpiarEncuesta(LectorCSV(opciones.entrada), EscritorCSV(opciones.salida), politica)
    resumen = caso_de_uso.ejecutar()
    print(
        f"{resumen.n_entrada} filas leídas, {resumen.n_duplicados_eliminados} duplicados eliminados, "
        f"{resumen.n_atipicos_ajustados} atípicos recortados, {resumen.n_imputados} ingresos imputados. "
        f"Salida: {opciones.salida}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Aquí está la inyección de dependencias en acción: la línea que construye `LimpiarEncuesta` decide que hoy el lector es un CSV y el escritor es otro CSV. Mañana puede ser una tabla de SQL y el caso de uso no se entera.

Pruébalo con la encuesta del Taller 2 (ajusta la ruta a donde la tengas):

```powershell
python -m limpieza.adaptadores.cli ..\ruta\al\material\datos\encuesta_hogares.csv salida\encuesta_limpia.csv
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> La terminal dice `1215 filas leídas, 15 duplicados eliminados, 6 atípicos recortados, 27 ingresos imputados`. Son los mismos números del Taller 2 y del Taller 3, porque son las mismas reglas. En `salida/` quedaron el CSV y `encuesta_limpia_resumen.json`.

Prueba también `--percentil 0.95`: el resumen cambia su descripción solo, porque la política se describe a sí misma.

## 3.4 HTTP: el contrato del muñeco, sin reglas adentro

Primero la traducción, porque es la parte que más se confunde con reglas. `src/limpieza/adaptadores/contrato_json.py`:

```python
"""Traducción entre el contrato JSON del Taller 3 y los DataFrames del dominio.

El contrato dice: entra {"registros": [...]} y sale {"registros": [...], "resumen": {...}}.
Esa forma es cosa del transporte, no de las reglas de limpieza, y por eso la
traducción vive en un adaptador y no en el dominio.
"""

import pandas as pd

from limpieza.dominio import ResultadoLimpieza


def registros_a_dataframe(registros: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(registros)
    df["ocupado"] = df["ocupado"].astype("Int64")
    df["ingreso"] = pd.to_numeric(df["ingreso"], errors="coerce")
    return df


def dataframe_a_registros(df: pd.DataFrame) -> list[dict]:
    # JSON no tiene NaN: los vacíos deben salir como null
    return df.astype(object).where(df.notna(), None).to_dict(orient="records")


def resultado_a_salida(resultado: ResultadoLimpieza) -> dict:
    return {
        "registros": dataframe_a_registros(resultado.encuesta),
        "resumen": resultado.resumen.como_dict(),
    }
```

Esas líneas estaban en `app_acoplada.py` mezcladas con el `drop_duplicates`. Aquí tienen archivo propio, y la palabra `registros` aparece por primera vez en el proyecto: en un adaptador, que es donde el contrato del Taller 3 tiene derecho a existir.

Ahora el servicio, `src/limpieza/adaptadores/http.py`:

```python
"""Adaptador HTTP: la etapa 2 del muñeco, servida con FastAPI.

Ejecutar:  uvicorn limpieza.adaptadores.http:app --port 8002 --reload

Las rutas son las mismas del Taller 3 (GET /salud y POST /procesar), de modo
que el ensamblador del muñeco no nota la diferencia. Lo único que hace este
archivo es traducir: JSON a DataFrame, dominio, DataFrame a JSON.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from limpieza.adaptadores.contrato_json import registros_a_dataframe, resultado_a_salida
from limpieza.dominio import PoliticaDeLimpieza, limpiar

NUMERO = 2
NOMBRE = "limpiar"


class Entrada(BaseModel):
    registros: list[dict]
    politica: dict | None = None


app = FastAPI(
    title=f"Etapa {NUMERO} — {NOMBRE}",
    description="Eliminación de duplicados, tratamiento de atípicos e imputación de ingreso",
    version="1.0.0",
)


@app.get("/salud")
def salud():
    return {"etapa": NUMERO, "nombre": NOMBRE, "estado": "ok"}


@app.post("/procesar")
def procesar(entrada: Entrada):
    if not entrada.registros:
        raise HTTPException(status_code=422, detail="registros no puede estar vacío")
    politica = PoliticaDeLimpieza.desde_dict(entrada.politica or {})
    resultado = limpiar(registros_a_dataframe(entrada.registros), politica)
    return resultado_a_salida(resultado)
```

Compara `procesar` con la de `app_acoplada.py`. De treinta líneas quedaron cuatro, y las cuatro son traducción o llamada al dominio. De paso ganó algo que la versión acoplada no tenía: la petición puede traer una `politica`, de modo que metodología prueba el percentil 95 desde `/docs` sin que nadie edite código.

```powershell
uvicorn limpieza.adaptadores.http:app --port 8002 --reload
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `http://localhost:8002/docs` muestra `/salud` y `/procesar`, y `/procesar` acepta el cuerpo de la sección 1.1 del Módulo 1 con el mismo resultado de entonces.

## 3.5 Probar el adaptador HTTP contra los fixtures del Taller 3

Copia `etapa_2_entrada.json` y `etapa_2_salida.json` a `tests/fixtures/`. Después, `tests/adaptadores/test_http.py`:

```python
"""El adaptador HTTP cumple el contrato del Taller 3, verificado contra sus fixtures."""

import json
from collections import Counter
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from limpieza.adaptadores.http import app

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture(scope="module")
def cliente():
    return TestClient(app)


def test_salud(cliente):
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"etapa": 2, "nombre": "limpiar", "estado": "ok"}


def test_procesar_reproduce_el_resumen_de_referencia(cliente):
    entrada = json.loads((FIXTURES / "etapa_2_entrada.json").read_text(encoding="utf-8"))
    referencia = json.loads((FIXTURES / "etapa_2_salida.json").read_text(encoding="utf-8"))

    respuesta = cliente.post("/procesar", json=entrada)

    assert respuesta.status_code == 200
    salida = respuesta.json()
    assert salida["resumen"] == referencia["resumen"]
    assert len(salida["registros"]) == referencia["resumen"]["n_salida"]


def test_procesar_cumple_las_reglas_del_contrato(cliente):
    """Las mismas verificaciones que hace validar_etapa_2 en el muñeco."""
    entrada = json.loads((FIXTURES / "etapa_2_entrada.json").read_text(encoding="utf-8"))
    salida = cliente.post("/procesar", json=entrada).json()
    registros = salida["registros"]

    assert all(c == 1 for c in Counter(r["id_persona"] for r in registros).values())
    assert not any(r["ocupado"] == 1 and r["ingreso"] is None for r in registros)
    assert sum(1 for r in registros if r["ingreso_imputado"]) == salida["resumen"]["n_imputados"]
    assert max(r["ingreso"] for r in registros if r["ingreso"] is not None) <= 20_000_000


def test_procesar_rechaza_una_entrada_vacia(cliente):
    assert cliente.post("/procesar", json={"registros": []}).status_code == 422


def test_la_politica_viaja_en_la_peticion(cliente):
    entrada = json.loads((FIXTURES / "etapa_2_entrada.json").read_text(encoding="utf-8"))
    entrada["politica"] = {"percentil_atipicos": 0.9}
    salida = cliente.post("/procesar", json=entrada).json()
    assert "percentil 90" in salida["resumen"]["metodo_imputacion"]
```

`TestClient` levanta la aplicación en memoria: no hay puerto, no hay servidor, y la prueba corre en medio segundo. La segunda prueba es la que importa: el resumen que produce tu adaptador es idéntico, campo por campo, al fixture de referencia del Taller 3.

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `12 passed`.

> [!NOTE]
> **📘 Concepto**
>
> Si hiciste el ejercicio 2.8, la segunda prueba te acaba de fallar: el resumen tiene un campo `n_edades_descartadas` que el fixture no tiene. No es un error del código, es el contrato hablando. Tienes tres salidas y ninguna es "borrar la regla": que el adaptador HTTP omita el campo al traducir (el contrato manda, el dominio sabe más de lo que publica), que el contrato cambie por Pull Request etiquetado `contrato` como en el Taller 3, o que la regla nueva sea opcional en la política. Decidirlo es arquitectura. Aquí, lo más honesto es la primera opción, y dejar escrito por qué en el Módulo 5.

## 3.6 Kedro: cinco líneas, sin instalar Kedro

`src/limpieza/adaptadores/kedro.py`:

```python
"""Adaptador Kedro: la misma limpieza como nodo del pipeline del Taller 2.

Un nodo de Kedro es una función con DataFrames y diccionarios de entrada y
salida. Esta función traduce el diccionario de parámetros del YAML a una
política del dominio y devuelve lo que el catálogo espera. Para usarla en el
proyecto encuesta_hogares basta con importarla en pipeline.py:

    from limpieza.adaptadores.kedro import nodo_limpiar
    node(func=nodo_limpiar, inputs=["encuesta_validada", "params:limpieza"],
         outputs=["encuesta_limpia", "resumen_limpieza"], name="limpiar")

No importa kedro: no hace falta, y así el adaptador se prueba sin instalarlo.
"""

import pandas as pd

from limpieza.dominio import PoliticaDeLimpieza, limpiar


def nodo_limpiar(encuesta: pd.DataFrame, parametros: dict) -> tuple[pd.DataFrame, dict]:
    politica = PoliticaDeLimpieza.desde_dict(parametros)
    resultado = limpiar(encuesta, politica)
    return resultado.encuesta, resultado.resumen.como_dict()
```

Si vuelves al `limpiar` que escribiste en el Taller 2, vas a ver que ese nodo era, sin saberlo, dominio y adaptador juntos: hacía las reglas y además traducía el diccionario de parámetros. Ahora las reglas viven en un paquete que el proyecto Kedro puede instalar con `pip install -e ../etapa-limpiar`, y el nodo se reduce a la traducción. Es la misma regla de la dependencia, aplicada a un framework que ya te resultaba cómodo.

Pruébalo junto con la terminal, en `tests/adaptadores/test_kedro_y_cli.py`:

```python
"""Los otros dos adaptadores: el nodo para Kedro y la línea de comandos."""

import json

import pandas as pd

from limpieza.adaptadores.cli import main
from limpieza.adaptadores.kedro import nodo_limpiar


def test_el_nodo_devuelve_lo_que_el_catalogo_espera(encuesta_minima):
    encuesta, resumen = nodo_limpiar(encuesta_minima, {"percentil_atipicos": 0.5, "grupos_imputacion": ["area", "sexo"]})
    assert isinstance(encuesta, pd.DataFrame)
    assert isinstance(resumen, dict)
    assert resumen["n_salida"] == 4


def test_la_cli_deja_el_csv_y_el_resumen(tmp_path, encuesta_minima):
    entrada = tmp_path / "entrada.csv"
    salida = tmp_path / "limpia" / "encuesta_limpia.csv"
    encuesta_minima.to_csv(entrada, index=False)

    codigo = main([str(entrada), str(salida), "--percentil", "0.5"])

    assert codigo == 0
    assert len(pd.read_csv(salida)) == 4
    resumen = json.loads((tmp_path / "limpia" / "encuesta_limpia_resumen.json").read_text(encoding="utf-8"))
    assert resumen["n_duplicados_eliminados"] == 1
```

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `14 passed`. Seis del dominio, una del caso de uso, cinco del adaptador HTTP y dos de los otros adaptadores. Cuatro caminos de entrada, una sola implementación de las reglas.

## 3.7 El mapa de dependencias

Antes de seguir, comprueba la regla de la dependencia con un comando. Busca qué importa cada capa:

```powershell
findstr /s /n "^from ^import" src\limpieza\dominio\*.py
findstr /s /n "^from ^import" src\limpieza\adaptadores\*.py
```

En macOS o Linux, `grep -rn "^from\|^import" src/limpieza/dominio`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> En `dominio/` solo aparecen `dataclasses`, `typing`, `pandas` y módulos del propio dominio. En `adaptadores/` aparecen `fastapi`, `argparse`, `json` y `limpieza.dominio`, nunca otro adaptador. Si un archivo de `dominio/` importa algo de `adaptadores/` o de `fastapi`, hay que sacarlo antes de continuar.

## 3.8 La prueba de fuego: el muñeco no nota la diferencia

Si tienes el repositorio del muñeco del Taller 3 clonado, levanta tu adaptador HTTP en el puerto 8002 y, desde la carpeta del muñeco y con su propio entorno, corre su probador:

```powershell
python -m ensamblador.probar --etapa 2
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `[OK] Etapa 2 (limpiar, torso) en http://localhost:8002` y `Cumple el contrato`. El ensamblador del Taller 3 acaba de validar una etapa que no vive en su repositorio, que no usa su fábrica de servicios y cuyas reglas están en un paquete aparte con pruebas propias. Ese es el punto del taller en una línea de salida.

## 3.9 Ejercicio práctico: un quinto adaptador

Escribe `adaptadores/parquet.py` con un `LectorParquet` y un `EscritorParquet` que cumplan los puertos, y agrega a la terminal una opción `--formato csv|parquet` que elija qué adaptadores inyectar. Instala `pyarrow` para poder escribir Parquet. Lo que debes notar al terminar: no tocaste `dominio/` ni `aplicacion/`, y el pedido "el muñeco pasa a Parquet" de la tabla del Módulo 1 acaba de costarte un archivo nuevo y tres líneas en otro. En el Módulo 4 vas a ver cómo quitar incluso la opción `--formato`.

## 3.10 Troubleshooting del Módulo 3

| Síntoma | Causa probable | Solución |
|----|----|----|
| `python -m limpieza.adaptadores.cli` dice `No module named limpieza` | El proyecto no está instalado en este entorno | `pip install -e ".[http,dev]"` desde la raíz del proyecto |
| `uvicorn` arranca pero `/procesar` devuelve 422 con el fixture | El fixture tiene una llave que `Entrada` no acepta, o está vacío | `Entrada` admite `registros` y `politica`; verifica que el JSON tenga `registros` con elementos |
| `test_procesar_reproduce_el_resumen_de_referencia` falla por `metodo_imputacion` | Cambiaste el texto de `descripcion` en la política | Debe producir exactamente `mediana del ingreso de ocupados por area x sexo; atipicos recortados al percentil 99` |
| El mismo test falla por un campo de más en el resumen | Hiciste el ejercicio 2.8 | Lee el concepto de la sección 3.5 y decide |
| `TestClient` no se importa | Falta `httpx` | `pip install httpx`, o reinstala con `".[http,dev]"` |
| El probador del muñeco dice "no responde" | El servicio no está en 8002 o lo cerraste | Déjalo corriendo en una terminal aparte mientras pruebas |

## 3.11 Para profundizar (opcional)

- Instala este paquete dentro del entorno de tu proyecto Kedro del Taller 2 con `pip install -e ..\etapa-limpiar` y reemplaza el nodo `limpiar` por `nodo_limpiar`. `kedro run` debe dar exactamente los mismos tabulados.
- Mira cómo el ensamblador del Taller 3 valida las etapas (`contrato/validaciones.py`). Es un adaptador también: traduce "cumple el contrato" a un muñeco verde.
