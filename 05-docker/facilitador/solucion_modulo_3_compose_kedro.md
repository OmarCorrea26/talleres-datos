# Solución de referencia. Ejercicio 3.8: el pipeline y Kedro-Viz en Compose

`compose.yaml` en la raíz del proyecto `encuesta-hogares`:

```yaml
services:
  # Corre el pipeline completo y termina. `docker compose run pipeline` lo lanza;
  # `docker compose run pipeline run --pipeline preparacion` corre una parte.
  pipeline:
    build: .
    image: encuesta-hogares:1.0
    volumes:
      - ./data:/app/data

  # Visualizador. Decisión: una segunda imagen con kedro-viz encima de la primera,
  # porque la imagen del pipeline no debe cargar con una herramienta de desarrollo.
  viz:
    build:
      context: .
      dockerfile: Dockerfile.viz
    image: encuesta-hogares-viz:1.0
    command: viz run --host 0.0.0.0 --no-browser
    ports:
      - "4141:4141"
    volumes:
      - ./data:/app/data
```

`Dockerfile.viz`:

```dockerfile
FROM encuesta-hogares:1.0
USER root
RUN pip install --no-cache-dir kedro-viz
USER kedro
```

Uso:

```powershell
docker compose build
docker compose run --rm pipeline
docker compose up viz
# http://localhost:4141
```

La otra decisión defendible es agregar `kedro-viz` a `requirements-docker.txt` y usar una sola imagen. Es más simple y la imagen pesa unos 150 MB más. Lo que se evalúa no es cuál eligieron sino que lo hayan escrito con su razón.

Nota: `docker compose run` es para servicios que terminan (el pipeline); `up` es para los que se quedan (viz). Si usan `up` para los dos, el pipeline va a aparecer como "exited" y es correcto, pero confunde.
