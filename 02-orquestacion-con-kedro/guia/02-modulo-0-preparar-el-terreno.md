# Módulo 0 — Preparar el terreno

Objetivo: tener un entorno virtual nuevo con Kedro y Kedro-Viz instalados, la carpeta del taller a la mano y la encuesta sintética ubicada. Unos 30 minutos.

### Lo que necesitas antes de empezar

- Python 3.11 o superior y VSCode instalados (Módulo 0 del Taller 1). Verifica con `python --version`.
- Git instalado y configurado con tu nombre y correo (Módulo 3 del Taller 1).
- El material de este taller descomprimido en una carpeta de tu computador. Dentro vas a encontrar `guia/`, `material/datos/` y `material/encuesta-hogares/`.

## 0.1 Una carpeta para los talleres y una para el proyecto

Vamos a separar dos cosas que es fácil confundir. Por un lado está el **material del taller**, que es de solo lectura: la guía, la encuesta y el proyecto de referencia. Por otro lado está **tu proyecto**, el que vas a construir paso a paso, que vive en una carpeta aparte y con su propio repositorio.

Crea una carpeta para tus proyectos si no la tienes, tal como hiciste en el Taller 1:

```powershell
cd C:\Users\tu-usuario\Documentos\proyectos
```

Todavía no crees la carpeta del proyecto Kedro: eso lo hace Kedro por ti en el Módulo 1.

> [!TIP]
> **💡 Tip**
>
> Evita rutas con espacios o tildes para la carpeta de proyectos. Funcionan, pero cada tanto algún comando se tropieza con ellas y pierdes veinte minutos buscando un error que no es tuyo.

## 0.2 Un entorno virtual nuevo para este taller

En el Taller 1 aprendiste que cada proyecto lleva su propio entorno virtual, de manera que las versiones de sus paquetes no interfieran con las de otros. Kedro trae bastantes dependencias, así que esta regla aplica con más razón.

Crea el entorno en la carpeta de proyectos y actívalo:

```powershell
python -m venv .venv-kedro
.venv-kedro\Scripts\activate
```

En macOS o Linux la activación es `source .venv-kedro/bin/activate`.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> La terminal muestra `(.venv-kedro)` al inicio de la línea. Si PowerShell dice que la ejecución de scripts está deshabilitada, aplica la solución del Troubleshooting del Módulo 1 del Taller 1: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, una sola vez.

> [!NOTE]
> **📘 Concepto**
>
> ¿Por qué el entorno queda en la carpeta de proyectos y no dentro del proyecto Kedro? Porque el proyecto todavía no existe, y porque Kedro genera su propio `.gitignore` que ya sabe ignorar `.venv`. Si prefieres moverlo adentro después, puedes. Lo que importa es que haya uno y que esté activo cada vez que trabajes.

## 0.3 Instalar Kedro y sus acompañantes

Con el entorno activo, instala Kedro, Kedro-Viz, los conectores de datos que vamos a usar y las librerías de siempre:

```powershell
pip install "kedro~=1.7.0" kedro-viz "kedro-datasets[pandas-csvdataset,pandas-parquetdataset,pandas-exceldataset,json-jsondataset]" pandas openpyxl pyarrow pytest
```

Va a tardar unos minutos. Mientras tanto, lee el siguiente concepto.

> [!NOTE]
> **📘 Concepto**
>
> Kedro se divide en tres paquetes que conviene distinguir desde ahora. `kedro` es el núcleo: la estructura de proyecto, el catálogo, los nodos y los pipelines. `kedro-datasets` son los conectores: la pieza que sabe leer un CSV, un Parquet o un Excel con pandas, de modo que tus funciones nunca tengan que abrir archivos. `kedro-viz` es la herramienta visual que dibuja tus pipelines en el navegador. Lo que va entre corchetes al instalar `kedro-datasets` son los conectores que elegimos; hay decenas más, desde SQL hasta Spark.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `kedro --version` responde `kedro, version 1.7.x`. Si ves un número 0.19, instalaste una versión anterior: repite el `pip install` con las comillas tal como están escritas arriba.

> [!TIP]
> **💡 Tip**
>
> Kedro envía estadísticas de uso anónimas y te lo va a preguntar la primera vez. Para que no insista, define la variable de entorno `KEDRO_DISABLE_TELEMETRY=1` o responde que no cuando pregunte. No cambia nada del taller.

## 0.4 Verificar que todo funciona

Tres comprobaciones rápidas, en el mismo orden:

```powershell
kedro info
python -c "import kedro_datasets, pandas; print('listo')"
kedro viz --help
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> El primer comando dibuja el logo de Kedro y lista los plugins instalados, entre ellos `kedro_viz`. El segundo imprime `listo`. El tercero muestra los subcomandos `build`, `deploy` y `run`.

## 0.5 Ubicar la encuesta

La encuesta sintética está en `material/datos/encuesta_hogares.csv`. Ábrela con VSCode o con Excel y mírala con ojo de analista antes de seguir, porque la vas a procesar durante todo el taller.

| Columna | Qué contiene |
|----|----|
| `id_persona` | Identificador único. Hay 15 filas duplicadas a propósito |
| `id_hogar` | Hogar al que pertenece la persona |
| `departamento` | Antioquia, Bogota, Narino, Santander o Valle |
| `area` | Urbana o Rural |
| `sexo` | H o M |
| `edad` | De 0 a 89 años |
| `ocupado` | 1 si está ocupado, 0 si no, vacío para menores de 15 |
| `ingreso` | Ingreso mensual en pesos. Vacío para no ocupados y para un 4 % de ocupados; seis valores tienen un cero de más |
| `factor_expansion` | Factor crudo, sin calibrar a totales poblacionales |

Si quieres regenerarla o entender de dónde sale cada problema, el script `material/datos/generar_encuesta.py` la produce con una semilla fija: la tuya y la de tus compañeros son idénticas.

> [!NOTE]
> **📘 Concepto**
>
> Los problemas de esta encuesta no son casuales. Cada uno justifica un paso del proceso: los duplicados justifican la limpieza, los ingresos faltantes la imputación, los atípicos el recorte y los factores crudos la calibración. Cuando en el Módulo 2 escribas cada nodo, vas a saber exactamente qué problema está resolviendo.

## 0.6 Glosario rápido: de SAS, R y Excel al vocabulario de Kedro

| Lo que ya conoces | En Kedro se llama | Qué es |
|----|----|----|
| Un `DATA` step o una función que transforma un data frame | Nodo | Una función de Python con entradas y salidas con nombre |
| Un programa `.sas` o un script `.R` que encadena pasos | Pipeline | Un conjunto de nodos que Kedro ordena según sus dependencias |
| `libname`, `read.csv("ruta")`, abrir un archivo | Catálogo de datos | Un archivo YAML donde cada dataset tiene nombre, tipo y ruta |
| Macrovariables, `%let`, constantes al inicio del script | Parámetros | Un YAML con valores que los nodos reciben como argumentos |
| Carpetas `raw`, `clean`, `final` | Capas de datos | Carpetas numeradas en `data/` que marcan la madurez del dato |
| Correr el programa completo | `kedro run` | Ejecuta el pipeline, leyendo y escribiendo según el catálogo |

## 0.7 Troubleshooting del Módulo 0

| Síntoma | Causa probable | Solución |
|----|----|----|
| `kedro` no se reconoce como comando | El entorno virtual no está activo | `.venv-kedro\Scripts\activate` y reintenta. Debe verse `(.venv-kedro)` |
| `pip install` falla en `pyarrow` | Versión de Python sin rueda precompilada | Verifica `python --version`; con 3.11 o 3.12 la instalación es directa |
| `kedro info` tarda muchísimo la primera vez | Kedro revisa plugins e inicializa configuración | Es normal una sola vez. La segunda corrida es inmediata |
| `kedro viz --help` dice que no existe el comando | `kedro-viz` no quedó instalado | `pip install kedro-viz` dentro del entorno activo |

## 0.8 Para profundizar (opcional)

- La documentación oficial de Kedro, en docs.kedro.org, tiene una sección "Get started" que vale la pena hojear después del Módulo 1, cuando ya tengas un proyecto en la mano.
- La lista completa de conectores de `kedro-datasets` está en el mismo sitio. Busca los que corresponden a las fuentes que usas en tu trabajo: SQL, SPSS, Stata, SAS.
