# Módulo 1 — Qué es una API y cómo se construye una con FastAPI

Objetivo: entender qué problema resuelve una API, cómo funciona una petición HTTP, y construir tu primer servicio con FastAPI, incluyendo validación automática de datos con Pydantic. Unas dos horas.

### Lo que necesitas antes de empezar

- Módulo 0 completado.
- Recordar cómo escribir una función en Python con parámetros y `return` (Módulo 2 del Taller 1).

## 1.1 El problema que resuelve una API

En el Taller 1 hiciste `from analisis_v2 import promedio_por_grupo`. Eso funciona si el archivo está en tu máquina, en tu entorno virtual, en tu versión de pandas. Ahora imagina que el equipo de calibración trabaja en R, que el equipo de publicación necesita el resultado desde un tablero de Power BI, y que la imputación la mantiene otra dirección. Importar archivos ya no sirve.

Una **API** (interfaz de programación de aplicaciones) resuelve esto poniendo una **ventanilla** delante de tu código. Cualquiera puede acercarse a la ventanilla, entregar una solicitud en un formato acordado y recibir una respuesta en otro formato acordado. No necesita saber qué hay detrás: si es Python o R, si usa pandas o data.table. Solo necesita conocer el formato: eso es el **contrato**.

> [!NOTE]
> **📘 Concepto**
>
> La analogía con la estadística oficial es directa. Un formulario de recolección es un contrato: define qué preguntas se hacen, en qué orden, con qué categorías. El encuestador no necesita saber cómo se va a procesar; el procesador no necesita saber quién encuestó. Mientras ambos respeten el formulario, el proceso funciona. Una API es un formulario para programas.

Casi todo lo que usas a diario en la web consume APIs: cuando una aplicación muestra el clima, pidió los datos a una API de un servicio meteorológico; cuando el portal de datos abiertos deja descargar una tabla, suele exponerla también por API para que otros programas la consulten sin abrir el navegador.

## 1.2 HTTP en diez minutos

Las APIs que construimos aquí hablan **HTTP**, el mismo protocolo del navegador. Una interacción HTTP tiene dos partes: una **petición** (request) que envía el cliente y una **respuesta** (response) que devuelve el servidor.

| Elemento de la petición | Qué es | En nuestro taller |
|----|----|----|
| Método (verbo) | Qué quieres hacer: `GET` leer, `POST` enviar datos para procesar, `PUT` actualizar, `DELETE` borrar | `GET /salud` para ver si el servicio vive; `POST /procesar` para enviarle datos |
| Ruta (path) | A qué recurso del servidor te diriges | `/salud`, `/procesar`, `/docs` |
| Cuerpo (body) | Los datos que envías, casi siempre en JSON | El JSON con los registros de la encuesta |
| Cabeceras (headers) | Metadatos: tipo de contenido, autenticación | `Content-Type: application/json` (FastAPI lo maneja solo) |

La respuesta trae un **código de estado**, un número de tres cifras que resume qué pasó. Vas a ver estos:

| Código | Significado | Cuándo lo verás aquí |
|----|----|----|
| 200 | OK: todo bien | Tu etapa procesó y devolvió resultado |
| 404 | Not Found: la ruta no existe | Escribiste mal la URL (`/procesa` en vez de `/procesar`) |
| 422 | Unprocessable Entity: el cuerpo no tiene la forma esperada | Pydantic rechazó los datos de entrada |
| 500 | Internal Server Error: el código del servidor falló | Tu `procesar` lanzó una excepción (un `KeyError`, una división por cero) |
| 501 | Not Implemented: la ruta existe pero no hace nada aún | Tu etapa todavía lanza `NotImplementedError`. El muñeco lo muestra como ausente |

> [!NOTE]
> **📘 Concepto**
>
> **JSON** (JavaScript Object Notation) es el formato de intercambio universal de las APIs. Se parece a un diccionario de Python: llaves entre comillas, valores que pueden ser números, texto, `true`/`false`, `null`, listas o más diccionarios. La diferencia importante: JSON no tiene `NaN` ni tipos de numpy. Cuando conviertas un DataFrame a JSON vas a tener que cuidar eso, y lo veremos en el Módulo 2.

## 1.3 Tu primer servicio con FastAPI

FastAPI es una librería de Python para construir APIs. Su gracia es que hace el trabajo pesado (leer la petición, convertir el JSON, validar tipos, generar documentación) a partir de funciones normales de Python con anotaciones de tipo. Para practicar sin tocar el repositorio, crea una carpeta aparte:

```powershell
cd ..
mkdir practica-api
cd practica-api
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn httpx
```

Crea un archivo `hola_api.py` con este contenido:

```python
# hola_api.py — primer servicio
from fastapi import FastAPI

app = FastAPI(title="Mi primera API")

@app.get("/salud")
def salud():
    return {"estado": "ok", "mensaje": "El servicio está vivo"}

@app.get("/saludo/{nombre}")
def saludo(nombre: str, formal: bool = False):
    if formal:
        return {"saludo": f"Buenos días, {nombre}."}
    return {"saludo": f"¡Hola, {nombre}!"}
```

### Línea por línea

- `app = FastAPI(...)` crea la aplicación. Es el objeto que `uvicorn` va a ejecutar.
- `@app.get("/salud")` es un **decorador**: le dice a FastAPI que la función de abajo responde a peticiones `GET` en la ruta `/salud`. La función devuelve un diccionario; FastAPI lo convierte en JSON.
- `/saludo/{nombre}` tiene un **parámetro de ruta**: lo que escribas en la URL después de `/saludo/` llega a la función como `nombre`. La anotación `: str` no es decorativa: FastAPI la usa para validar.
- `formal: bool = False` es un **parámetro de consulta** (query): se pasa como `?formal=true` en la URL. Como tiene valor por defecto, es opcional.

Levanta el servicio:

```powershell
uvicorn hola_api:app --reload
```

> [!NOTE]
> **📘 Concepto**
>
> `uvicorn` es un **servidor ASGI**: el programa que abre el puerto, escucha peticiones y se las pasa a tu aplicación. FastAPI define qué hacer; uvicorn hace que suceda. `hola_api:app` significa "el objeto `app` dentro del archivo `hola_api.py`". `--reload` reinicia el servidor cada vez que guardas el archivo, ideal mientras desarrollas.

Abre en el navegador `http://localhost:8000/salud`, luego `http://localhost:8000/saludo/Omar` y luego `http://localhost:8000/saludo/Omar?formal=true`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Ves el JSON de cada respuesta en el navegador. El tercero dice "Buenos días, Omar."

Ahora prueba `http://localhost:8000/saludo/Omar?formal=quizas`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Respuesta con código 422 y un JSON que explica que `formal` debe ser booleano. No escribiste una sola línea de validación: FastAPI la dedujo de la anotación `bool`.

## 1.4 La documentación automática

Abre `http://localhost:8000/docs`. FastAPI genera, a partir de tus funciones, una página interactiva (Swagger UI) que lista todas las rutas, sus parámetros, y permite probarlas desde el navegador con el botón "Try it out".

Esto es más importante de lo que parece. Es la **documentación del contrato**, siempre actualizada porque sale del código. Cuando en el Módulo 2 levantes tu etapa, `http://localhost:800N/docs` es lo que le mostrarías a un compañero para explicarle qué recibe y qué devuelve tu servicio.

> [!TIP]
> **💡 Tip**
>
> Hay una segunda vista en `http://localhost:8000/redoc`, más de lectura. Y en `http://localhost:8000/openapi.json` está la especificación cruda en formato OpenAPI, el estándar que usan herramientas externas para generar clientes automáticamente.

## 1.5 Recibir datos: POST y Pydantic

Con `GET` pasas parámetros en la URL. Cuando lo que envías es un conjunto de datos (mil registros de una encuesta), eso va en el cuerpo de una petición `POST`, en JSON. Y ahí entra **Pydantic**: la librería que FastAPI usa para definir la forma exacta de ese JSON y validarla.

Agrega esto al final de `hola_api.py`:

```python
from pydantic import BaseModel, Field
from statistics import mean

class Muestra(BaseModel):
    nombre: str
    valores: list[float] = Field(min_length=1)

class Resumen(BaseModel):
    nombre: str
    n: int
    promedio: float

@app.post("/resumir", response_model=Resumen)
def resumir(muestra: Muestra):
    return Resumen(nombre=muestra.nombre, n=len(muestra.valores), promedio=mean(muestra.valores))
```

- `Muestra` es un **modelo**: describe que el JSON de entrada debe tener un `nombre` (texto) y una lista `valores` de números con al menos un elemento. Si llega algo distinto, FastAPI responde 422 antes de ejecutar tu función.
- `Resumen` es el modelo de salida. `response_model=Resumen` hace dos cosas: documenta en `/docs` qué devuelves, y **verifica** que lo que devuelves cumple esa forma. Si tu función devolviera un diccionario sin `promedio`, el error sería tuyo y se vería.
- Dentro de la función, `muestra` ya no es un diccionario: es un objeto con atributos tipados. `muestra.valores` es una lista de `float`, garantizado.

Guarda (el servidor se reinicia solo), ve a `/docs`, abre `POST /resumir`, "Try it out", y envía:

```json
{"nombre": "ingreso urbano", "valores": [1200000, 1850000, 990000]}
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Respuesta 200 con `n: 3` y el promedio. Ahora borra la lista y deja `"valores": []`: respuesta 422 que dice que la lista debe tener al menos un elemento.

> [!NOTE]
> **📘 Concepto**
>
> Pydantic es el corazón del contrato de este taller. Abre `contrato/esquemas.py` del repositorio y vas a reconocer exactamente esta estructura: modelos con campos tipados, `Optional` para lo que puede ser nulo, `Field(ge=0, le=1)` para acotar rangos. `extra="forbid"` en la clase base significa que si tu etapa devuelve un campo que no está declarado, es error: el contrato es explícito en las dos direcciones.

## 1.6 Consumir una API desde Python

Hasta ahora usaste el navegador como cliente. Un programa también puede ser cliente. Con el servidor corriendo, en **otra** terminal (activa el entorno virtual) crea `cliente.py`:

```python
# cliente.py — consume la API desde Python
import httpx

r = httpx.get("http://localhost:8000/saludo/Ana", params={"formal": True})
print(r.status_code, r.json())

datos = {"nombre": "edad rural", "valores": [34, 51, 27, 60]}
r = httpx.post("http://localhost:8000/resumir", json=datos)
print(r.status_code, r.json())

r = httpx.post("http://localhost:8000/resumir", json={"nombre": "vacio", "valores": []})
print(r.status_code, r.json()["detail"][0]["msg"])
```

```powershell
python cliente.py
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Tres líneas: `200 {...}`, `200 {...}` con el promedio 43.0, y `422` con el mensaje de validación.

Esto es exactamente lo que hace el ensamblador con tu etapa: `httpx.post("http://localhost:800N/procesar", json=entrada)` y luego valida `r.json()`. Ábrelo: `ensamblador/verificar.py` tiene menos de sesenta líneas y ya puedes leerlo completo.

> [!TIP]
> **💡 Tip**
>
> `httpx` y `requests` hacen lo mismo; usamos `httpx` porque además soporta llamadas asíncronas, que no necesitas ahora pero verás en proyectos más grandes. En R, el equivalente es `httr2`.

## 1.7 Leer la fábrica de servicios del repositorio

Vuelve al repositorio del taller y abre `contrato/servicio.py`. Ahora tienes todo lo necesario para entenderlo:

- `crear_app(numero, procesar)` recibe el número de tu etapa y **tu función** `procesar`, y devuelve una aplicación FastAPI ya armada.
- `GET /salud` devuelve el número y nombre de la etapa. Sirve para comprobar que el servicio vive sin enviarle datos.
- `POST /procesar` lee el JSON del cuerpo (`await request.json()`), lo pasa a tu función y devuelve lo que ella retorne.
- Si tu función lanza `NotImplementedError`, responde **501**; el ensamblador lo interpreta como "ausente". Cualquier otra excepción responde **500** con el nombre del error; el ensamblador lo interpreta como "chueco" y te muestra el mensaje en la tabla.

La decisión de diseño importante: la validación del contrato **no** está en el servicio de cada etapa, sino en el ensamblador y en las pruebas. Tu servicio solo recibe y devuelve diccionarios. Eso te da libertad para implementar como quieras y deja la verificación en un solo lugar, que es de todos.

> [!WARNING]
> **⚠️ Atención**
>
> Podrías preguntarte por qué `procesar` recibe un `dict` y no un modelo Pydantic tipado, como en 1.5. Es deliberado: queremos que tú conviertas el JSON a DataFrame y de vuelta, porque ahí está la mitad de los errores reales (nulos, tipos, nombres de columnas). Cuando domines eso, el paso natural es tipar la entrada con `Entrada3.model_validate(entrada)` al inicio de tu función, y es una buena práctica que puedes adoptar.

## 1.8 Buenas prácticas al construir APIs

- **Una ruta hace una cosa.** `/procesar` procesa. No mezcles "procesar y también guardar en disco y también enviar correo".
- **El contrato es explícito.** Declara modelos de entrada y salida. Un campo que "a veces viene" es un error esperando ocurrir.
- **Códigos de estado honestos.** No devuelvas 200 con `{"error": "algo falló"}` adentro. Si falló, es 4xx o 5xx. El cliente decide qué hacer según el código, no leyendo mensajes.
- **El servicio no tiene estado.** Cada petición trae todo lo que necesita. No guardes resultados en variables globales "para la próxima llamada": con dos clientes a la vez se mezclan.
- **Nombres estables.** Cambiar el nombre de un campo rompe a todos los clientes. Por eso `contrato/` se cambia con PR revisado por el equipo, nunca por cuenta propia.
- **Documenta las decisiones estadísticas en el código.** Qué método de imputación, qué percentil de recorte, qué fórmula de varianza. El siguiente que lea tu etapa (o tú en seis meses) necesita saber por qué, no solo qué.

## 1.9 Troubleshooting del Módulo 1

| Síntoma | Causa probable | Solución |
|----|----|----|
| `Error loading ASGI app. Could not import module "hola_api"` | Estás en otra carpeta, o el archivo se llama distinto | `cd` a la carpeta del archivo; revisa que se llame exactamente `hola_api.py` |
| `Attribute "app" not found in module` | Escribiste `App = FastAPI()` o un nombre distinto | El objeto debe llamarse `app`, o cambia el comando a `hola_api:nombre_real` |
| El navegador muestra `{"detail":"Not Found"}` | La ruta no existe | Revisa la ortografía; mira las rutas disponibles en `/docs` |
| 422 cuando estás seguro de que el JSON está bien | Una comilla simple, una coma final, o el tipo no coincide | Copia el JSON en `/docs`, que te marca la línea. Los textos van con comillas dobles |
| Cambias el archivo y el servidor no se entera | Arrancaste sin `--reload` | Detén con `Ctrl + C` y arranca con `--reload` |
| `httpx.ConnectError` en `cliente.py` | El servidor no está corriendo, o corre en otro puerto | Verifica en la primera terminal que uvicorn siga vivo y en qué puerto |

## 1.10 Para profundizar (opcional)

- Documentación oficial de FastAPI, sección "Tutorial - User Guide": está en español y es de las mejores que existen. Lee "Path Parameters", "Query Parameters", "Request Body" y "Response Model".
- Documentación de Pydantic v2, sección "Models" y "Fields": para entender `Field`, validadores y `model_config`.
- Reto: agrega a `hola_api.py` una ruta `POST /mediana` que reciba el mismo modelo `Muestra` y devuelva la mediana. Luego una `GET /estadisticas/{variable}` que devuelva 404 si la variable no está en una lista fija. Usa `from fastapi import HTTPException` y `raise HTTPException(status_code=404, detail="...")`.
