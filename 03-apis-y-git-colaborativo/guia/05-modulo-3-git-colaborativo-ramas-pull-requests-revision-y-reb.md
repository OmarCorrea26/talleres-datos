# Módulo 3 — Git colaborativo: ramas, Pull Requests, revisión y rebase

Objetivo: llevar tu etapa al repositorio compartido siguiendo el flujo de un equipo: rama propia, commits con convención, Pull Request, revisión de un compañero, integración continua en verde y rebase cuando `main` cambie debajo de ti. Este módulo no se hace solo: coordina con el equipo. Unas tres horas de trabajo propio, repartidas en varios días.

### Lo que necesitas antes de empezar

- Módulo 2 completado (tu etapa en OK).
- Módulo 3 del Taller 1 fresco: `add`, `commit`, `push`, `.gitignore`, qué es el remoto `origin`.

## 3.1 Qué cambia cuando el repositorio es de todos

En el Taller 1, `git push` era el final del trabajo. Aquí es el principio. Con seis personas en un repositorio aparecen tres problemas nuevos y Git tiene un mecanismo para cada uno:

| Problema | Mecanismo | Dónde lo ves en este taller |
|----|----|----|
| Dos personas cambian archivos al mismo tiempo | **Ramas**: cada quien trabaja en una copia paralela de la historia y se integran después | Una rama `feature/etapa-N-...` por persona; `main` no se toca directo |
| Alguien sube código roto que afecta a los demás | **Pull Request + revisión + integración continua**: nada llega a `main` sin ojos humanos y pruebas automáticas | GitHub Actions corre `pytest` en cada PR; un compañero revisa |
| `main` avanzó mientras trabajabas y tu rama quedó desactualizada | **Rebase**: reescribe tu rama como si hubieras empezado desde el `main` actual | El cambio de contrato planeado a mitad del taller |

> [!NOTE]
> **📘 Concepto**
>
> Una **rama** es un puntero a un commit. `main` apunta al último commit de la historia principal. Cuando creas `feature/etapa-3`, creas un segundo puntero en el mismo commit. Cada commit que haces mueve tu puntero; `main` se queda donde estaba. Nada se copia: es la misma historia con dos cabezas. Por eso crear ramas es instantáneo y gratis, y por eso se recomienda usarlas para todo.

## 3.2 El modelo de ramas del taller

- `main` es la rama de integración. Está **protegida**: GitHub rechaza cualquier `push` directo. Solo recibe cambios por Pull Request aprobado y con pruebas en verde. Lo que hay en `main` es, por definición, lo que funciona.
- `feature/etapa-N-nombre-tunombre` es tu rama de trabajo. Sale de `main`, vive lo que dure tu etapa, y muere cuando se mezcla.
- `contrato/...` son ramas para cambios al contrato. Las abre el facilitador (o quien lo proponga por Issue) y las revisa todo el equipo.

La convención de nombres no es capricho: cuando el repositorio tiene doce ramas, `feature/etapa-3-calibrar-ana` dice qué es, de quién es y a qué etapa pertenece sin abrirla.

## 3.3 Crear tu rama

Siempre desde un `main` actualizado:

```powershell
git switch main
git pull
git switch -c feature/etapa-3-calibrar-ana
```

- `git switch main` te lleva a la rama principal (`checkout` hace lo mismo; `switch` es la forma moderna y menos ambigua).
- `git pull` trae lo último del remoto. **Nunca crees una rama desde un **`main`** viejo.**
- `git switch -c` crea la rama y te cambia a ella en un solo paso.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `git branch` muestra tu rama con un asterisco. `git status` dice `On branch feature/etapa-3-calibrar-ana` y `nothing to commit`.

> [!WARNING]
> **⚠️ Atención**
>
> Si ya editaste `app.py` en el Módulo 2 estando en `main`, no pasa nada: los cambios sin commit se llevan contigo al cambiar de rama. Crea la rama ahora y haz el commit ahí. Lo que sí sería un problema es haber hecho commit en `main`; si te pasó, ve a la sección 3.11.

## 3.4 Commits que cuentan una historia

Un commit es una unidad de cambio con un mensaje. En un repositorio compartido, el mensaje lo van a leer otros, dentro de meses, buscando por qué algo está como está. Usamos la convención **Conventional Commits**:

```text
tipo(alcance): descripción en imperativo, minúscula, sin punto final

feat(etapa-3): calibrar factores por departamento con posestratificación
fix(etapa-3): convertir factor_calibrado a float antes de exportar
docs(etapa-3): documentar la razón de ajuste en el resumen
test(etapa-3): cubrir el caso de departamento sin registros
```

| Tipo | Cuándo |
|----|----|
| `feat` | Funcionalidad nueva (la primera versión de tu etapa) |
| `fix` | Corrección de un error |
| `refactor` | Reorganizar código sin cambiar lo que hace |
| `docs` | Comentarios, README, docstrings |
| `test` | Pruebas |
| `chore` | Mantenimiento: dependencias, configuración |

Haz tu primer commit de la etapa:

```powershell
git add etapas/etapa_3_calibrar/app.py
git commit -m "feat(etapa-3): calibrar factores por departamento con posestratificación"
```

> [!WARNING]
> **⚠️ Atención**
>
> `git add .` agrega **todo** lo que cambió, incluyendo `salida/tabulados.xlsx` o un notebook de exploración que dejaste en la raíz. Agrega por nombre de archivo, o revisa con `git status` qué vas a incluir antes de `git add .`. El `.gitignore` cubre lo obvio (`.venv`, `salida/`, `__pycache__`), pero no adivina tus archivos de prueba.

> [!TIP]
> **💡 Tip**
>
> Commits pequeños y frecuentes. "Implementar la etapa" en un solo commit de 200 líneas es difícil de revisar; tres commits (estructura básica, lógica de calibración, resumen y exportación) se leen solos. Si ya hiciste todo junto, no te preocupes esta vez.

## 3.5 Subir la rama y abrir el Pull Request

```powershell
git push -u origin feature/etapa-3-calibrar-ana
```

`-u` vincula tu rama local con la remota; a partir de ahí basta `git push`. GitHub responde en la terminal con un enlace para crear el Pull Request. Ábrelo, o ve al repositorio en el navegador: verás un aviso amarillo "Compare & pull request".

> [!NOTE]
> **📘 Concepto**
>
> Un **Pull Request** (PR) es una solicitud formal: "tengo estos cambios en mi rama, pido que se integren a `main`". No es solo un botón de mezclar: es un espacio de conversación con la diferencia (diff) línea por línea, comentarios, aprobaciones y el resultado de las pruebas automáticas. En muchos equipos es **el** lugar donde ocurre la transferencia de conocimiento.

Al abrir el PR, GitHub carga la plantilla del repositorio (`.github/pull_request_template.md`). Llénala completa: qué etapa, qué decisiones tomaste, y marca el checklist solo si es verdad. Asigna como revisor (panel derecho, "Reviewers") al compañero que te corresponda según lo acordado con el equipo.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El PR existe, apunta de tu rama a `main`, tiene descripción, un revisor asignado, y en la parte inferior aparece el check "Pruebas de contrato" corriendo (círculo amarillo) o terminado (verde o rojo).

## 3.6 Integración continua: leer lo que dice GitHub Actions

Al abrir el PR se dispara el flujo definido en `.github/workflows/contrato.yml`: GitHub arranca una máquina virtual limpia con Ubuntu, instala Python 3.12, instala `requirements.txt` y corre `pytest -v`. Si todo pasa, check verde. Si algo falla, check rojo y la rama protegida no permite mezclar.

Haz clic en "Details" junto al check para ver el registro. Está organizado en pasos; abre el paso `pytest -v`. Verás la misma salida que en tu terminal.

> [!NOTE]
> **📘 Concepto**
>
> **Integración continua** (CI) significa que cada cambio se integra y se prueba de inmediato, en una máquina que no es la tuya. La frase "en mi máquina funciona" deja de ser un argumento. Fíjate en lo que revela: si tu etapa lee un archivo con ruta absoluta, o usa un paquete que instalaste pero no está en `requirements.txt`, pasará en tu PC y fallará en CI. Eso no es una molestia: es el sistema haciendo su trabajo.

> [!WARNING]
> **⚠️ Atención**
>
> Las pruebas de las etapas de tus compañeros que aún no están en `main` aparecen como `skipped`. Es normal. Lo que te concierne es que la tuya diga `PASSED` y ninguna diga `FAILED`.

## 3.7 Revisar código (y recibir revisión)

Cada persona revisa el PR de otra. Revisar no es aprobar por cortesía: es la segunda línea de defensa después de las pruebas, y la primera para todo lo que las pruebas no ven (claridad, decisiones estadísticas, mantenibilidad).

### Cómo revisar

1. Lee la descripción del PR. Si no explica qué decisiones tomó, pídelo antes de leer código.
1. Trae la rama a tu máquina y **ejecútala**: `git fetch origin` y luego `git switch feature/etapa-3-calibrar-ana`. Levanta su servicio y corre `probar --etapa 3`. Confiar en el check verde está bien; verlo correr en tu máquina es mejor, y además aprendes de su código.
1. Lee el diff en GitHub, archivo por archivo. Comenta **en la línea** (pasa el ratón sobre el número de línea, aparece un `+`). Preguntas concretas: "¿por qué la mediana y no la media?", "esta ruta es absoluta, en CI va a fallar", "esta función hace tres cosas; ¿la separamos?".
1. Distingue lo que bloquea de lo que sugiere. Un error de contrato o una ruta absoluta bloquea; un nombre de variable mejorable es una sugerencia. Dilo explícitamente: "(bloqueante)" o "(sugerencia)".
1. Termina con "Review changes": **Approve** si se puede mezclar (con o sin sugerencias menores), **Request changes** si hay algo bloqueante, **Comment** si solo preguntas.

### Cómo recibir revisión

- Los comentarios son sobre el código, no sobre ti. Responde a cada uno: aplicando el cambio, o explicando por qué no.
- Los ajustes van como commits nuevos en la misma rama (`fix(etapa-3): ...`) y `git push`. El PR se actualiza solo; no abras otro.
- Cuando apliques un cambio pedido, marca la conversación como resuelta ("Resolve conversation") y avisa: "Listo, ajustes aplicados".

> [!TIP]
> **💡 Tip**
>
> La revisión más útil que puedes hacer es correr el código del otro con un caso que no pensó. Por ejemplo, para la etapa 2: ¿qué pasa si un grupo entero de área × sexo no tiene ningún ocupado con ingreso? ¿La mediana de imputación es `NaN`? Ese comentario vale más que diez sobre estilo.

## 3.8 Rebase: traer main actualizado a tu rama

Este es el corazón del módulo. Mientras trabajabas, `main` cambió: se mezcló la etapa de un compañero, o el facilitador mezcló un cambio de contrato. Tu rama salió de un `main` que ya no existe. Antes de mezclar, tu rama tiene que **ponerse al día**.

> [!NOTE]
> **📘 Concepto**
>
> Hay dos formas de traer `main` a tu rama. **Merge** crea un commit extra que une las dos historias; funciona, pero deja una historia enredada, llena de "Merge branch 'main' into feature/...". **Rebase** toma tus commits, los pone a un lado, avanza tu rama hasta el `main` actual, y vuelve a aplicar tus commits uno por uno encima. El resultado es una historia lineal, como si hubieras empezado hoy. En este taller usamos rebase para ramas propias, que es la práctica más común en equipos que valoran una historia legible.

Antes y después, en forma de dibujo (cada letra es un commit):

```text
Antes:            A---B---C  main
                       \
                        D---E  feature/etapa-3   (salió de B)

Después de rebase: A---B---C  main
                           \
                            D'---E'  feature/etapa-3   (ahora sale de C)
```

`D'` y `E'` son tus mismos cambios, pero son commits nuevos (tienen otro identificador porque su padre cambió). Esa es la razón de todas las advertencias que siguen.

### Los comandos

```powershell
git switch feature/etapa-3-calibrar-ana   # estar en tu rama
git status                                 # sin cambios pendientes
git fetch origin                           # trae el remoto sin tocar tus archivos
git rebase origin/main                     # reaplica tus commits sobre main
```

- `fetch` es distinto de `pull`: descarga la información del remoto y actualiza `origin/main`, pero no modifica tu rama. Es la forma segura de "mirar qué hay" antes de decidir.
- `rebase origin/main` es lo que hace el trabajo. Si tus commits no tocan los mismos archivos que cambiaron en `main`, termina en un segundo con `Successfully rebased`. Si sí los tocan, aparece un **conflicto**.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `git log --oneline -5` muestra tus commits encima de los últimos de `main`. `git status` dice `Your branch and 'origin/feature/...' have diverged`: es correcto, tu rama local ya es distinta de la que subiste antes.

### Resolver un conflicto

Un conflicto ocurre cuando `main` y tu commit cambiaron **las mismas líneas** del mismo archivo. Git no adivina cuál versión es la buena; te lo pregunta. La terminal dirá algo como:

```text
CONFLICT (content): Merge conflict in etapas/etapa_3_calibrar/app.py
error: could not apply a1b2c3d... feat(etapa-3): ...
Resolve all conflicts manually, mark them as resolved with "git add/rm <conflicted_files>",
then run "git rebase --continue".
```

Abre el archivo en VSCode. Verás marcas:

```text
<<<<<<< HEAD
    version_contrato = "1.1"          # lo que hay en main
=======
    razon = objetivo[d] / suma[d]      # lo que hay en tu commit
>>>>>>> a1b2c3d (feat(etapa-3): ...)
```

1. Decide qué debe quedar. A veces es una de las dos versiones; a menudo son **las dos**, en el orden correcto. VSCode ofrece botones ("Accept Current", "Accept Incoming", "Accept Both"); úsalos si te sirven, pero **lee** el resultado.
1. Borra las marcas `<<<<<<<`, `=======`, `>>>>>>>`. No puede quedar ninguna.
1. Verifica que el archivo funciona: levanta el servicio y corre `probar`. Un conflicto "resuelto" que no corre no está resuelto.
1. `git add etapas/etapa_3_calibrar/app.py` y luego `git rebase --continue`. Si tienes varios commits, Git puede detenerse otra vez en el siguiente; repite.
1. Si te enredaste y quieres volver a como estabas antes de empezar: `git rebase --abort`. No se pierde nada.

> [!NOTE]
> **📘 Concepto**
>
> En un rebase, `HEAD` ("Current" en VSCode) es la versión de `main`, y "Incoming" es la de **tu commit**. Es al revés de lo que intuitivamente esperarías, y al revés de un merge. Es la fuente de error número uno al resolver conflictos en rebase. Léelo dos veces.

### Subir la rama después del rebase

Como tus commits son ahora `D'` y `E'`, el remoto todavía tiene `D` y `E`. Un `git push` normal es rechazado ("non-fast-forward"). Hay que decirle a Git que sí, que quieres reemplazar la historia remota de **tu** rama:

```powershell
git push --force-with-lease
```

> [!WARNING]
> **⚠️ Atención**
>
> `--force-with-lease` y no `--force`. La diferencia: `--force-with-lease` se niega a sobreescribir si alguien más subió algo a tu rama desde tu último `fetch`; `--force` arrasa con todo. En una rama tuya son casi equivalentes, pero acostúmbrate a la versión segura. Y la regla de oro: **nunca hagas rebase (ni push forzado) de una rama que otros también usan**, y en particular nunca de `main`. Estás reescribiendo historia que otros tienen; les rompes el repositorio.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El PR en GitHub se actualiza solo, muestra tus commits sobre los últimos de `main`, y el check de CI vuelve a correr. Si sigue verde, estás listo para mezclar.

## 3.9 El cambio de contrato (evento del taller)

En algún momento, cuando varias ramas estén abiertas, el facilitador anuncia por un Issue un **cambio de contrato**: por ejemplo, agregar un campo obligatorio a un `resumen`, o mover un umbral de calidad. Lo mezcla a `main` por un PR de tipo `contrato`, que todos deben revisar.

Lo que tienes que hacer, en este orden:

1. Leer el Issue y el diff del PR de contrato. Entender **si te afecta**: ¿cambió `SalidaN` de tu etapa? ¿Cambió una validación que te aplica?
1. Hacer `git fetch origin` y `git rebase origin/main` en tu rama (sección 3.8). Como no tocaste `contrato/`, normalmente no hay conflicto.
1. Si te afecta, adaptar tu etapa, probar, commit `fix(etapa-N): adaptar al contrato 1.1`, `git push --force-with-lease`.
1. Si no te afecta, igual haces el rebase: tu rama debe salir del `main` actual para que CI pruebe tu etapa **con el contrato actual**, no con el viejo.

Esto es exactamente lo que pasa en un proyecto real cuando cambia un esquema de base de datos o el formato de un archivo de intercambio. La diferencia es que aquí sabes que va a pasar y el daño es cero.

## 3.10 Coordinación: Issues, asignaciones y avisos

- **Issues** para todo lo que no sea código: dudas sobre el contrato, propuestas de cambio, reportes de que algo en `main` no funciona. Un Issue por tema, título descriptivo, menciona con `@usuario` a quien deba responder.
- **Asignación de revisores** acordada al inicio: 1 revisa a 2, 2 a 3, ... 6 a 1. Así nadie queda sin revisor y nadie revisa dos.
- **Avisa antes de mezclar algo que afecta a otros.** En este taller solo el facilitador mezcla, pero la práctica es general: un comentario en el PR ("esto cambia el orden de las columnas, etapa 2 y 3 revisen") ahorra una tarde de depuración ajena.
- **No trabajes en silencio.** Si vas a tardar, si te bloqueaste, si vas a cambiar de método: escríbelo en tu PR o en el Issue de tu etapa. Un equipo no es seis personas trabajando cerca; es seis personas que saben en qué están las otras cinco.

## 3.11 Comandos de rescate

Cosas que van a pasar, y cómo salir:

| Situación | Comando | Nota |
|----|----|----|
| Quiero ver qué cambié antes de hacer commit | `git diff` | Solo lo no agregado. `git diff --staged` para lo agregado con `add` |
| Quiero ver la historia | `git log --oneline --graph --all` | Con `--all` ves todas las ramas; el gráfico muestra de dónde sale cada una |
| Hice cambios en el archivo equivocado y quiero descartarlos | `git restore ruta/archivo.py` | Irreversible: vuelve a la versión del último commit |
| Hice `git add` de algo que no debía | `git restore --staged ruta/archivo.py` | Lo saca del área de preparación sin borrar el cambio |
| Necesito cambiar de rama pero tengo cambios a medias | `git stash` ... `git stash pop` | Guarda los cambios en un cajón temporal y los recupera después |
| Hice commit en `main` por error (local, no subido) | `git switch -c feature/mi-rama` y luego en main `git reset --hard origin/main` | Primero salvas el commit en una rama nueva; luego regresas main a lo que hay en el remoto |
| El mensaje del último commit tiene un error | `git commit --amend -m "mensaje nuevo"` | Solo si no lo has subido; si ya lo subiste, es historia reescrita (`--force-with-lease`) |
| Perdí commits después de un rebase que salió mal | `git reflog` | Muestra dónde estuvo `HEAD`; `git reset --hard HEAD@{n}` te devuelve ahí. Git casi nunca borra nada de verdad |
| Quiero abandonar un rebase a medias | `git rebase --abort` | Vuelve exactamente al estado anterior |

## 3.12 Buenas prácticas de colaboración con Git

- **Una rama, un propósito.** Si mientras haces tu etapa encuentras un error en el README, no lo arregles en tu rama: abre otra (`docs/corregir-readme`) o un Issue.
- **Rebase antes de pedir revisión, no después.** Que el revisor vea tu código sobre el `main` actual.
- **Nunca subas secretos ni datos reales.** Contraseñas, tokens, archivos de microdatos con identificación. En Git, lo que se sube queda en la historia aunque lo borres después.
- `.gitignore`** es parte del proyecto.** Si generas un tipo de archivo nuevo que no debe subirse, agrégalo ahí y mándalo en un PR.
- **Mensajes para el que lee, no para el que escribe.** "arreglos" no dice nada; "fix(etapa-5): evitar división por cero en dominios sin ocupados" lo dice todo.
- **Lee el diff de tu propio PR antes de pedir revisión.** Vas a encontrar `print` olvidados, comentarios obsoletos y archivos que no debían ir. Es la revisión más barata que existe.

## 3.13 Troubleshooting del Módulo 3

| Síntoma | Causa probable | Solución |
|----|----|----|
| `! [remote rejected] main -> main (protected branch hook declined)` | Intentaste `push` directo a `main` | Es la protección funcionando. Crea una rama, mueve ahí tu commit (3.11) y abre un PR |
| `! [rejected] ... (non-fast-forward)` al hacer push de tu rama | Hiciste rebase y el remoto tiene la historia vieja | `git push --force-with-lease` (solo en tu rama) |
| `error: cannot rebase: You have unstaged changes` | Tienes cambios sin commit | Haz commit, o `git stash` antes y `git stash pop` después |
| El PR dice "This branch has conflicts that must be resolved" | `main` cambió las mismas líneas que tú | Rebase local (3.8), resuelve, push forzado. Evita el editor de conflictos de la web para archivos de código |
| CI falla con `ModuleNotFoundError` de un paquete que tú sí tienes | Instalaste algo con `pip` y no está en `requirements.txt` | Agrégalo a `requirements.txt` en un commit `chore(deps): ...` y avisa en el PR |
| CI falla con `FileNotFoundError` y en tu máquina funciona | Ruta absoluta o dependencia de un archivo que solo tú tienes | Rutas relativas a `Path(__file__)`; el único dato que puedes asumir es el fixture de entrada |
| Aparece `Merge branch 'main' into feature/...` en tu historia | Hiciste `git pull` estando en tu rama (que hace merge) | No es grave. Para la próxima: `git fetch` + `git rebase origin/main`. Puedes configurar `git config --global pull.rebase true` |
| Después de resolver conflictos, `git rebase --continue` dice `No changes` | Al resolver, dejaste el archivo idéntico a `main`; tu commit quedó vacío | `git rebase --skip` para saltar ese commit (su contenido ya estaba en main) |

## Cierre del Módulo 3

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Tu PR fue aprobado por un compañero, tiene el check de CI en verde, está rebaseado sobre `main`, y el facilitador lo mezcló. Además revisaste el PR de otra persona con al menos un comentario sustantivo. Y `git log --oneline` en `main` muestra tu commit con su mensaje bien formado.
