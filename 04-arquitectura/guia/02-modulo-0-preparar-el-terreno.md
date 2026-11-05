# Módulo 0 — Preparar el terreno

Objetivo: un entorno virtual con lo necesario, el material ubicado y, si lo tienes, el repositorio del muñeco a la mano para la verificación final. Unos 30 minutos.

### Lo que necesitas antes de empezar

- Python 3.11 o superior, VSCode y Git, configurados como en el Taller 1.
- El material de este taller descomprimido. Adentro vas a encontrar `guia/`, `material/modulo_1/app_acoplada.py` y `material/etapa-limpiar/`.
- Opcional, para la sección 3.8: tu clon del repositorio del muñeco del Taller 3.

## 0.1 Un entorno para este taller

En tu carpeta de proyectos, crea y activa un entorno nuevo:

```powershell
cd C:\Users\tu-usuario\Documentos\proyectos
python -m venv .venv-arquitectura
.venv-arquitectura\Scripts\activate
pip install pandas fastapi uvicorn httpx pytest
```

Son las mismas librerías del Taller 3 más `pytest`. No vas a instalar Kedro: en la sección 3.6 vas a ver que el adaptador para Kedro no lo necesita, y esa es parte de la lección.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `python -c "import pandas, fastapi, httpx, pytest; print('listo')"` imprime `listo` con el entorno activo.

## 0.2 El material

Mira la carpeta `material/` antes de empezar. Hay dos cosas y conviene distinguirlas desde ya.

`modulo_1/app_acoplada.py` es el punto de partida: la etapa 2 del muñeco con todo en un archivo. Es muy parecida a la que entregaste en el Taller 3, y a propósito.

`etapa-limpiar/` es el punto de llegada: el mismo proceso reorganizado en dominio, aplicación y adaptadores, con catorce pruebas y tres registros de decisión. No lo abras todavía con detalle. Vas a construirlo tú en los módulos 2 y 3, y la gracia está en descubrir por qué cada archivo existe. Cuando algo no te funcione, ahí está para comparar.

## 0.3 Las cuatro palabras del taller

Vas a leerlas decenas de veces, así que conviene fijarlas ahora con la definición que usa esta guía.

| Palabra | Qué significa aquí | En el Taller 2 y 3 ya lo viste como |
|----|----|----|
| Dominio | Las reglas del proceso estadístico, escritas sin saber de archivos, HTTP ni frameworks | Los nodos de Kedro, que reciben y devuelven DataFrames |
| Puerto | Lo que el dominio necesita del exterior, declarado como una interfaz en su propio idioma | El contrato del muñeco: qué entra y qué sale de cada etapa |
| Adaptador | Una pieza que traduce entre el mundo exterior y un puerto, sin reglas propias | El catálogo de Kedro, que convierte "dame `encuesta_cruda`" en leer un CSV |
| Caso de uso | La secuencia que orquesta el dominio a través de los puertos para resolver un pedido completo | El `pipeline.py`, que dice qué nodo alimenta a cuál |

> [!NOTE]
> **📘 Concepto**
>
> La regla que ata las cuatro palabras es una sola y se llama regla de la dependencia: las dependencias apuntan hacia adentro. Los adaptadores conocen al dominio; el dominio no conoce a ningún adaptador. Si alguna vez un archivo de `dominio/` importa `fastapi`, se rompió la regla, y todo lo que este taller promete deja de ser cierto.

## 0.4 Troubleshooting del Módulo 0

| Síntoma | Causa probable | Solución |
|----|----|----|
| `pip install` de `fastapi` falla con un error de compilación | Versión de Python muy vieja o muy nueva | Verifica `python --version`; con 3.11 o 3.12 todo son ruedas precompiladas |
| `uvicorn` no se reconoce como comando | El entorno no está activo | `.venv-arquitectura\Scripts\activate` y reintenta |
