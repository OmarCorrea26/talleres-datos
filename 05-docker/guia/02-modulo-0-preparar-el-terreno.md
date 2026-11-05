# Módulo 0 — Preparar el terreno

Objetivo: Docker Desktop instalado y funcionando, un primer contenedor corriendo, y el vocabulario mínimo para entender lo que viene. Unos 45 minutos, más lo que tarde la descarga.

### Lo que necesitas antes de empezar

- Windows 10 u 11 de 64 bits, actualizado, con al menos 8 GB de memoria. Si tienes macOS o Linux, Docker Desktop también existe para ellos y los comandos de la guía son los mismos.
- Permisos de administrador en tu computador personal.
- El material del taller descomprimido: `guia/` y `material/`.

## 0.1 Instalar Docker Desktop

Descarga el instalador desde `https://www.docker.com/products/docker-desktop/` y ejecútalo. En Windows va a pedirte que use WSL 2, el subsistema de Linux de Windows; acepta. Si el instalador te dice que WSL no está instalado, abre PowerShell como administrador, ejecuta `wsl --install`, reinicia y vuelve a correr el instalador de Docker.

Al terminar, reinicia el computador aunque no te lo pida. Después abre Docker Desktop desde el menú de inicio y espera a que el ícono de la ballena en la bandeja deje de moverse.

> [!NOTE]
> **📘 Concepto**
>
> Docker corre contenedores de Linux. En Windows lo hace dentro de una máquina virtual muy liviana que gestiona WSL 2, y por eso lo necesita. Tú no vas a ver esa máquina virtual nunca, sin embargo explica dos cosas que vas a notar: que los contenedores "piensan" en rutas de Linux con barras normales, y que montar carpetas de Windows dentro de un contenedor es un poco más lento que en Linux nativo.

> [!WARNING]
> **⚠️ Atención**
>
> Docker Desktop es gratuito para uso personal y educativo, y de pago para empresas grandes. Para este taller, en tu máquina personal, no hay problema. Si en tu entidad quisieran usarlo, es una conversación que debe pasar por quien compra las licencias, y conviene saberlo antes de proponerlo.

## 0.2 Verificar la instalación

Abre PowerShell, sin necesidad de administrador:

```powershell
docker --version
docker compose version
docker run --rm hello-world
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Las dos primeras líneas responden con una versión (Docker 27 o superior, Compose v2 o superior). La tercera descarga una imagen diminuta, la corre, imprime un mensaje que empieza por `Hello from Docker!` y termina. Si ves `error during connect` o `the docker daemon is not running`, Docker Desktop no está abierto: ábrelo y espera a la ballena.

Corre una segunda cosa, que vas a usar todo el taller:

```powershell
docker run --rm python:3.11-slim python --version
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Imprime `Python 3.11.x`. Acabas de ejecutar Python sin haberlo instalado: vino dentro de una imagen que Docker descargó. Fíjate en que la versión no es necesariamente la que tienes en tu máquina, y esa es exactamente la idea.

## 0.3 Las siete palabras del taller

| Palabra | Qué es | Lo más parecido que ya conoces |
|----|----|----|
| Imagen | Un archivo inmutable con un sistema de archivos completo: intérprete, paquetes, tu código. Se construye una vez | Un entorno virtual congelado, con el sistema operativo incluido |
| Contenedor | Un proceso corriendo a partir de una imagen, aislado del resto de la máquina. Se crea, corre y se borra | Una sesión de Python abierta sobre ese entorno |
| Dockerfile | El texto que dice cómo construir una imagen, paso a paso | Un `requirements.txt` que además dice qué versión de Linux y qué comando arrancar |
| Registro | Un servidor de donde se descargan y a donde se suben imágenes. Docker Hub es el público | PyPI, pero para imágenes |
| Capa | Cada paso del Dockerfile produce una capa. Docker reutiliza las que no cambiaron | La caché de pip |
| Volumen | Una carpeta de tu máquina visible dentro del contenedor. Es la única forma de que lo que el contenedor escribe sobreviva | Un disco de red montado |
| Compose | Un archivo YAML que describe varios contenedores y cómo se conectan, y un comando que los levanta juntos | El `levantar_todo.ps1` del Taller 3, pero declarativo |

> [!TIP]
> **💡 Tip**
>
> La distinción que más cuesta es imagen contra contenedor. Piensa en la imagen como el instalador y en el contenedor como el programa corriendo. De un instalador puedes abrir muchos programas; cuando cierras uno, el instalador sigue ahí intacto.

## 0.4 El material

Dentro de `material/` hay cuatro carpetas y conviene saber qué es cada una antes de empezar.

`script-del-taller-2/` tiene el monolito del Taller 2 y la encuesta sintética. Es lo que vas a correr dentro de un contenedor en el Módulo 1.

`servicio-limpieza/` es una copia del proyecto del Taller 4 con su Dockerfile ya escrito. `pipeline-kedro/` es una copia del proyecto del Taller 2, también con Dockerfile. `muneco/` es el código del muñeco del Taller 3, con las seis etapas implementadas, un Dockerfile y un `compose.yaml`.

En los módulos 2 y 3 vas a escribir esos archivos tú, sobre tus propios proyectos. Las copias están para comparar y para que el taller funcione aunque no tengas los anteriores a la mano. Cada copia tiene un `ORIGEN.md` que dice de dónde viene.

## 0.5 Troubleshooting del Módulo 0

| Síntoma | Causa probable | Solución |
|----|----|----|
| El instalador dice que la virtualización está desactivada | Opción de la BIOS/UEFI | Entra a la configuración de arranque y activa "Virtualization Technology" o "SVM Mode". Es un cambio único |
| `docker run` se queda colgado la primera vez | Está descargando la imagen y no hay barra de progreso en algunas terminales | Espera; `python:3.11-slim` pesa unos 45 MB |
| `error during connect` | Docker Desktop cerrado | Ábrelo y espera a que el ícono se estabilice |
| `wsl --install` falla por política | Equipo institucional | Este taller es para el computador personal |
| Docker Desktop consume mucha memoria | Es normal: reserva memoria para la máquina virtual | En Settings, Resources, puedes limitarla a 4 GB para este taller |
