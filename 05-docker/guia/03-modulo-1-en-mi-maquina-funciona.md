# Módulo 1 — En mi máquina funciona

Objetivo: correr el script del Taller 2 dentro de un contenedor que no tiene nada tuyo instalado, entender qué pasó y qué no pasó, y sentir el problema que una imagen propia resuelve. Una hora.

### Lo que necesitas antes de empezar

- Docker Desktop abierto y `docker run --rm hello-world` funcionando.
- La carpeta `material/script-del-taller-2` ubicada.

## 1.1 Un contenedor vacío

Desde la carpeta `material/script-del-taller-2`, intenta correr el monolito dentro de la imagen de Python que descargaste en el Módulo 0:

```powershell
docker run --rm -v "${PWD}:/trabajo" -w /trabajo python:3.11-slim python modulo_1/proceso_monolito.py
```

En macOS o Linux, reemplaza `${PWD}` por `$(pwd)`.

Falla con `ModuleNotFoundError: No module named 'pandas'`. Es el resultado correcto, y es la primera lección: el contenedor tiene Python y nada más. No tiene tu entorno virtual, no tiene pandas, no sabe que existe tu máquina salvo por la carpeta que le montaste.

Lee el comando por partes antes de seguir. `--rm` borra el contenedor cuando termina. `-v "${PWD}:/trabajo"` monta la carpeta actual de tu máquina en la ruta `/trabajo` de adentro: eso es un volumen. `-w /trabajo` dice que el comando corra desde esa ruta. `python:3.11-slim` es la imagen. Y lo que sigue es el comando que corre adentro.

## 1.2 Instalar y correr, todo adentro

Dale lo que le falta, en el mismo comando:

```powershell
docker run --rm -v "${PWD}:/trabajo" -w /trabajo python:3.11-slim sh -c "pip install -q pandas openpyxl && python modulo_1/proceso_monolito.py"
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El script imprime la tabla de tasas de ocupación con sus coeficientes de variación, igual que en el Taller 2, y en tu carpeta aparece `salida_monolito.xlsx`. El contenedor ya no existe, sin embargo el archivo sí, porque se escribió en la carpeta montada.

Ahora vuelve a correr exactamente el mismo comando. Tarda lo mismo: vuelve a instalar pandas desde cero. Nada de lo que se instaló la primera vez sobrevivió, porque se instaló dentro del contenedor y el contenedor se borró. Esa es la segunda lección, y es la que motiva todo el Módulo 2: lo que un proceso necesita para correr no debería instalarse cada vez; debería estar en la imagen.

> [!NOTE]
> **📘 Concepto**
>
> Un contenedor es efímero por diseño. Todo lo que escribe dentro de sí mismo desaparece cuando termina, salvo lo que escribe en un volumen. Suena a limitación y es una garantía: cada corrida parte del mismo estado exacto, el de la imagen. No hay "se me quedó un archivo de la vez pasada" ni "funciona porque instalé algo hace meses". Si quieres que algo persista, tiene que ser explícito: un volumen para los datos, una imagen nueva para el software.

## 1.3 Mirar lo que hay

Tres comandos para ver el estado de Docker en tu máquina:

```powershell
docker images
docker ps -a
docker system df
```

El primero lista las imágenes descargadas: `hello-world` y `python:3.11-slim`, con su tamaño. El segundo lista los contenedores, incluidos los terminados; con `--rm` no debería haber ninguno. El tercero dice cuánto disco ocupa todo. Vuelve a estos tres comandos cada vez que algo te parezca raro: la mitad de los problemas con Docker se diagnostican mirando qué imágenes y contenedores existen.

> [!TIP]
> **💡 Tip**
>
> Docker Desktop tiene una interfaz gráfica que muestra lo mismo. Úsala para mirar, pero aprende los comandos: en un servidor no hay interfaz, y en el Módulo 4 los vas a necesitar en integración continua.

## 1.4 Lo que acaba de pasar, dibujado

```text
   Tu máquina                              Contenedor (python:3.11-slim)
   ------------------------------          --------------------------------
   script-del-taller-2/          <--v-->   /trabajo/            (el volumen)
     modulo_1/proceso_monolito.py            modulo_1/proceso_monolito.py
     datos/encuesta_hogares.csv              datos/encuesta_hogares.csv
     salida_monolito.xlsx  <--- escrito aquí por el proceso de adentro

   Python 3.12, tu .venv, pandas 2.x        Python 3.11.18, pandas recién instalado
   (no los vio)                             (desaparecen al terminar)
```

El script no supo que corría en otro Python ni en otro sistema operativo. Leyó `datos/encuesta_hogares.csv` por una ruta relativa, escribió al lado, y terminó. Si en vez de pandas hubiera necesitado una librería de sistema que tú tienes y tu compañero no, la diferencia se habría visto aquí, en un contenedor idéntico para los dos.

## 1.5 Ejercicio práctico: la misma corrida con otra versión

Repite el comando de la sección 1.2 cambiando la imagen por `python:3.12-slim` y después por `python:3.10-slim`. Anota si el script corre igual en las tres. Después prueba con `pandas==1.5.3` en el `pip install`. Lo que debes notar: cambiar de versión de Python o de pandas te costó editar un comando, no reinstalar nada en tu máquina, y tu entorno virtual quedó intacto. Es la forma más barata que existe de responder "¿esto corre con la versión que tiene el servidor?".

## 1.6 Troubleshooting del Módulo 1

| Síntoma | Causa probable | Solución |
|----|----|----|
| `docker: invalid reference format` | Comillas o `${PWD}` mal escritos; en PowerShell deben ser comillas dobles | Copia el comando tal cual; en macOS o Linux usa `$(pwd)` |
| El contenedor no ve los archivos (`No such file or directory`) | La carpeta montada no es la que crees | `cd` a `script-del-taller-2` antes de correr; `${PWD}` es la carpeta actual |
| Docker pide permiso para compartir la unidad | Primera vez que montas una carpeta de esa unidad | Acepta en el diálogo de Docker Desktop, o en Settings, Resources, File sharing |
| `pip install` es muy lento o falla por red | Proxy o red corporativa | Es otra razón para el computador personal; en casa suele ser inmediato |
| `salida_monolito.xlsx` queda con dueño raro en Linux | El proceso de adentro corre como root | En el Módulo 2 se resuelve con un usuario sin privilegios |

## 1.7 Para profundizar (opcional)

- Corre `docker run --rm -it python:3.11-slim bash` y explora el contenedor desde adentro con `ls /`, `python -c "import sys; print(sys.version)"` y `pip list`. Sal con `exit`. Ver que es un Linux completo pero mínimo ayuda a fijar la idea.
- `docker image inspect python:3.11-slim` muestra todo lo que Docker sabe de la imagen, incluido el comando por defecto y las capas.
