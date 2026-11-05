# Talleres de desarrollo para analistas estadísticos

Una ruta de formación pensada para equipos que vienen de SAS, R o Excel y necesitan dar el salto a Python, a procesos reproducibles y a trabajo colaborativo en GitHub. Cada taller es autónomo, de modo que se puede enviar por separado, y sin embargo todos cuentan una misma historia: una encuesta de hogares sintética que empieza como un script suelto y termina como un proceso con pipelines, servicios y despliegue.

> **Ejercicios de formación.** Los datos son sintéticos y los proyectos son ficticios. Nada de lo que hay aquí corresponde a un producto ni a una operación estadística real.

## La ruta

| # | Taller | Qué deja instalado en la cabeza | Estado |
|---|--------|---------------------------------|--------|
| 1 | [Python desde cero](01-python-desde-cero/) | Entornos virtuales, scripts con funciones, Git básico y uso crítico de asistentes de IA | Listo |
| 2 | [Orquestación con Kedro](02-orquestacion-con-kedro/) | De scripts a pipelines reproducibles: catálogo de datos, nodos, parámetros y pruebas | Listo |
| 3 | [APIs y Git colaborativo](03-apis-y-git-colaborativo/) | Servicios HTTP con FastAPI, pruebas de contrato, ramas, Pull Requests, revisión y rebase | Listo |
| 4 | [Arquitectura de software](04-arquitectura/) | Separar responsabilidades, patrones de diseño y SOLID leídos en código real, diseño que resiste el cambio | Listo |
| 5 | [Docker y despliegue](05-docker/) | Imágenes, volúmenes y Compose: el servicio, el pipeline y el muñeco completo corriendo igual en cualquier máquina | Listo |

Los talleres se toman en orden. Cada uno asume lo que enseñó el anterior y no lo vuelve a explicar.

## Cómo está organizado cada taller

```
0N-nombre-del-taller/
  README.md        presentación corta y cómo arrancar
  taller.toml      título, subtítulo y nombre del archivo que se genera
  guia/            la guía completa en Markdown, un archivo por módulo
  guia/img/        imágenes que usa la guía
  material/        archivos de referencia por módulo (cuando aplica)
  facilitador/     soluciones y notas para quien dicta el taller (no se envía)
```

La fuente de verdad es el Markdown de `guia/`. El documento de Word y el zip que recibe cada participante se generan a partir de él, de manera que una corrección se hace una sola vez y en un solo lugar.

## Generar los entregables

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r herramientas/requirements.txt

python herramientas/empaquetar.py                              # todos los talleres
python herramientas/empaquetar.py 03-apis-y-git-colaborativo   # uno solo
python herramientas/empaquetar.py --con-facilitador 03-apis-y-git-colaborativo
```

Los resultados quedan en `dist/`: un `.docx` con tabla de contenido por taller y un `.zip` con el taller completo, listo para enviar. La carpeta `facilitador/` se excluye del zip salvo que se pida con `--con-facilitador`.

## Herramientas

| Script | Para qué sirve |
|--------|----------------|
| `herramientas/empaquetar.py` | Convierte `guia/*.md` a docx y arma el zip de cada taller |
| `herramientas/docx_a_markdown.py` | Migra una guía escrita en Word a Markdown. Se usó una vez para traer los talleres 1 y 3 y queda por si vuelve a hacer falta |
| `herramientas/sincronizar_copias.py` | Regenera las copias de los talleres 2, 3 y 4 que el Taller 5 empaqueta en contenedores. Se corre después de cambiar cualquiera de esos proyectos |

## Convenciones de escritura

Las guías usan los llamados de atención de GitHub, que se ven bien en el navegador y se traducen a cajas de color en el Word generado:

```markdown
> [!TIP]
> **💡 Tip**
>
> Atajo, recomendación o paralelo con lo que ya conoces.

> [!WARNING]
> **⚠️ Atención**
>
> Error común o algo que hay que leer con cuidado.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Estado esperado: si lo ves, vas bien.

> [!NOTE]
> **📘 Concepto**
>
> Explicación de fondo: qué es y por qué existe.
```

## Licencia

El material se publica bajo licencia MIT. Puedes usarlo, adaptarlo y compartirlo conservando el aviso de copyright.
