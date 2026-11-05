# Módulo 0 — Antes de empezar

Antes de escribir una línea de código, hay que preparar el computador. Este módulo cubre la instalación de Python y VSCode, y termina con una tabla de equivalencias SAS / R / Python para anclar lo que viene en los siguientes módulos.

Si tienes todo ya instalado, este módulo te toma unos 15 minutos solo verificando. Si partes de cero, calcula 30 a 45 minutos.

## 0.1 Requisitos de tu computador

| Componente | Mínimo recomendado |
|----|----|
| Sistema operativo | Windows 10 o 11 (esta guía asume Windows + PowerShell) |
| RAM | 8 GB |
| Espacio en disco | 5 GB libres |
| Permisos | Capacidad de instalar software (administrador) |
| Conexión a internet | Sí, para descargas e instalaciones |

> [!TIP]
> **💡 Tip**
>
> Si trabajas en macOS o Linux, los conceptos son los mismos. La diferencia es la terminal: en lugar de PowerShell usarás Terminal (macOS) o Bash (Linux), y los comandos de activación del entorno virtual cambian ligeramente. Estas diferencias se anotan donde aplican.

## 0.2 Instalar Python

Python se descarga desde el sitio oficial:

https://www.python.org/downloads/

### Paso a paso

1. Abre la página y descarga la versión estable más reciente para Windows (3.11 o superior).
1. Ejecuta el archivo .exe descargado.
1. En la primera pantalla del instalador, marca la casilla "Add python.exe to PATH" en la parte inferior.
1. Haz clic en "Install Now".
1. Cuando termine, haz clic en "Close".

> [!WARNING]
> **⚠️ Atención**
>
> Si NO marcas "Add python.exe to PATH" al instalar, los comandos python y pip no funcionarán desde PowerShell y tendrás que desinstalar y volver a instalar. Es el error más común. Verifica esa casilla antes de hacer clic en Install Now.

### Verificación

Abre PowerShell: presiona la tecla Windows, escribe "PowerShell" y abre la aplicación. Ejecuta:

```powershell
python --version
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver una línea similar a Python 3.11.7 (el número exacto puede variar). Si en su lugar ves un error del tipo "no se reconoce como comando", revisa la sección de Troubleshooting al final del módulo.

Verifica también que pip esté disponible:

```powershell
pip --version
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Debes ver una línea como pip 23.x.x from C:\Users\... seguida de la ruta donde quedó instalado.

## 0.3 Instalar Visual Studio Code

VSCode es el editor que vas a usar durante todo el taller. Es gratuito, liviano y se descarga desde:

https://code.visualstudio.com/

### Paso a paso

1. Descarga el instalador para Windows desde el botón principal de la página.
1. Ejecuta el .exe.
1. En la pantalla de "Tareas Adicionales", marca al menos estas tres opciones:
   - Agregar a PATH (recomendada por defecto)
   - Registrar Code como editor para tipos de archivo compatibles
   - Agregar la acción "Abrir con Code" al menú contextual del explorador
1. Finaliza la instalación y abre VSCode.

### Instalar las extensiones esenciales

Una vez VSCode esté abierto, instala estas tres extensiones. En la barra lateral izquierda, haz clic en el icono de extensiones (cuatro cuadrados):

| Extensión | Publicador | Para qué sirve |
|----|----|----|
| Python | Microsoft | Soporte general del lenguaje: ejecución, debugging, análisis |
| Pylance | Microsoft | Autocompletado y detección de errores en tiempo real |
| Jupyter | Microsoft | Abrir y ejecutar notebooks .ipynb dentro de VSCode |

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Después de instalar, todas deben aparecer en la sección "INSTALLED" del panel de extensiones, sin botón "Install" pendiente.

## 0.4 Verificar que todo funciona

Última verificación antes de cerrar este módulo. Abre la terminal integrada de VSCode:

- Atajo: Ctrl + ñ  (en algunos teclados Ctrl + `)
- O por menú: Ver → Terminal

En la terminal, ejecuta uno por uno:

```powershell
python --version
pip --version
code --version
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Las tres líneas deben mostrar números de versión, sin errores. Si las tres responden, terminaste el Módulo 0.

## 0.5 Glosario rápido SAS / R / Python

Esta tabla resume las equivalencias más comunes. No es necesario memorizarla: vas a verla aplicada en los siguientes módulos. Sirve como referencia cuando te preguntes "¿cómo se hacía esto en lo que ya conozco?".

| Acción | SAS | R | Python (pandas) |
|----|----|----|----|
| Cargar un CSV | `PROC IMPORT` | `read.csv("x.csv")` | `pd.read_csv("x.csv")` |
| Cargar un Excel | `PROC IMPORT DBMS=XLSX` | `readxl::read_excel()` | `pd.read_excel()` |
| Resumen estadístico | `PROC MEANS / PROC FREQ` | `summary(df)` | `df.describe()` |
| Primeras filas | `PROC PRINT (OBS=5)` | `head(df)` | `df.head()` |
| Filtrar filas | `WHERE edad > 18` | `filter(df, edad > 18)` | `df[df.edad > 18]` |
| Agrupar y resumir | `PROC MEANS CLASS=sexo` | `group_by() %>% summarise()` | `df.groupby('sexo').agg(...)` |
| Unir tablas | `PROC SQL  JOIN` | `left_join(a, b)` | `pd.merge(a, b)` |
| Crear variable nueva | `DATA step` | `mutate(x = ...)` | `df['x'] = ...` |
| Exportar resultados | `PROC EXPORT` | `write.csv()` | `df.to_csv()` |
| Entorno aislado | `(no aplica nativo)` | `renv` | `.venv  (estándar)` |
| IDE típico | `SAS Studio / EG` | `RStudio` | `VSCode / PyCharm` |
| Gestor de paquetes | `(incluidos en la instalación)` | `install.packages()` | `pip install` |
| Notebook | `(no nativo)` | `R Markdown / .Rmd` | `Jupyter / .ipynb` |
| Comentario | `* esto es comentario;` | `# esto es comentario` | `# esto es comentario` |

> [!TIP]
> **🔁 Si vienes de SAS o R**
>
> Si dominas SAS, piensa en Python como un lenguaje sin DATA steps explícitos: las tablas (DataFrames) son objetos de primera clase y las operaciones se encadenan. Si dominas R, Python con pandas es muy parecido a base R + dplyr en un solo paquete; la sintaxis con punto (df.head()) reemplaza al pipe %>% como mecanismo de encadenamiento.

## 0.6 Troubleshooting del Módulo 0

| Síntoma | Causa probable | Solución |
|----|----|----|
| 'python' no se reconoce como comando interno o externo | No marcaste "Add python.exe to PATH" en la instalación | Desinstala Python desde Configuración → Aplicaciones, descarga de nuevo el instalador y vuelve a instalar marcando la casilla |
| 'pip' no se reconoce como comando | PATH incompleto o instalación parcial | Reinstala Python marcando "Add python.exe to PATH" |
| Error de permisos al ejecutar el instalador | No tienes permisos de administrador | Clic derecho sobre el .exe → "Ejecutar como administrador" |
| VSCode no detecta Python en el selector de intérprete | Extensión Python no instalada o VSCode abierto antes de instalar Python | Instala la extensión Python de Microsoft y reinicia VSCode |
| pip install falla con error SSL o de red | Firewall corporativo o proxy bloqueando la conexión | Consulta con el área de TI sobre proxy interno o certificado de la entidad |
| Tengo dos versiones de Python instaladas y no sé cuál se ejecuta | Instalaciones anteriores que quedaron en PATH | En PowerShell ejecuta where.exe python  para ver todas las rutas; conserva solo la más reciente |

Cuando termines este módulo sin errores pendientes, sigue al Módulo 1.
