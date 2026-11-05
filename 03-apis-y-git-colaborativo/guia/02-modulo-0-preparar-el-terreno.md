# Módulo 0 — Preparar el terreno

Objetivo: tener el repositorio compartido en tu máquina, con su entorno virtual, las pruebas corriendo y el ensamblador mostrando el muñeco vacío. Unos 30 minutos.

### Lo que necesitas antes de empezar

- Python 3.11 o superior y VSCode instalados (Módulo 0 del Taller 1).
- Git instalado y configurado con tu nombre y correo (Módulo 3 del Taller 1). Verifica con `git config --global user.name`.
- Tu cuenta de GitHub, y haber aceptado la invitación como colaborador del repositorio `OmarCorrea26/taller-api-muneco` (te llega por correo; también aparece en github.com/notifications).
- Saber qué etapa te corresponde. Está en la tabla del `README.md` del repositorio.

## 0.1 ¿Por qué un repositorio compartido y no uno por persona?

En el Taller 1 cada quien tenía su repositorio. Eso sirve para aprender Git, pero no representa cómo se trabaja de verdad: en un proyecto real hay **un** repositorio, muchas personas y un flujo que evita que se pisen. Este taller usa ese modelo. Una consecuencia inmediata: lo que subes lo ven todos, y lo que sube otro te afecta. Por eso existen las ramas, las revisiones y el rebase, que son el tema del Módulo 3.

## 0.2 Clonar el repositorio

Abre PowerShell, ve a la carpeta donde guardas tus proyectos y clona:

```powershell
cd C:\Users\tu-usuario\Documentos\proyectos
git clone https://github.com/OmarCorrea26/taller-api-muneco.git
cd taller-api-muneco
```

Git te pedirá autenticarte la primera vez que hagas `push`; con `clone` de un repositorio al que tienes acceso normalmente basta con estar autenticado en el navegador o con Git Credential Manager, que se instala con Git para Windows.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `dir` (o `ls`) muestra las carpetas `contrato`, `datos`, `ensamblador`, `etapas`, `fixtures`, `tests` y el archivo `README.md`.

> [!TIP]
> **💡 Tip**
>
> Abre la carpeta en VSCode con `code .` desde la misma terminal. El explorador de archivos de la izquierda te muestra toda la estructura y la terminal integrada ya queda ubicada en la raíz del proyecto.

## 0.3 Entorno virtual e instalación

Igual que en el Taller 1: un entorno virtual por proyecto, para que las versiones de FastAPI y pandas de este taller no interfieran con las de otros.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En macOS o Linux la activación es `source .venv/bin/activate`.

> [!NOTE]
> **📘 Concepto**
>
> `requirements.txt` es la lista de paquetes que el proyecto necesita, con versiones mínimas. Es parte del repositorio precisamente para que **todos instalen lo mismo**. Cuando en el Módulo 3 veas que GitHub Actions instala el proyecto en una máquina limpia, lo hace con este archivo. Si tu código depende de un paquete que no está aquí, funcionará en tu máquina y fallará en la de todos los demás.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `pip list` muestra, entre otros, `fastapi`, `uvicorn`, `pydantic`, `httpx`, `pandas`, `pytest`. La terminal muestra `(.venv)` al inicio de la línea.

> [!WARNING]
> **⚠️ Atención**
>
> Si PowerShell dice que la ejecución de scripts está deshabilitada al activar el entorno, ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a intentar. Está documentado en el Troubleshooting del Módulo 1 del Taller 1.

## 0.4 Correr las pruebas por primera vez

El repositorio incluye pruebas automáticas. Córrelas ahora, antes de tocar nada, para saber cómo se ve el estado inicial:

```powershell
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Seis pruebas marcadas como `skipped` (`ssssss`) y cero errores. Significa: las seis etapas existen pero ninguna está implementada. Es el punto de partida correcto.

> [!NOTE]
> **📘 Concepto**
>
> `pytest` busca archivos que empiecen por `test_` y ejecuta las funciones que empiecen por `test_`. Aquí hay una sola prueba, parametrizada seis veces (una por etapa). Cada una carga la entrada de referencia de la etapa, llama a tu función `procesar` y valida el resultado contra el contrato. Es lo mismo que hace el muñeco, pero sin pantalla: por eso sirve para que GitHub lo corra solo.

## 0.5 Levantar el ensamblador y ver el muñeco vacío

El ensamblador es un servicio más. Se levanta con `uvicorn`, el programa que ejecuta aplicaciones FastAPI (lo verás en detalle en el Módulo 1):

```powershell
uvicorn ensamblador.app:app --port 8000
```

Abre el navegador en `http://localhost:8000`. Deberías ver el muñeco con las seis partes punteadas y una tabla que dice, para cada etapa, que no responde. Es lo esperado: no hay ningún servicio corriendo en los puertos 8001 a 8006.

![](img/muneco_01.png)

*El muñeco al inicio: seis partes ausentes.*

Detén el servidor con `Ctrl + C` en la terminal.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> La página carga, el muñeco aparece punteado y la tabla muestra seis filas en estado AUSENTE con el mensaje "No responde en http://localhost:800N".

> [!TIP]
> **💡 Tip**
>
> La página se recarga sola cada diez segundos. Más adelante, cuando levantes tu etapa, no necesitas hacer nada en el navegador: en el siguiente ciclo tu parte del muñeco aparece.

## 0.6 Recorrer la estructura del repositorio

Dedica diez minutos a abrir cada carpeta. Saber dónde está cada cosa te ahorra horas después.

| Carpeta o archivo | Qué contiene | ¿La tocas? |
|----|----|----|
| `contrato/` | Esquemas de datos (`esquemas.py`), reglas de validación (`validaciones.py`), registro de etapas y puertos (`etapas.py`), fábrica de servicios (`servicio.py`), población objetivo para calibrar | Solo lectura. Cambiarla es un PR de contrato |
| `datos/` | `generar_datos.py` y el CSV sintético que produce | No |
| `fixtures/` | Entrada y salida de referencia de cada etapa, en JSON. Con esto se prueba tu etapa sin depender de las demás | No |
| `etapas/etapa_N_nombre/app.py` | El esqueleto de cada etapa. Tiene una función `procesar` que lanza `NotImplementedError` | **Sí, solo la tuya** |
| `ensamblador/` | `app.py` dibuja el muñeco; `probar.py` prueba una etapa desde la terminal; `encadenar.py` corre el proceso completo | No |
| `tests/` | Prueba de contrato que corre `pytest` y GitHub Actions | No |
| `.github/` | Definición de la integración continua y plantilla de Pull Request | No |
| `scripts/` | Scripts para levantar los siete servicios de una vez | No |
| `apendice_r/` | Ejemplo de una etapa en R con plumber | Solo si vas por R |

> [!NOTE]
> **📘 Concepto**
>
> **Fixtures.** Un fixture es un dato de prueba fijo y conocido. Aquí, `fixtures/etapa_3_entrada.json` es exactamente lo que la etapa 3 recibiría si la etapa 2 estuviera perfecta. Esto rompe la dependencia entre personas: puedes implementar y probar tu etapa desde el primer día, aunque las anteriores no existan. En un proyecto real, esto es lo que permite que un equipo de veinte personas avance en paralelo.

## 0.7 Troubleshooting del Módulo 0

| Síntoma | Causa probable | Solución |
|----|----|----|
| `git clone` dice `Repository not found` | No has aceptado la invitación como colaborador, o el repo es privado y no estás autenticado | Revisa github.com/notifications; acepta la invitación. Reintenta |
| `pip install -r requirements.txt` falla en un paquete | Versión de Python muy vieja o sin internet | `python --version` debe ser 3.11+. Si es 3.9 o 3.10, actualiza Python |
| `uvicorn` no se reconoce como comando | El entorno virtual no está activado | `.venv\Scripts\activate` y reintenta. Debe verse `(.venv)` en la terminal |
| `ModuleNotFoundError: No module named 'contrato'` | Ejecutaste desde otra carpeta | Todos los comandos van desde la **raíz** del repo (donde está `README.md`) |
| El navegador dice que no puede conectar a localhost:8000 | El servidor no arrancó o arrancó en otro puerto | Mira la terminal: debe decir `Uvicorn running on http://127.0.0.1:8000` |
| Puerto 8000 ocupado (`address already in use`) | Otro programa usa el puerto | Cierra la otra terminal con uvicorn, o usa `--port 8010` solo para esta prueba |
