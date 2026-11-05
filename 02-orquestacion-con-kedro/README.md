# Taller 2. De scripts sueltos a pipelines reproducibles con Kedro

> **Ejercicio de formación.** Los datos son sintéticos y el proyecto es ficticio. No corresponde a ningún producto ni operación estadística real.

Segundo taller de la ruta. Toma la encuesta de hogares sintética que acompaña a estos talleres y la convierte, paso a paso, en un proyecto Kedro con dos pipelines: uno que prepara la base (valida, limpia, calibra) y otro que estima (indicadores ponderados, precisión, clasificación de calidad y publicación). Es el mismo proceso que el Taller 3 reparte después entre seis servicios.

## Qué vas a aprender

| Módulo | Tema | Resultado al finalizar |
|--------|------|------------------------|
| 0 | Preparar el terreno | Entorno nuevo con Kedro y Kedro-Viz instalados y verificados |
| 1 | Del script al proyecto | El proyecto creado, la encuesta registrada en el catálogo y cargada sin rutas en el código |
| 2 | Pipelines | Los dos pipelines corriendo con `kedro run`, parametrizados, visibles en Kedro-Viz, con namespaces y un hook |
| 3 | Calidad y entrega | Pruebas con pytest, el proyecto en tu repositorio de GitHub y empaquetado |
| 4 | IA en el IDE | Un indicador nuevo agregado con apoyo de IA, revisado por ti, y el Issue de entrega |

## Qué hay en esta carpeta

- `guia/` es la guía completa, un archivo por módulo. Se lee en orden.
- `material/datos/` contiene la encuesta sintética (`encuesta_hogares.csv`) y el script que la genera con semilla fija.
- `material/modulo_1/proceso_monolito.py` es el "antes": todo el proceso en un script de corrido, con el que arranca el Módulo 1.
- `material/encuesta-hogares/` es el proyecto Kedro completo y verificado, para comparar cuando algo no funcione. No incluye la solución del ejercicio del Módulo 4.
- `facilitador/` tiene las soluciones de los ejercicios y notas para quien dicta el taller. No se envía a los participantes.

## Requisitos previos

Haber completado el Taller 1: Python con funciones y pandas básico, entornos virtuales, Git y GitHub, y un asistente de IA instalado en VSCode. La guía no vuelve a explicar esos fundamentos.

## Cómo usarlo

Empieza por `guia/01-introduccion.md`. Tu propio proyecto Kedro va en una carpeta aparte, con su propio repositorio, tal como se explica en el Módulo 1. El material de esta carpeta es de solo lectura.

Si recibiste el taller como zip, adentro viene también la guía en formato Word con el mismo contenido.

## Versiones

El material se construyó y verificó con Python 3.11, Kedro 1.7, kedro-datasets 10 y kedro-viz 12.5. Con versiones 0.19 de Kedro algunos comandos cambian de nombre.
