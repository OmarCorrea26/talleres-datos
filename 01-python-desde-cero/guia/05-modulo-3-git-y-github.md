# Módulo 3 — Git y GitHub

Hasta ahora tu código vive solo en tu computador. Si pierdes el equipo, pierdes el trabajo. Si quieres mostrarle algo a alguien, le mandas un .zip por correo (y a la semana ya nadie sabe cuál era la versión buena). Eso lo resuelve Git, y la copia en la nube la resuelve GitHub. Este módulo cubre los dos.

Al final vas a tener tu código publicado en un repositorio público de GitHub bajo la convención taller-python-tu-nombre, con un .gitignore correcto, un README.md, y un Issue de entrega mencionando a quien va a revisar (@OmarCorrea26).

Calcula unas dos horas.

### Lo que necesitas antes de empezar

La carpeta taller_python con los archivos del Módulo 2 funcionando. Conexión a internet. Y si todavía no tienes cuenta de GitHub, un correo electrónico para crearla.

## 3.1 ¿Qué problema resuelve Git?

Te suena familiar: termina el día con un archivo análisis.py. Mañana lo modificas pero te da miedo perder lo que ya funcionaba, así que guardas una copia llamada análisis_v2.py. Pasan días y la carpeta termina con análisis_v2_FINAL.py, análisis_v2_FINAL_corregido.py, análisis_v2_DEFINITIVO_este_sí.py. Eventualmente nadie sabe cuál era la versión que servía. Si has trabajado con archivos compartidos en una entidad, esto no es exageración.

Git resuelve exactamente eso. Es un sistema que guarda el historial completo de cambios de tus archivos manteniendo siempre un solo archivo "vigente", pero con todas las versiones anteriores accesibles. Puedes volver a cualquier estado anterior, comparar versiones lado a lado y colaborar con otros sin pisarte el trabajo.

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> En SAS no hay un equivalente nativo: cada quien gestiona versiones a mano. En R, RStudio tiene integración con Git (Tools → Project Options → Git), que internamente usa el mismo Git que vamos a instalar aquí. Si en algún momento usaste esa integración en RStudio, sabes más Git de lo que crees.

## 3.2 Git vs GitHub — la distinción clave

Es la confusión más frecuente para principiantes:

| Git | GitHub |
|----|----|
| Software de control de versiones que se instala en tu computador | Sitio web donde se alojan repositorios Git en la nube |
| Funciona 100% offline una vez instalado | Requiere internet |
| Gratis y open source desde 2005 | Servicio comercial de Microsoft (capa gratuita generosa) |
| No necesita cuenta | Requiere cuenta personal |
| Puedes usarlo solo, sin GitHub | No tiene sentido sin Git |

Otras alternativas a GitHub: GitLab, Bitbucket, Codeberg. Todas usan Git por debajo. En este taller usamos GitHub porque es el estándar de facto en la industria.

## 3.3 Instalar Git en Windows

1. Ve a https://git-scm.com/download/win y descarga el instalador.
1. Ejecuta el .exe.
1. Acepta los valores por defecto de cada pantalla del wizard. Los defaults son razonables para principiantes.
1. Cuando termine, abre PowerShell (o reinicia VSCode si lo tenías abierto) y ejecuta:

```powershell
git --version
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver una línea como git version 2.43.0.windows.1 (el número exacto puede variar). Si dice "comando no reconocido", reinicia el computador para refrescar el PATH y reintenta.

## 3.4 Configurar tu identidad

Git asocia cada cambio (commit) a una persona usando un nombre y un correo. Configúralos UNA sola vez:

```powershell
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu_correo@ejemplo.com"
```

> [!WARNING]
> **⚠️ Atención**
>
> Usa exactamente el MISMO correo que vas a usar (o usas) en GitHub. Si los correos no coinciden, tus commits no se atribuirán correctamente a tu cuenta de GitHub y aparecerán como "unknown".

Para verificar la configuración:

```powershell
git config --global user.name
git config --global user.email
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Cada comando debe devolver lo que pusiste, sin errores.

## 3.5 Crear tu cuenta de GitHub

Si ya tienes cuenta, salta a la sección 3.6.

1. Ve a https://github.com y haz clic en "Sign up".
1. Ingresa el correo (el MISMO que configuraste en Git).
1. Crea una contraseña fuerte.
1. Escoge un username — piénsalo bien, es público y va en la URL de todos tus repos (github.com/tu-username).
1. Verifica el correo cuando GitHub te envíe el código.

> [!TIP]
> **💡 Tip**
>
> Recomendación de username: usa algo profesional, fácil de recordar y consistente con tus otros perfiles (LinkedIn, etc.). Ejemplos buenos: jperez, juan-perez, jperez-datos. Evita números aleatorios al final tipo jperez1234 si puedes.

## 3.6 Conceptos clave de Git

Antes de usar Git, conviene tener claras estas ocho palabras. No las memorices: vuelve a esta tabla cuando aparezcan en los siguientes pasos.

| Término | Definición simple |
|----|----|
| `repository (repo)` | Una carpeta versionada por Git. Tiene una subcarpeta .git oculta con el historial completo. |
| `working directory` | Los archivos como los ves en tu computador. Lo que editas en VSCode. |
| `staging area` | Una "zona de espera" donde marcas qué archivos quieres incluir en el próximo commit. |
| `commit` | Un snapshot etiquetado de los archivos en staging. Tiene un mensaje describiendo el cambio. |
| `branch` | Una rama de desarrollo. Por defecto se llama main. |
| `remote` | Un repo gemelo alojado en otro lugar (típicamente GitHub). Se llama origin por convención. |
| `push` | Subir tus commits locales al remote (GitHub). |
| `pull` | Bajar commits del remote a tu repo local. |
| `.gitignore` | Archivo de texto que lista qué archivos Git debe ignorar (no versionar). |

Flujo básico que vas a repetir muchas veces:

```text
# 1. Modificas archivos en VSCode
# 2. Ves que cambio:
git status

# 3. Marcas que cambios quieres en el commit:
git add nombre_de_archivo.py
# o agregar todo lo modificado:
git add .

# 4. Creas el commit con un mensaje:
git commit -m "Descripcion breve del cambio"

# 5. Subes a GitHub:
git push
```

## 3.7 Inicializar tu repositorio local

Abre la terminal en VSCode con tu carpeta taller_python abierta. Asegúrate del directorio:

```text
pwd
```

Inicializa el repo:

```powershell
git init
```

Esto crea una subcarpeta oculta .git dentro de tu proyecto que va a almacenar el historial. No la edites manualmente.

Verifica el estado:

```powershell
git status
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver una lista de "Untracked files" con todos tus .py, el .venv y los archivos generados. Eso significa que Git los ve pero todavía no los está versionando.

## 3.8 Crear tu .gitignore

Antes de hacer el primer commit, hay que decirle a Git qué NO debe versionar:

- La carpeta .venv (pesa mucho y cada quien la regenera)
- Los cachés de Python (__pycache__, *.pyc)
- Los archivos generados localmente (datos_ejemplo.csv, resumen.xlsx)
- Configuración local del editor (.vscode/)

En el material complementario del Módulo 3 está el archivo gitignore_template.txt. En VSCode:

1. Crea un archivo nuevo en la raíz de taller_python.
1. Nómbralo exactamente .gitignore (con el punto al inicio, sin extensión).
1. Copia y pega el contenido de gitignore_template.txt.
1. Guarda.

Ahora ejecuta de nuevo:

```powershell
git status
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> La lista de "Untracked files" ahora es mucho más corta: no debe aparecer la carpeta .venv ni los archivos generados. Solo deben aparecer tus .py, el .gitignore y los archivos fuente.

## 3.9 Tu primer commit

Agrega todos los archivos relevantes al staging area:

```powershell
git add .
```

El punto significa "todo lo que ve git status". Verifica:

```powershell
git status
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Los archivos ahora aparecen bajo "Changes to be committed" (en verde). Eso significa que están listos para el commit.

Crea el commit:

```powershell
git commit -m "Primer commit: estructura inicial del taller"
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver una salida como: [main (root-commit) a3b8c12] Primer commit: estructura inicial del taller   N files changed, X insertions(+) Eso significa que el snapshot quedó guardado en tu repo local.

> [!TIP]
> **💡 Tip**
>
> Buenas prácticas de mensajes de commit: cortos (idealmente 50 caracteres), en presente, describiendo QUÉ cambió, no CÓMO. Buen ejemplo: "Agrega función mediana_por_grupo". Mal ejemplo: "asd asd cambios".

## 3.10 Crear el repositorio en GitHub

1. Ve a https://github.com e inicia sesión.
1. Arriba a la derecha, haz clic en el botón "+" → "New repository".
1. Nombre del repo: taller-python-tu-nombre (en minúsculas, con guiones, sin tildes ni ñ).
1. Visibilidad: marca PUBLIC.
1. Importante: NO marques "Add a README", "Add .gitignore" ni "Choose a license". Vas a subir tu repo local tal cual.
1. Clic en "Create repository".

> [!IMPORTANT]
> **✅ Checkpoint**
>
> GitHub te muestra una página con instrucciones bajo el título "…or push an existing repository from the command line". Esos son los comandos que vamos a usar.

## 3.11 Conectar local con remoto

En la página del repo en GitHub vas a ver tres comandos. Cópialos uno por uno a tu terminal (con (.venv) activo o sin él — Git funciona igual). Reemplaza tu-usuario y tu-nombre:

```powershell
git remote add origin https://github.com/tu-usuario/taller-python-tu-nombre.git
git branch -M main
git push -u origin main
```

Línea por línea:

- git remote add origin ... — registra GitHub como la copia remota llamada origin
- git branch -M main — renombra la rama principal a main (estándar moderno)
- git push -u origin main — sube tu commit al remoto y establece el seguimiento

> [!WARNING]
> **⚠️ Atención**
>
> El último comando te va a pedir autenticación. GitHub ya no acepta contraseñas para esto desde 2021. Necesitas un Personal Access Token (PAT). Si te lo pide y no sabes qué poner, ve a la sección de Troubleshooting al final del módulo.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Si la autenticación funciona, verás líneas como "Writing objects: 100%" y al final "main → main". Recarga la página del repo en GitHub: tus archivos deben aparecer ahí.

## 3.12 El ciclo del día a día — segundo commit

Ya tienes tu primer commit publicado. El flujo se repite así para cada cambio:

1. Modifica un archivo (por ejemplo, edita analisis_v2.py para agregar un comentario nuevo).
1. Guarda con Ctrl + S.
1. Ve el cambio: git status
1. Agrega al staging: git add analisis_v2.py
1. Crea el commit: git commit -m "Agrega comentario explicativo en analisis_v2"
1. Sube a GitHub: git push

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Después de push, recarga el repo en GitHub. Debes ver dos commits en el historial y el cambio reflejado en el archivo.

## 3.13 Atajo: Source Control de VSCode

Todo lo anterior se puede hacer con la UI de VSCode sin usar la terminal:

1. Atajo Ctrl + Shift + G abre el panel de Source Control.
1. Ahí ves los archivos modificados. Pasa el mouse sobre cada uno y haz clic en "+" para agregarlo al staging.
1. Escribe el mensaje del commit en el campo de arriba.
1. Haz clic en "Commit" (el check).
1. Para hacer push, haz clic en el ícono de sincronización abajo o en "..." → "Push".

¿Terminal o UI? Mi recomendación: aprende el flujo en terminal primero, ahí entiendes qué pasa por dentro. Una vez lo dominas, usa la UI de VSCode en el día a día — es más cómoda. Para operaciones avanzadas (resolver conflictos de merge, rebase, manejo de stash) eventualmente vas a necesitar la terminal de todas formas, pero para el ciclo básico add → commit → push, la UI es suficiente y se siente menos intimidante.

## 3.14 Agregar tu README.md

El README.md es el archivo de presentación de tu repo. Es lo primero que se ve cuando alguien lo abre en GitHub. Está escrito en Markdown.

En el material del Módulo 3 está README_template.md. Cópialo a la raíz de tu taller_python, renómbralo a README.md (sin el _template) y personalízalo: reemplaza [Tu Nombre] por tu nombre real.

Cuando guardes, haz el ciclo de commit:

```powershell
git add README.md
git commit -m "Agrega README con descripcion del proyecto"
git push
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Recarga tu repo en GitHub. Ahora debe mostrar tu README formateado abajo de la lista de archivos.

## 3.15 Entregable — Issue de validación

Este es el paso final del Módulo 3 y la forma oficial de "entregar" tu avance para revisión.

1. Ve a la página de tu repo en GitHub.
1. Haz clic en la pestaña "Issues" en la barra superior.
1. Haz clic en "New issue".
1. Como título usa: "Entrega Módulo 3 — Taller de Python"
1. En el cuerpo, copia el texto sugerido del archivo issue_entrega_template.txt (en el material del Módulo 3) y completa tus datos.
1. Verifica que @OmarCorrea26 aparece resaltado en azul (eso confirma que la mención funcionó).
1. Haz clic en "Submit new issue".

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Al crear el Issue, GitHub notifica automáticamente al revisor. La entrega quedó registrada.

La revisión se hace dentro del mismo Issue. Las entregas se revisan antes del inicio del siguiente sprint del taller — no esperes respuesta el mismo día, planifícate con esa cadencia en mente.

Si dejo observaciones, las verás como comentarios en tu Issue. Aplica los ajustes en tu código, haz commit y push, y comenta de vuelta en el Issue algo como "Listo, ajustes aplicados". Cuando el Issue se cierra, la entrega está aceptada.

## 3.16 Troubleshooting del Módulo 3

| Síntoma | Causa probable | Solución |
|----|----|----|
| git --version dice "comando no reconocido" | Git no quedó en el PATH | Cierra y vuelve a abrir VSCode y la terminal. Si persiste, reinicia el computador. |
| git push pide username y password pero no acepta tu contraseña | GitHub ya no acepta contraseñas para push (desde 2021) | Genera un Personal Access Token (PAT): GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic). Marca el scope "repo". Usa el token generado como password. |
| fatal: not a git repository | Ejecutaste un comando de Git en una carpeta que no es repo | Asegúrate de estar en taller_python (pwd) y de haber ejecutado git init antes |
| Estoy subiendo accidentalmente la carpeta .venv (pesa mucho) | El .gitignore no se creó antes del primer commit | Elimina el seguimiento con: git rm -r --cached .venv  Luego commit y push |
| git push falla con "updates were rejected" | Hay commits en GitHub que no tienes localmente (común si creaste el repo con README inicial) | Ejecuta git pull origin main --rebase y luego git push de nuevo |
| Modifiqué un archivo pero git status dice "nothing to commit" | Olvidaste guardar el archivo (Ctrl + S) en VSCode | Guarda el archivo y vuelve a ejecutar git status |
| Mi nombre no aparece en el commit de GitHub | El correo de git config --global user.email no coincide con el de tu cuenta de GitHub | Ajusta el correo con: git config --global user.email "correo_de_github" |

## 3.17 Para profundizar (opcional)

- Comando útil: git log --oneline para ver el historial compacto
- Comando útil: git diff para ver qué cambió desde el último commit
- Branches: aprende a crear ramas con git checkout -b nueva-rama para probar cambios sin afectar main
- Pull requests: cuando trabajes en equipo, los cambios se proponen vía PRs en lugar de empujar directo a main

Recursos para profundizar:

- Tutorial interactivo gratuito: https://learngitbranching.js.org/
- Cheat sheet oficial de Git: https://education.github.com/git-cheat-sheet-education.pdf
- Documentación de GitHub: https://docs.github.com/es
- Libro Pro Git (gratis, en español): https://git-scm.com/book/es/v2
