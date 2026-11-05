# Guía del facilitador — Taller 5 (solo para quien facilita)

Esta carpeta no va al zip que reciben los participantes: `herramientas/empaquetar.py` la excluye salvo que se pida `--con-facilitador`.

## Qué hay aquí

| Archivo | Ejercicio |
|----|----|
| `solucion_modulo_2_cli.md` | 2.9, la terminal del Taller 4 como imagen |
| `solucion_modulo_3_compose_kedro.md` | 3.8, el pipeline y Kedro-Viz en Compose |

El ejercicio 1.5 (otras versiones) y el 4.4 (Dockerfile con IA revisado) no tienen solución única; el checkpoint y la lista de la sección 4.3 bastan.

## Cómo está armado el material

Las carpetas `servicio-limpieza`, `pipeline-kedro`, `muneco` y `script-del-taller-2` son copias generadas de los talleres 4, 2, 3 y 2. No se editan a mano: se edita el taller de origen o la sobrecapa en `material/_docker/<nombre>/` y se corre `python herramientas/sincronizar_copias.py` desde la raíz del repositorio. El script borra y vuelve a crear cada copia, así que cualquier cambio hecho directamente en una copia se pierde.

El muñeco copiado trae las seis etapas implementadas, tomadas de las soluciones del facilitador del Taller 3. Quien llega al Taller 5 ya hizo el 3, de modo que no es una filtración; aun así, conviene saberlo.

Hay un cambio en el código del muñeco respecto al Taller 3 tal como se publicó: `ensamblador/verificar.py` y `ensamblador/encadenar.py` leen la URL de cada etapa de una variable de entorno `ETAPA_N_URL`, con `localhost` como valor por defecto. Está aplicado en `03-apis-y-git-colaborativo/` de este repositorio y es compatible hacia atrás. Si el repositorio público del muñeco se usa para el Taller 5, hay que llevarle ese cambio.

## Antes de dictar

1. Con Docker Desktop abierto, corre los tres bloques de `material/README.md`. El de Compose es la demostración más convincente y conviene hacerla en vivo: siete contenedores, seis partes verdes, y `docker compose ps` mostrando `etapa_2` sobre otra imagen.
2. Verifica que las imágenes base se descargan en la red donde vas a dictar. Sin acceso a Docker Hub no hay taller; si hay dudas, descarga `python:3.11-slim` de antemano en cada máquina.
3. Genera el zip con `python herramientas/empaquetar.py 05-docker` desde la raíz del repositorio. Es el zip más pesado de la ruta por las copias; es el precio de que sea autónomo.

## Dónde se atascan

- **Módulo 0.** La instalación de Docker Desktop. Virtualización desactivada en la BIOS, WSL sin instalar, el reinicio que se saltan. Pide que lleguen con Docker instalado y `hello-world` corriendo; de lo contrario la primera hora se va en eso.
- **Módulo 1.** `${PWD}` con comillas simples en PowerShell, o corrido desde la carpeta equivocada. El mensaje `invalid reference format` confunde porque no dice nada de rutas.
- **Módulo 2.** El `--host 0.0.0.0`. Lo omiten, `docker ps` dice `Up`, `/docs` no abre y culpan al puerto. Antes de buscar otra causa, revisar el `CMD`.
- **Módulo 3.** Todas las etapas `ausente` en `/estado`: casi siempre es que levantaron el muñeco con el código del Taller 3 sin el cambio de `ETAPA_N_URL`. La sección 3.4 lo explica; vale la pena mostrar el `diff` en vivo.
- **Módulo 4.** El flujo de GitHub falla en `imagen` por el `.dockerignore`: si excluyeron `pyproject.toml` por error, o si el `COPY` no coincide con la estructura del repositorio. El registro del paso de construcción lo dice con claridad.

## Rúbrica de revisión sugerida

| Criterio | Peso |
|----|----|
| Pull Request con los checks `pruebas` e `imagen` en verde | 30 % |
| Dockerfile del servicio con base fijada, usuario sin privilegios, `.dockerignore` y dependencias antes del código | 30 % |
| `docker compose up` del muñeco con las seis partes verdes y la etapa 2 sobre la imagen propia | 20 % |
| Ejercicios 2.9 y 3.8 con una decisión escrita (qué entra a la imagen y por qué) | 20 % |
