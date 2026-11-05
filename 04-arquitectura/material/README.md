# Material complementario del Taller 4

Archivos de referencia para seguir la guía. La guía está hecha para que construyas el proyecto tú mismo; estos sirven para comparar cuando algo no funciona.

## Qué hay adentro

`modulo_1/app_acoplada.py` es el punto de partida del Módulo 1: la etapa 2 del muñeco con transporte, traducción, reglas y decisiones en un solo archivo. Se levanta con `uvicorn app_acoplada:app --port 8002` desde `modulo_1/` y cumple el contrato del Taller 3.

`etapa-limpiar/` es el proyecto terminado al final del Módulo 5, sin los ejercicios 4.7 y 5.4 (esa solución está en la carpeta del facilitador). Incluye los fixtures de la etapa 2 del Taller 3 en `tests/fixtures/` y los tres registros de decisión en `docs/decisiones/`.

## Correr el proyecto de referencia

Con un entorno virtual activo:

```powershell
cd etapa-limpiar
pip install -e ".[http,parquet,dev]"
pytest
python -m limpieza.adaptadores.cli ..\..\..\02-orquestacion-con-kedro\material\datos\encuesta_hogares.csv salida\encuesta_limpia.csv
uvicorn limpieza.adaptadores.http:app --port 8002
```

`pytest` reporta veinte pruebas en verde. La terminal informa 15 duplicados, 6 atípicos y 27 imputaciones, los mismos números de los talleres 2 y 3. Con el servicio arriba, el probador del muñeco (`python -m ensamblador.probar --etapa 2` desde el repositorio del Taller 3) responde que cumple el contrato.

## Correspondencia con la guía

| Sección de la guía | Archivo de referencia |
|----|----|
| 1.1 a 1.3 | `modulo_1/app_acoplada.py` |
| 2.1 Proyecto instalable | `etapa-limpiar/pyproject.toml` |
| 2.2 y 2.3 Política y reglas | `etapa-limpiar/src/limpieza/dominio/politica.py` y `reglas.py` |
| 2.4 Pruebas del dominio | `etapa-limpiar/tests/conftest.py` y `tests/dominio/test_reglas.py` |
| 2.5 a 2.7 Puertos y caso de uso | `etapa-limpiar/src/limpieza/dominio/puertos.py`, `aplicacion/limpiar_encuesta.py` y `tests/aplicacion/` |
| 3.2 a 3.6 Adaptadores | `etapa-limpiar/src/limpieza/adaptadores/` y `tests/adaptadores/` |
| 4.4 Strategy | `etapa-limpiar/src/limpieza/dominio/imputacion.py`, los cambios en `politica.py` y `reglas.py`, y `tests/dominio/test_imputacion.py` |
| 4.5 Factory | `etapa-limpiar/src/limpieza/adaptadores/fabrica.py`, `parquet.py`, `cli.py` y `tests/adaptadores/test_fabrica.py` |
| 5.2 Registros de decisión | `etapa-limpiar/docs/decisiones/` |
