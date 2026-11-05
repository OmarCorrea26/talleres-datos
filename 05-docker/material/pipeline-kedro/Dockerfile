# Imagen del pipeline Kedro de la encuesta de hogares (Taller 2).
#
# Construir:  docker build -t encuesta-hogares:1.0 .
# Correr:     docker run --rm -v "${PWD}/data:/app/data" encuesta-hogares:1.0
#             docker run --rm -v "${PWD}/data:/app/data" encuesta-hogares:1.0 kedro run --pipeline preparacion
#
# Los datos NO van dentro de la imagen: se montan como volumen al correr.
# La imagen lleva el proceso; los datos son de quien la ejecuta.

FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    KEDRO_DISABLE_TELEMETRY=1

WORKDIR /app

# Dependencias mínimas de ejecución: sin kedro-viz, sin Jupyter, sin pytest.
# Son la mitad del tamaño y no hacen falta para correr el pipeline.
COPY requirements-docker.txt ./
RUN pip install -r requirements-docker.txt

COPY pyproject.toml ./
COPY conf/base/ ./conf/base/
COPY src/ ./src/

# Kedro exige que exista conf/local aunque esté vacío, y data/ es el punto de montaje
RUN mkdir -p conf/local data \
    && useradd --create-home --shell /bin/false kedro \
    && chown -R kedro:kedro /app
USER kedro

ENTRYPOINT ["kedro"]
CMD ["run"]
