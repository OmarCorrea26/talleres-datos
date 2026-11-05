# Módulo 2 — La primera imagen

Objetivo: escribir el Dockerfile del servicio de limpieza del Taller 4, construir la imagen, correrla con un usuario sin privilegios y una verificación de salud, medir cuánto pesa y hacer que el probador del muñeco la valide sin saber que es un contenedor. Dos horas.

### Lo que necesitas antes de empezar

- Tu proyecto `etapa-limpiar` del Taller 4, o la copia en `material/servicio-limpieza` si no lo tienes a la mano.
- Opcional, para la sección 2.8: tu clon del repositorio del muñeco del Taller 3 con su entorno.

## 2.1 Qué debe tener la imagen

Antes de escribir, piensa qué necesita el servicio para correr, y nada más. Un Python. Las dependencias que `pyproject.toml` declara bajo `http`: pandas, FastAPI, uvicorn. El código de `src/`. Un comando que arranque uvicorn. Eso es todo. No necesita pytest, ni las pruebas, ni los fixtures, ni la carpeta `docs/`, ni tu entorno virtual.

Esta lista es el Dockerfile. Lo demás es sintaxis.

## 2.2 El Dockerfile, instrucción por instrucción

En la raíz del proyecto `etapa-limpiar`, crea un archivo llamado exactamente `Dockerfile`, sin extensión:

```dockerfile
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
```

Léelo de arriba abajo con calma. `FROM` dice de qué imagen partes: la misma que usaste en el Módulo 1, con su versión escrita. `ENV` fija variables de entorno para todo lo que siga. `WORKDIR` crea la carpeta de trabajo y se mete en ella. `COPY` trae archivos de tu máquina a la imagen. `RUN` ejecuta un comando durante la construcción, y lo que ese comando deja instalado queda en la imagen. `USER` cambia quién ejecuta todo lo que sigue. `EXPOSE` documenta el puerto. `HEALTHCHECK` le da a Docker una forma de saber si el servicio está sano. Y `CMD` es el comando que corre cuando el contenedor arranca.

> [!NOTE]
> **📘 Concepto**
>
> El orden de las instrucciones no es estético. Docker guarda cada paso como una capa y, al reconstruir, reutiliza todas las capas hasta la primera que cambió. Por eso `pyproject.toml` se copia antes que `src/` y la instalación va antes que el código: cuando edites un nodo, la reconstrucción reutiliza la capa de pip, que es la que tarda, y termina en segundos. Si copiaras todo de una vez, cada cambio de una línea reinstalaría pandas.

> [!WARNING]
> **⚠️ Atención**
>
> La línea de `CMD` lleva `--host 0.0.0.0` y no es opcional. En el Taller 3 uvicorn escuchaba en `localhost` y bastaba, porque tú y el servicio estaban en la misma máquina. Dentro de un contenedor, `localhost` es el contenedor mismo, y nadie de afuera llega. `0.0.0.0` significa "escucha en todas las interfaces", que es lo que permite que el puerto publicado funcione.

## 2.3 Lo que no entra

Crea `.dockerignore` al lado del Dockerfile:

```text
# Lo que NO entra a la imagen. Menos contexto = construcción más rápida e imagen más chica.
.venv/
__pycache__/
*.pyc
*.egg-info/
.pytest_cache/
tests/
docs/
salida/
.git/
```

Cuando corres `docker build .`, el punto final es el contexto: todo lo que hay en esa carpeta se envía a Docker antes de construir. Sin este archivo, tu entorno virtual de cientos de megas viaja cada vez, aunque ninguna instrucción lo use. Es el equivalente del `.gitignore` que aprendiste en el Taller 1, y la misma lógica: lo que no es parte del producto, no se incluye.

## 2.4 Construir

```powershell
docker build -t limpieza:1.0 .
```

`-t limpieza:1.0` le pone nombre y etiqueta a la imagen. El punto es el contexto. La primera construcción tarda un par de minutos: descarga la base si no la tiene e instala las dependencias. Mira la salida: cada instrucción aparece numerada, con `CACHED` cuando se reutilizó una capa.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> La última línea dice `naming to docker.io/library/limpieza:1.0`. `docker images` lista `limpieza` con etiqueta `1.0`.

Ahora cambia cualquier comentario en `src/limpieza/adaptadores/http.py`, guarda y vuelve a construir. Fíjate en que la instalación de pip sale como `CACHED` y la construcción termina en segundos. Esa es la ganancia del orden de las capas.

## 2.5 Correr y probar desde afuera

```powershell
docker run --rm -d --name limpieza -p 8002:8002 limpieza:1.0
```

`-d` lo deja corriendo en segundo plano, `--name` le pone nombre al contenedor y `-p 8002:8002` publica el puerto: el 8002 de tu máquina va al 8002 del contenedor. Abre `http://localhost:8002/docs`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> La documentación automática de FastAPI aparece, idéntica a la del Taller 4. `docker ps` muestra el contenedor `limpieza` con estado `Up` y, pasados unos segundos, `(healthy)`. Eso último es el `HEALTHCHECK` funcionando: Docker llamó a `/salud` y respondió.

Tres comandos que vas a usar siempre que un contenedor no haga lo que esperas:

```powershell
docker logs limpieza
docker exec limpieza id
docker inspect --format "{{.State.Health.Status}}" limpieza
```

El primero muestra la salida del proceso de adentro, que es donde uvicorn escribe sus errores. El segundo ejecuta un comando dentro del contenedor que ya está corriendo: `id` responde `uid=1000(servicio)`, la prueba de que el servicio no corre como administrador. El tercero consulta el estado de salud.

> [!NOTE]
> **📘 Concepto**
>
> ¿Por qué un usuario sin privilegios? Porque un contenedor que corre como root y tiene una vulnerabilidad en FastAPI o en pandas le entrega a quien la explote un root dentro del contenedor, y desde ahí los escapes al sistema anfitrión son más fáciles. Con un usuario normal, el daño posible se reduce a lo que ese usuario puede tocar: la carpeta `/app`. Son dos líneas y es la diferencia entre una imagen que un equipo de seguridad aprueba y una que rechaza.

## 2.6 Medir y adelgazar

```powershell
docker images limpieza
docker history limpieza:1.0
```

El primer comando dice cuánto pesa la imagen. El segundo muestra cada capa con su tamaño. Si construiste con `.[http,parquet]` en vez de `.[http]`, la capa de pip pesa unos 370 MB y la imagen total ronda los 660 MB; con `.[http]` la capa baja a unos 190 MB y la imagen a unos 430 MB. La diferencia es `pyarrow`, que el servicio HTTP no usa en ningún momento. Es la misma pregunta de la sección 2.1, hecha con números: ¿qué necesita este proceso para correr?

> [!TIP]
> **💡 Tip**
>
> Las dos preguntas que más adelgazan una imagen son "¿esta dependencia la usa el proceso o solo las pruebas?" y "¿esta base trae cosas que no necesito?". Las variantes `-slim` de las imágenes oficiales ya quitan compiladores y documentación. Hay variantes más pequeñas todavía, como `alpine`, pero pandas y numpy suelen necesitar compilarse en ellas y la construcción pasa de minutos a media hora. Para procesos con pandas, `slim` es el punto justo.

## 2.7 Etiquetas y versiones

Haz un cambio pequeño en el servicio, por ejemplo el `description` de la aplicación FastAPI, y construye con otra etiqueta:

```powershell
docker build -t limpieza:1.1 .
docker images limpieza
```

Las dos versiones coexisten. Puedes correr la 1.0 en un puerto y la 1.1 en otro, comparar, y volver atrás en un segundo si la nueva falla. Eso, en un servidor, se llama despliegue sin riesgo.

> [!WARNING]
> **⚠️ Atención**
>
> No uses la etiqueta `latest`, ni para tus imágenes ni en el `FROM`. "La última" cambia sin avisar, de modo que la misma construcción da resultados distintos en días distintos. Una imagen reproducible nombra versiones concretas: `python:3.11-slim` en la base, `limpieza:1.1` en la tuya. Si quieres máxima reproducibilidad, la base se puede fijar por su huella digital con `@sha256:...`, que Docker muestra al descargarla.

## 2.8 La prueba de fuego, otra vez

Con el contenedor corriendo en 8002, ve a tu clon del muñeco del Taller 3, con su entorno activo, y corre su probador:

```powershell
python -m ensamblador.probar --etapa 2
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `[OK] Etapa 2 (limpiar, torso) en http://localhost:8002` y `Cumple el contrato`. En el Taller 4 el probador validó una etapa que vivía en otro paquete. Ahora valida una que vive en otro sistema operativo, con otro Python, dentro de un contenedor. El contrato sigue siendo el mismo y eso es lo único que el probador mira.

Detén el contenedor cuando termines:

```powershell
docker stop limpieza
```

## 2.9 Ejercicio práctico: la terminal como imagen

El proyecto del Taller 4 también tiene una línea de comandos. Escribe un segundo Dockerfile, llamado `Dockerfile.cli`, que construya una imagen cuyo `ENTRYPOINT` sea `python -m limpieza.adaptadores.cli`, de modo que `docker run --rm -v "${PWD}/datos:/datos" limpieza-cli:1.0 /datos/encuesta_hogares.csv /datos/limpia.csv` limpie un archivo de tu máquina y deje el resultado al lado. Constrúyela con `docker build -f Dockerfile.cli -t limpieza-cli:1.0 .`. Pista: necesita el extra `parquet` si quieres que acepte `.parquet`, y un volumen, porque sin él no hay forma de que el archivo entre ni salga.

## 2.10 Troubleshooting del Módulo 2

| Síntoma | Causa probable | Solución |
|----|----|----|
| `failed to solve: ... pyproject.toml: not found` | Corriste `docker build` desde otra carpeta | El punto final es el contexto; ubícate en la raíz del proyecto |
| `pip install` falla con `No matching distribution` | El `FROM` no es una imagen de Python o la versión es muy vieja | `python:3.11-slim`, tal cual |
| `/docs` no abre aunque `docker ps` muestra `Up` | Falta `--host 0.0.0.0` en el `CMD`, o no publicaste el puerto con `-p` | Sección 2.2 y 2.5 |
| `port is already allocated` | Tu etapa del Taller 3 o un contenedor anterior ocupa el 8002 | `docker ps` y `docker stop` el que sobre, o publica en otro puerto: `-p 8012:8002` |
| El estado dice `(unhealthy)` | El servicio tarda más de 5 s en arrancar o `/salud` no responde | `docker logs` para ver el error; sube `--start-period` si solo es lentitud |
| `permission denied` al escribir en `/app` | El usuario `servicio` no es dueño de la carpeta donde escribes | Crea la carpeta y dale permisos antes de `USER`, como hace el Dockerfile del muñeco en el Módulo 3 |

## 2.11 Para profundizar (opcional)

- Construcciones en varias etapas (`FROM ... AS constructor`) permiten compilar en una imagen grande y copiar solo el resultado a una pequeña. Para servicios con pandas no cambia mucho; para proyectos con compilación de C sí.
- `docker scout quickview limpieza:1.0` (incluido en Docker Desktop) lista vulnerabilidades conocidas de los paquetes de la imagen. Vale la pena correrlo una vez para ver qué aparece en la base y por qué conviene reconstruir con frecuencia.
