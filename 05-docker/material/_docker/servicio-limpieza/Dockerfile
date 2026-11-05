# Imagen del servicio de limpieza (etapa 2 del muñeco, versión del Taller 4).
#
# Construir:  docker build -t limpieza:1.0 .
# Correr:     docker run --rm -p 8002:8002 limpieza:1.0
#
# Cada instrucción es una capa. Las que cambian poco (base, dependencias) van
# primero para que Docker las reutilice; el código, que cambia siempre, va al final.

FROM python:3.11-slim

# Que pip no deje caché dentro de la imagen y que Python no escriba .pyc
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Primero solo lo que hace falta para instalar dependencias: si el código cambia
# pero pyproject.toml no, esta capa se reutiliza y la construcción tarda segundos.
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install ".[http]"

# El servicio no necesita privilegios: un usuario propio limita el daño si algo falla
RUN useradd --create-home --shell /bin/false servicio
USER servicio

EXPOSE 8002

# Docker pregunta cada 30 s si el servicio sigue vivo usando su propia ruta /salud
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8002/salud')" || exit 1

# 0.0.0.0 y no localhost: dentro del contenedor, localhost es solo el contenedor
CMD ["uvicorn", "limpieza.adaptadores.http:app", "--host", "0.0.0.0", "--port", "8002"]
