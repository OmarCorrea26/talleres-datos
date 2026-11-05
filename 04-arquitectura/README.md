# Taller 4. Arquitectura de software para procesos estadísticos

> **Ejercicio de formación.** Los datos son sintéticos y el proyecto es ficticio. No corresponde a ningún producto ni operación estadística real.

Cuarto taller de la ruta. Toma la etapa 2 del muñeco del Taller 3, la limpieza de la encuesta, y la reorganiza en dominio, aplicación y adaptadores, de modo que las mismas reglas sirvan por HTTP dentro del muñeco, como nodo del pipeline del Taller 2 y como comando de terminal, sin una regla duplicada. Pone nombre a los patrones de diseño que ese código ya usa, lee SOLID en los archivos del proyecto e implementa Strategy y Factory frente a dos pedidos reales. Cierra con registros de decisión de arquitectura y con una segunda etapa refactorizada con ayuda de IA.

## Qué vas a aprender

| Módulo | Tema | Resultado al finalizar |
|--------|------|------------------------|
| 0 | Preparar el terreno | Entorno listo y el material ubicado |
| 1 | El problema del acoplamiento | Un diagnóstico de la etapa acoplada: qué cambia por qué razón |
| 2 | El dominio en el centro | Las reglas de limpieza como paquete puro, con sus pruebas, sus puertos y su caso de uso |
| 3 | Adaptadores | La misma limpieza por archivos, por terminal, por HTTP y como nodo de Kedro |
| 4 | Los patrones que ya usaste | Los patrones de diseño y SOLID señalados en el código, más Strategy y Factory implementados con pruebas |
| 5 | Decisiones que se documentan | Tres registros de decisión, una estructura que se explica sola y una segunda etapa refactorizada con IA |

## Qué hay en esta carpeta

- `guia/` es la guía completa, un archivo por módulo. Se lee en orden.
- `material/modulo_1/app_acoplada.py` es el "antes": la etapa 2 del muñeco con todo en un archivo. Funciona y cumple el contrato.
- `material/etapa-limpiar/` es el "después": el proyecto terminado con veinte pruebas y tres registros de decisión. Sirve para comparar, no para copiar.
- `facilitador/` tiene las soluciones de los ejercicios de los módulos 4 y 5 y notas para quien dicta el taller. No se envía a los participantes.

## Requisitos previos

Haber completado los talleres 1, 2 y 3. En particular, haber implementado una etapa del muñeco con FastAPI y haber escrito nodos de Kedro: este taller reorganiza ese código, no lo enseña de nuevo.

## Cómo usarlo

Empieza por `guia/01-introduccion.md`. Tu propio proyecto va en una carpeta aparte, con su propio repositorio, tal como se explica en el Módulo 2.

Si recibiste el taller como zip, adentro viene también la guía en formato Word con el mismo contenido.

## Versiones

El material se construyó y verificó con Python 3.11, pandas 2, FastAPI 0.1xx y pytest 8. El adaptador para Kedro no requiere tener Kedro instalado.
