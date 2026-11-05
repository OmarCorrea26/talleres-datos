# Solución de referencia. Ejercicio 2.9: la terminal del Taller 4 como imagen

`Dockerfile.cli` en la raíz del proyecto `etapa-limpiar`:

```dockerfile
FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml ./
COPY src/ ./src/
# parquet, para que acepte .parquet además de .csv; sin http, porque la terminal no sirve nada
RUN pip install ".[parquet]"

RUN useradd --create-home --shell /bin/false servicio
USER servicio

# Punto de entrada fijo: todo lo que siga al nombre de la imagen son argumentos de la CLI
ENTRYPOINT ["python", "-m", "limpieza.adaptadores.cli"]
CMD ["--help"]
```

Construir y usar:

```powershell
docker build -f Dockerfile.cli -t limpieza-cli:1.0 .
docker run --rm limpieza-cli:1.0
docker run --rm -v "${PWD}\datos:/datos" limpieza-cli:1.0 /datos/encuesta_hogares.csv /datos/limpia.csv --metodo media
```

Lo que debe notar quien lo resuelve: sin el volumen no hay forma de que el archivo entre ni salga; el `ENTRYPOINT` convierte la imagen en un comando; y la imagen es distinta de la del servicio porque instala otras dependencias, aunque el código sea el mismo. Dos mecanismos de entrega, dos imágenes, un dominio.

Verificado: la imagen construye sobre `material/servicio-limpieza` y la corrida con la encuesta devuelve `1215 filas leídas, 15 duplicados eliminados, 6 atípicos recortados, 27 ingresos imputados`.
