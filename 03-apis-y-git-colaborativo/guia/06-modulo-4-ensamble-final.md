# Módulo 4 — Ensamble final

Objetivo: con las seis etapas mezcladas en `main`, levantar todo el sistema, ver el muñeco completo, correr el proceso de punta a punta y entregar. Una hora.

### Lo que necesitas antes de empezar

- Las seis etapas mezcladas en `main` (o al menos la mayoría: el ejercicio también sirve para ver quién falta).

## 4.1 Actualizar y levantar todo

```powershell
git switch main
git pull
pytest
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `6 passed`. Si alguna dice `skipped`, esa etapa aún no está en `main`; si alguna dice `FAILED`, algo se mezcló sin pasar por CI (no debería ser posible) o un cambio de contrato posterior la rompió.

Levanta los siete servicios. En Windows, el script abre una ventana de PowerShell por servicio y el navegador:

```powershell
.\scripts\levantar_todo.ps1
```

En macOS o Linux: `bash scripts/levantar_todo.sh`. Si prefieres control manual, son siete terminales con `uvicorn ... --port 800N` cada una.

![](img/muneco_03.png)

*Seis etapas en verde: el proceso completo cumple el contrato.*

> [!TIP]
> **💡 Tip**
>
> Si tu PowerShell bloquea el script ("no se puede cargar porque la ejecución de scripts está deshabilitada"), es la misma política del Módulo 0: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## 4.2 Leer el diagnóstico

El ensamblador prueba cada etapa **por separado**, con su fixture de entrada. Eso significa que una etapa puede estar verde aunque la anterior esté chueca: es correcto, porque lo que se evalúa es el cumplimiento individual del contrato. La tabla al lado del muñeco te dice, para cada parte, la lista exacta de reglas que fallaron. Si hay algo chueco en la demo, la conversación del equipo es: ¿es la etapa o es el contrato? Ambas respuestas son válidas y ambas terminan en un PR.

También puedes consultar `http://localhost:8000/estado`, que devuelve el mismo diagnóstico en JSON. Es la forma en que otro programa (un tablero, un monitor) consumiría el ensamblador.

## 4.3 Correr el proceso de verdad: encadenar

Hasta aquí cada etapa recibió datos de referencia. Ahora vamos a correr el proceso real: el CSV entra a la etapa 1, lo que sale de la 1 entra a la 2, y así hasta el Excel final.

```powershell
python -m ensamblador.encadenar
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Seis líneas `OK`, un `salida/resultado_final.json` y `salida/tabulados.xlsx`. Ábrelo: doce filas con valor, error estándar, CV, intervalo y calidad.

En este modo no se compara contra la referencia (solo coherencia interna), porque el resultado depende de las decisiones de cada etapa real. Compara tus tabulados con `fixtures/etapa_6_salida.json`: deberían parecerse, y las diferencias deberían poder explicarse por las decisiones documentadas (método de imputación, tratamiento de atípicos).

> [!NOTE]
> **📘 Concepto**
>
> Acabas de ver la diferencia entre **prueba unitaria** (cada etapa con datos controlados, aislada) y **prueba de integración** (todo el sistema con datos reales, encadenado). Las dos son necesarias. La primera te dice *quién* falló; la segunda te dice *si* el conjunto funciona. Un sistema con solo pruebas de integración es difícil de depurar; uno con solo unitarias puede tener seis piezas perfectas que no encajan.

## 4.4 Entregable: Issue de cierre

Crea un Issue en el repositorio con el título `Cierre Taller 3 — [tu nombre]` y este contenido:

```text
Hola @OmarCorrea26,

Cierre de mi participación en el Taller 3.

**Mi etapa:** N — nombre (parte del muñeco)
**PR mezclado:** #número
**Revisé el PR de:** @usuario (#número)

**Decisiones que tomé y por qué:**
- ...

**Lo que más me costó:**
- ...

**Una cosa que haría distinto la próxima vez:**
- ...

**Captura del muñeco completo** (arrastra la imagen aquí)
```

La reflexión no es trámite. Escribir qué te costó es lo que convierte tres semanas de pelear con JSON y rebase en aprendizaje que se queda.

## 4.5 Para profundizar (opcional)

- **Tipar la entrada.** Cambia tu `procesar` para que empiece con `datos = EntradaN.model_validate(entrada)`. Verás errores más claros y el editor te autocompletará los campos.
- **Pruebas propias.** Agrega en `tests/` un archivo `test_etapa_N.py` con casos que el contrato no cubre: un dominio vacío, todos los ingresos nulos, un departamento con una sola persona.
- **Docker.** Empaquetar cada etapa en un contenedor es el paso natural para que corra igual en cualquier máquina. Un `Dockerfile` de diez líneas por etapa y un `docker-compose.yml` que levante las siete.
- **Kedro + API.** Tu etapa podría ser un nodo de un pipeline de Kedro expuesto por FastAPI: el pipeline organiza el proceso, la API lo hace consumible. Es una arquitectura común en equipos de datos.
- **Autenticación.** Ninguna API real es pública sin control. FastAPI tiene soporte para tokens (`fastapi.security`); el tutorial oficial tiene una sección "Security".
- **Versionar el contrato.** Cuando un cambio de esquema rompe clientes, la práctica es publicar `/v2/procesar` y mantener `/v1/` un tiempo. Piensa cómo lo harías con `contrato/esquemas.py`.

## Cierre del taller

Lo que hiciste, en orden: construiste un servicio que expone una función estadística mediante un contrato explícito; lo probaste contra ese contrato de forma automática; lo llevaste a un repositorio compartido por una rama propia; lo sometiste a revisión de un par y a integración continua; lo mantuviste al día con un `main` que cambió debajo de ti; y lo integraste con el trabajo de otras cinco personas hasta que el conjunto funcionó. Cada una de esas cosas es una práctica estándar en cualquier equipo que desarrolla software, y ahora tienes una experiencia concreta de cada una con la que comparar lo que te encuentres después.

El muñeco se olvida. Lo que queda es el reflejo: antes de decir "ya está", preguntarse **¿contra qué contrato lo probé, quién lo revisó, y sobre qué versión de main está?**
