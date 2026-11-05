# Taller 5. Docker: el mismo proceso, en cualquier máquina

> **Ejercicio de formación.** Los datos son sintéticos y los proyectos son ficticios. No corresponden a ningún producto ni operación estadística real.

Quinto y último taller de la ruta. Toma los proyectos de los talleres anteriores y los empaqueta en contenedores: el servicio de limpieza del Taller 4 como primera imagen, el pipeline Kedro del Taller 2 con los datos montados desde afuera, y el muñeco del Taller 3 completo con Docker Compose, con la etapa 2 servida por la imagen del Taller 4. Cierra con integración continua que construye y arranca la imagen en cada Pull Request y con la lista de verificación para revisar Dockerfiles escritos por IA.

## Qué vas a aprender

| Módulo | Tema | Resultado al finalizar |
|--------|------|------------------------|
| 0 | Preparar el terreno | Docker Desktop instalado y un contenedor corriendo |
| 1 | En mi máquina funciona | El script del Taller 2 corriendo dentro de un contenedor ajeno, sin instalar nada en tu máquina |
| 2 | La primera imagen | El servicio de limpieza empaquetado, con usuario sin privilegios, verificación de salud y tamaño medido |
| 3 | Datos afuera, servicios juntos | El pipeline Kedro con volúmenes y el muñeco completo con Docker Compose |
| 4 | Confiar en la imagen | Integración continua que construye y prueba la imagen, Dockerfiles con IA revisados, y el Issue de entrega |

## Qué hay en esta carpeta

- `guia/` es la guía completa, un archivo por módulo. Se lee en orden.
- `material/script-del-taller-2/` tiene el monolito del Taller 2 y la encuesta, para el Módulo 1.
- `material/servicio-limpieza/`, `material/pipeline-kedro/` y `material/muneco/` son copias de los proyectos de los talleres 4, 2 y 3 con sus Dockerfiles, `.dockerignore` y, en el caso del muñeco, su `compose.yaml` y las seis etapas implementadas. Cada una tiene un `ORIGEN.md`.
- `material/_docker/` contiene solo los archivos propios de Docker que se aplican encima de cada copia. Es lo que se edita; las copias se regeneran con `python herramientas/sincronizar_copias.py` desde la raíz del repositorio.
- `facilitador/` tiene las soluciones de los ejercicios y notas para quien dicta el taller. No se envía a los participantes.

## Requisitos previos

Haber completado los talleres 1 a 4. Un computador personal con Windows 10 u 11 de 64 bits (o macOS, o Linux), 8 GB de memoria y permisos de administrador para instalar Docker Desktop.

## Cómo usarlo

Empieza por `guia/01-introduccion.md`. Los Dockerfiles se escriben sobre tus propios proyectos de los talleres anteriores; las copias del material están para comparar y para que el taller funcione aunque no los tengas a la mano.

Si recibiste el taller como zip, adentro viene también la guía en formato Word con el mismo contenido.

## Versiones

El material se construyó y verificó con Docker Desktop 29 (Docker Compose v5) en Windows 11 con WSL 2, imágenes base `python:3.11-slim`, Kedro 1.7 y FastAPI 0.1xx.
