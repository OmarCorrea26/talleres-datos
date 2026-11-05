# Una sola imagen para las siete piezas del muñeco: el ensamblador y las seis etapas.
# Comparten código (contrato, fixtures) y dependencias; lo que cambia entre una y
# otra es el comando con el que arrancan. Eso lo decide compose.yaml.
#
# Construir:  docker build -t muneco:1.0 .
# Correr una etapa suelta:
#   docker run --rm -p 8003:8003 muneco:1.0 uvicorn etapas.etapa_3_calibrar.app:app --host 0.0.0.0 --port 8003

FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY contrato/ ./contrato/
COPY datos/ ./datos/
COPY ensamblador/ ./ensamblador/
COPY etapas/ ./etapas/
COPY fixtures/ ./fixtures/

# La etapa 6 escribe el Excel en salida/: la carpeta debe existir y ser del usuario
RUN mkdir -p salida \
    && useradd --create-home --shell /bin/false muneco \
    && chown -R muneco:muneco /app
USER muneco

# Por defecto arranca el ensamblador; compose.yaml cambia el comando para cada etapa
CMD ["uvicorn", "ensamblador.app:app", "--host", "0.0.0.0", "--port", "8000"]
