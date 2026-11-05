# Módulo 3 — Datos afuera, servicios juntos

Objetivo: empaquetar el pipeline Kedro con los datos fuera de la imagen, y levantar el muñeco completo con un solo comando usando Docker Compose, con la etapa 2 servida por el contenedor del Módulo 2. Dos horas.

### Lo que necesitas antes de empezar

- La imagen `limpieza:1.0` del Módulo 2 construida.
- Tu proyecto Kedro del Taller 2 o la copia en `material/pipeline-kedro`, y el código del muñeco en `material/muneco`.

## 3.1 Un proceso por lotes no es un servicio

El servicio del Módulo 2 arranca y se queda escuchando. El pipeline de Kedro arranca, procesa y termina. Esa diferencia cambia tres cosas en el Dockerfile: no hay puerto que publicar, no hay verificación de salud, y lo importante no es lo que el proceso responde sino lo que escribe. Y lo que escribe tiene que salir del contenedor, porque si no, se pierde con él. Tal como viste en el Módulo 1, eso se resuelve con un volumen.

Hay además una decisión que vale la pena tomar explícitamente: los datos no van dentro de la imagen. La imagen lleva el proceso, que cambia cuando cambia el código. Los datos cambian cada período, pueden ser confidenciales y pueden pesar gigas. Van montados al correr, igual que en el Taller 2 no iban al repositorio.

## 3.2 El Dockerfile del pipeline

En la raíz del proyecto `encuesta-hogares`, primero un `requirements-docker.txt` con lo mínimo para correr, sin Kedro-Viz, sin Jupyter y sin pytest:

```text
# Solo lo necesario para `kedro run` dentro del contenedor.
# Compara con requirements.txt: aquí no hay kedro-viz, ipython ni pytest.
kedro~=1.7.0
kedro-datasets[pandas-csvdataset,pandas-parquetdataset,pandas-exceldataset,json-jsondataset]
pandas
openpyxl
pyarrow
```

Después el `Dockerfile`:

```dockerfile
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
```

Dos cosas nuevas frente al Módulo 2. Se copia `conf/base/` pero no `conf/local/`: lo local es de cada máquina y nunca entra a una imagen, por la misma razón por la que no entraba al repositorio. Y la pareja `ENTRYPOINT` más `CMD`: el punto de entrada es fijo, `kedro`, y el comando por defecto es `run`, de modo que `docker run imagen` corre el pipeline completo y `docker run imagen run --pipeline preparacion` corre una parte. Lo que pongas después del nombre de la imagen reemplaza a `CMD`, nunca a `ENTRYPOINT`.

Y el `.dockerignore`, que esta vez excluye `data/` entero:

```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
.telemetry
.viz/
data/
conf/local/
notebooks/
tests/
.git/
```

## 3.3 Construir y correr con los datos montados

```powershell
docker build -t encuesta-hogares:1.0 .
```

Asegúrate de que `data/01_raw/encuesta_hogares.csv` exista en tu máquina (en el material está en `muneco/datos/`). Después:

```powershell
docker run --rm -v "${PWD}\data:/app/data" encuesta-hogares:1.0
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El registro de Kedro corre completo dentro del contenedor y termina con `Completed 7 out of 7 tasks` y el mensaje del hook, `Corrida terminada en X segundos`. En tu máquina, `data/08_reporting/tabulados.xlsx` existe y tiene las doce filas de siempre. El proceso corrió en Linux, con un Python que no es el tuyo, y dejó el resultado en tu disco.

Ahora corre sin el volumen para ver la diferencia:

```powershell
docker run --rm encuesta-hogares:1.0
```

Falla con `DatasetError: encuesta_cruda: Failed while loading data`. Sin volumen, `data/` está vacía dentro del contenedor. No es un error de Kedro: es la imagen diciéndote que los datos no son suyos.

Y prueba el `ENTRYPOINT`:

```powershell
docker run --rm -v "${PWD}\data:/app/data" encuesta-hogares:1.0 run --pipeline estimacion_rural
docker run --rm encuesta-hogares:1.0 registry list
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El primero completa cinco tareas y deja `data/08_reporting/rural/`. El segundo lista los cuatro pipelines sin necesitar datos. Todo lo que `kedro` sabe hacer, lo sabe hacer dentro de la imagen.

> [!TIP]
> **💡 Tip**
>
> Los parámetros de `conf/local` que no entran a la imagen se pueden pasar al correr, sin reconstruir: `docker run ... encuesta-hogares:1.0 run --params "limpieza.percentil_atipicos=0.95"`. Y las variables de entorno con `-e NOMBRE=valor`. Esa es la regla para contenedores: lo que cambia entre corridas o entre máquinas entra por fuera, al momento de correr; lo que es parte del proceso, por dentro, al construir.

## 3.4 El muñeco: una imagen, siete servicios

Ahora el proyecto más grande. En el Taller 3, `levantar_todo.ps1` abría siete ventanas de terminal, una por servicio, en la misma máquina. Con contenedores cada servicio corre aislado y Docker Compose los describe y los levanta juntos.

Hay un cambio pequeño en el código del muñeco que hay que entender antes. El ensamblador encontraba cada etapa en `http://localhost:800N`. En contenedores, `localhost` es cada contenedor mismo, así que esa dirección no sirve. El código de `ensamblador/verificar.py` ahora acepta una variable de entorno por etapa:

```python
url = url_base or os.environ.get(f"ETAPA_{numero}_URL") or f"http://localhost:{defi['puerto']}"
```

Si la variable no existe, todo sigue como en el Taller 3. Si existe, manda. Es un cambio de tres líneas, compatible hacia atrás, y es el patrón que aprendiste en el Módulo 1 del Taller 4 aplicado a la infraestructura: la dirección de un colaborador es configuración, no código.

> [!NOTE]
> **📘 Concepto**
>
> Esta es la regla más citada sobre aplicaciones que se despliegan bien: la configuración vive en el entorno, no en el código. Puertos, direcciones, rutas, credenciales, todo lo que cambia entre tu máquina, la de un compañero y el servidor, entra como variable de entorno. El código lee la variable y usa un valor razonable si no está. Así la misma imagen corre en los tres lugares sin reconstruirse.

El Dockerfile del muñeco es uno solo, en la raíz de su repositorio:

```dockerfile
# Una sola imagen para las siete piezas del muñeco: el ensamblador y las seis etapas.
# Comparten código (contrato, fixtures) y dependencias; lo que cambia entre una y
# otra es el comando con el que arrancan. Eso lo decide compose.yaml.

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
```

Fíjate en que `COPY` nombra las carpetas una por una en vez de copiar todo con `COPY . .`. Es más largo y es a propósito: lo que entra a la imagen está escrito, y `tests/` o `.venv/` no pueden colarse por descuido.

## 3.5 `compose.yaml`: describir en vez de ejecutar

En la raíz del muñeco, `compose.yaml`:

```yaml
# El muñeco completo con un solo comando:  docker compose up --build
# Abrir http://localhost:8000. Detener con Ctrl + C y limpiar con docker compose down.
#
# Siete servicios. Seis usan la misma imagen con comandos distintos; la etapa 2
# usa la imagen del servicio de limpieza del Taller 4, que vive en otra carpeta.
# Dentro de la red de compose cada servicio se encuentra por su nombre:
# el ensamblador llama a http://etapa_3:8003 y Docker resuelve el nombre.

services:
  ensamblador:
    build: .
    image: muneco:1.0
    ports:
      - "8000:8000"
    environment:
      ETAPA_1_URL: http://etapa_1:8001
      ETAPA_2_URL: http://etapa_2:8002
      ETAPA_3_URL: http://etapa_3:8003
      ETAPA_4_URL: http://etapa_4:8004
      ETAPA_5_URL: http://etapa_5:8005
      ETAPA_6_URL: http://etapa_6:8006
    depends_on:
      - etapa_1
      - etapa_2
      - etapa_3
      - etapa_4
      - etapa_5
      - etapa_6
    volumes:
      # encadenar deja aquí el resultado final cuando se corre dentro del contenedor
      - ./salida:/app/salida

  etapa_1:
    image: muneco:1.0
    command: uvicorn etapas.etapa_1_validar.app:app --host 0.0.0.0 --port 8001

  # La etapa 2 no sale de esta imagen: es el contenedor del Taller 4.
  # Mismo contrato, otro repositorio, otra imagen. El ensamblador no lo nota.
  etapa_2:
    build: ../servicio-limpieza
    image: limpieza:1.0

  etapa_3:
    image: muneco:1.0
    command: uvicorn etapas.etapa_3_calibrar.app:app --host 0.0.0.0 --port 8003

  etapa_4:
    image: muneco:1.0
    command: uvicorn etapas.etapa_4_indicadores.app:app --host 0.0.0.0 --port 8004

  etapa_5:
    image: muneco:1.0
    command: uvicorn etapas.etapa_5_precision.app:app --host 0.0.0.0 --port 8005

  etapa_6:
    image: muneco:1.0
    command: uvicorn etapas.etapa_6_publicar.app:app --host 0.0.0.0 --port 8006
    volumes:
      # El Excel que publica la etapa 6 queda en tu máquina, no dentro del contenedor
      - ./salida:/app/salida
```

Varias cosas que este archivo dice sin un solo `if`. Cada servicio es un contenedor. Seis comparten la imagen `muneco:1.0` y se distinguen por `command`. Solo el ensamblador publica un puerto hacia tu máquina: las etapas hablan entre sí por la red interna que Compose crea, donde cada servicio se encuentra por su nombre, y desde afuera no son alcanzables. Las variables `ETAPA_N_URL` apuntan a esos nombres. `depends_on` arranca las etapas antes que el ensamblador. Y la etapa 2 se construye desde otra carpeta, con otra imagen: la del Módulo 2.

Ajusta la ruta de `build: ../servicio-limpieza` a donde tengas tu proyecto del Taller 4.

## 3.6 Levantar, mirar, bajar

```powershell
docker compose up --build
```

La primera vez construye las dos imágenes y arranca los siete contenedores; verás los registros de todos entremezclados, cada línea con el nombre de su servicio. Cuando se estabilicen, abre `http://localhost:8000`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El muñeco aparece con las seis partes verdes. `http://localhost:8000/estado` devuelve seis entradas con `"estado": "ok"` y `"Cumple el contrato"`, y la de la etapa 2 muestra `"url": "http://etapa_2:8002"`: el ensamblador llamó al contenedor del Taller 4 por su nombre de servicio.

En otra terminal, desde la misma carpeta:

```powershell
docker compose ps
docker compose exec ensamblador python -m ensamblador.encadenar
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `ps` lista siete servicios en `Up`, con `etapa_2` sobre la imagen `limpieza:1.0` y marcada `(healthy)`. `encadenar` corre el proceso completo dentro del contenedor del ensamblador, etapa por etapa, y en tu máquina aparece `salida/tabulados.xlsx`, escrito por el contenedor de la etapa 6 a través de su volumen.

Para detener todo, Ctrl + C en la terminal de `up`, y después:

```powershell
docker compose down
```

`down` borra los contenedores y la red. Las imágenes quedan, y `salida/` también, porque está en tu disco.

> [!TIP]
> **💡 Tip**
>
> `docker compose up -d` levanta todo en segundo plano y te devuelve la terminal; `docker compose logs -f etapa_3` muestra el registro de un solo servicio; `docker compose restart etapa_3` reinicia uno sin tocar los demás. Cuando cambies el código de una etapa, `docker compose up --build etapa_3` reconstruye y reemplaza solo esa.

## 3.7 Lo que cambió respecto al Taller 3

En el Taller 3, para ver el muñeco verde hacía falta que seis personas tuvieran Python, el entorno, las dependencias y siete terminales abiertas en la misma máquina. Ahora hace falta Docker y un comando. Cualquier persona con el repositorio puede ver el proceso completo corriendo en cinco minutos, incluyendo a quien revisa un Pull Request, a quien audita el proceso o a quien lo va a operar en un servidor. Y la etapa 2 demostró algo más: dos equipos pueden entregar imágenes separadas, de repositorios separados, y el contrato las une.

## 3.8 Ejercicio práctico: el pipeline también en Compose

Escribe un `compose.yaml` para el proyecto Kedro con un solo servicio, `pipeline`, que construya la imagen, monte `./data` y corra `kedro run`. Después agrega un segundo servicio, `viz`, que use la misma imagen con `command: viz run --host 0.0.0.0` y publique el puerto 4141, para ver el linaje en el navegador desde un contenedor. Pista: Kedro-Viz no está en `requirements-docker.txt`, así que vas a tener que decidir si lo agregas a esa imagen o construyes una segunda imagen solo para visualizar. Las dos decisiones son defendibles; escribe en un comentario cuál tomaste y por qué.

## 3.9 Troubleshooting del Módulo 3

| Síntoma | Causa probable | Solución |
|----|----|----|
| `DatasetError` al correr el pipeline en el contenedor | Falta el volumen, o la ruta de `-v` no es la carpeta `data` | `-v "${PWD}\data:/app/data"` desde la raíz del proyecto; en macOS o Linux `$(pwd)/data` |
| Los archivos que escribe el contenedor aparecen con dueño `1000` en Linux | El usuario de adentro es `kedro` (uid 1000) | Es correcto; si molesta, corre con `--user $(id -u)` |
| En `/estado` todas las etapas dicen `ausente` | El ensamblador no recibió las variables `ETAPA_N_URL` o el código no las lee | Revisa `environment` en compose y que `verificar.py` tenga el cambio de la sección 3.4 |
| Solo la etapa 2 sale `ausente` | La ruta de `build: ../servicio-limpieza` no apunta a tu proyecto del Taller 4 | Corrígela; `docker compose config` muestra el archivo con las rutas resueltas |
| `port is already allocated` en 8000 | El ensamblador del Taller 3 sigue corriendo en tu máquina | Ciérralo, o publica en otro puerto: `"8010:8000"` |
| `docker compose up` reconstruye todo cada vez | Cambiaste un archivo que está antes de las dependencias en el Dockerfile | Revisa el orden de `COPY`; las dependencias van antes que el código |
| `permission denied` al escribir `salida/` | La carpeta no existe dentro de la imagen o no es del usuario | El Dockerfile del muñeco la crea y la asigna antes de `USER` |

## 3.10 Para profundizar (opcional)

- `docker compose config` imprime el archivo final con todo resuelto. Es la forma de ver qué entiende Compose antes de levantar nada.
- Los volúmenes con nombre (`volumes: datos:` en la raíz del compose) los gestiona Docker en vez de apuntar a una carpeta tuya. Sirven para bases de datos y cachés; para datos de encuesta que quieres ver en tu disco, el montaje de carpeta que usamos es más claro.
