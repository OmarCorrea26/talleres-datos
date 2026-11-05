# Material complementario del Taller 2

Archivos de referencia para seguir la guía. La idea no es copiarlos: la guía está hecha para que escribas cada archivo tú mismo, y estos sirven para comparar cuando algo no funciona o para regenerar el proyecto rápido si vuelves meses después.

## Qué hay adentro

`datos/encuesta_hogares.csv` es la encuesta sintética con la que se trabaja todo el taller, y `datos/generar_encuesta.py` la produce con semilla fija: si la corres, obtienes exactamente el mismo archivo.

`modulo_1/proceso_monolito.py` es el "antes" del Módulo 1: el proceso completo en un solo script, con sus rutas escritas a mano y sus números sueltos. Córrelo desde esta carpeta con `python modulo_1/proceso_monolito.py`.

`encuesta-hogares/` es el proyecto Kedro terminado tal como queda al final del Módulo 3, incluida la variante `estimacion_rural`, el hook y las pruebas. No incluye la encuesta en `data/01_raw` (cópiala desde `datos/`) ni la solución del ejercicio del Módulo 4.

## Correr el proyecto de referencia

Desde esta carpeta, con el entorno `.venv-kedro` del Módulo 0 activo:

```powershell
cd encuesta-hogares
pip install -r requirements.txt
copy ..\datos\encuesta_hogares.csv data\01_raw\
kedro run
pytest
```

`kedro run` completa siete tareas y deja los tabulados en `data/08_reporting/tabulados.xlsx`. `pytest` reporta cinco pruebas en verde.

## Correspondencia con la guía

| Sección de la guía | Archivo de referencia |
|----|----|
| 1.1 El script que creció | `modulo_1/proceso_monolito.py` |
| 1.6 Catálogo | `encuesta-hogares/conf/base/catalog.yml` |
| 2.2 a 2.4 Nodos y pipeline de preparación | `encuesta-hogares/src/encuesta_hogares/pipelines/preparacion/` y `conf/base/parameters_preparacion.yml` |
| 2.8 Pipeline de estimación | `encuesta-hogares/src/encuesta_hogares/pipelines/estimacion/` y `conf/base/parameters_estimacion.yml` |
| 2.9 Namespaces | `encuesta-hogares/src/encuesta_hogares/pipeline_registry.py` |
| 2.10 Hooks | `encuesta-hogares/src/encuesta_hogares/hooks.py` y `settings.py` |
| 3.2 a 3.4 Pruebas | `encuesta-hogares/pyproject.toml` y `encuesta-hogares/tests/` |
