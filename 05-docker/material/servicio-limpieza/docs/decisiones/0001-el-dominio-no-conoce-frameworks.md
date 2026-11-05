# 0001. El dominio no importa ningún framework ni toca archivos

Fecha: 2026-11-05
Estado: aceptada

## Contexto

La etapa de limpieza nació dentro de un servicio FastAPI, con las reglas estadísticas mezcladas con la lectura del JSON y las rutas HTTP. Cada vez que cambiaba el transporte (una versión nueva de FastAPI, una petición con otra forma) había que tocar el mismo archivo donde viven las reglas, y para probar una regla había que levantar un servidor.

## Decisión

Todo lo que sea regla de limpieza vive en `limpieza/dominio/` y solo puede importar `pandas` y la biblioteca estándar. Está prohibido importar `fastapi`, `kedro`, `argparse` o cualquier cosa que lea o escriba archivos. Lo que el dominio necesite del exterior lo pide a través de un puerto (`puertos.py`).

## Consecuencias

Ganamos pruebas del dominio que corren en milisegundos con cinco filas, y la posibilidad de servir la misma limpieza por HTTP, por Kedro y por terminal sin duplicarla. Pagamos una capa más de archivos y la disciplina de preguntarse, en cada cambio, si lo que estamos escribiendo es regla o es transporte. Esa pregunta es, justamente, el punto.
