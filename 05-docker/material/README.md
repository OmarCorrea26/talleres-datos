# Material complementario del Taller 5

Archivos de referencia para seguir la guía. La guía está hecha para que escribas los Dockerfiles sobre tus propios proyectos; estas copias sirven para comparar y para que el taller funcione aunque no tengas los anteriores a la mano.

## Qué hay adentro

`script-del-taller-2/` es el monolito del Taller 2 con la encuesta sintética. Se usa en el Módulo 1 para correrlo dentro de un contenedor de Python sin instalar nada en tu máquina.

`servicio-limpieza/` es el proyecto del Taller 4 con `Dockerfile`, `.dockerignore` y un flujo de GitHub Actions en `.github/workflows/imagen.yml`. Módulos 2 y 4.

`pipeline-kedro/` es el proyecto Kedro del Taller 2 con `Dockerfile`, `.dockerignore` y `requirements-docker.txt`. Módulo 3. No incluye la encuesta: cópiala desde `muneco/datos/encuesta_hogares.csv` a `data/01_raw/` antes de correr.

`muneco/` es el código del muñeco del Taller 3 con las seis etapas implementadas, `Dockerfile` y `compose.yaml`. Módulo 3.

Cada copia tiene un `ORIGEN.md` que dice de dónde viene. Los archivos propios de Docker viven en `_docker/` y se aplican encima de cada copia con `python herramientas/sincronizar_copias.py`.

## Correr el material de referencia

Con Docker Desktop abierto:

```powershell
cd servicio-limpieza
docker build -t limpieza:1.0 .
docker run --rm -d --name limpieza -p 8002:8002 limpieza:1.0
# http://localhost:8002/docs ; docker stop limpieza cuando termines

cd ..\pipeline-kedro
copy ..\muneco\datos\encuesta_hogares.csv data\01_raw\
docker build -t encuesta-hogares:1.0 .
docker run --rm -v "${PWD}\data:/app/data" encuesta-hogares:1.0

cd ..\muneco
docker compose up --build
# http://localhost:8000 ; Ctrl + C y docker compose down cuando termines
```

Verificado: la imagen del servicio pesa unos 430 MB y responde `(healthy)`; el pipeline completa siete tareas y deja `data/08_reporting/tabulados.xlsx`; el muñeco levanta siete contenedores y las seis partes salen verdes, con la etapa 2 sobre la imagen `limpieza:1.0`.

## Correspondencia con la guía

| Sección de la guía | Archivo de referencia |
|----|----|
| 1.1 y 1.2 | `script-del-taller-2/modulo_1/proceso_monolito.py` |
| 2.2 y 2.3 | `servicio-limpieza/Dockerfile` y `.dockerignore` |
| 3.2 | `pipeline-kedro/Dockerfile`, `.dockerignore` y `requirements-docker.txt` |
| 3.4 | `muneco/Dockerfile` y `muneco/ensamblador/verificar.py` (variables `ETAPA_N_URL`) |
| 3.5 | `muneco/compose.yaml` |
| 4.2 | `servicio-limpieza/.github/workflows/imagen.yml` |
