# Introducción

### ¿A quién va dirigido este taller?

A quienes completaron los talleres 1, 2 y 3. Ya escribiste nodos de Kedro, ya implementaste una etapa del muñeco como servicio con FastAPI y ya trabajaste con otros en el mismo repositorio. Este taller no agrega una herramienta nueva: agrega una forma de pensar el código que ya sabes escribir.

### El problema que vamos a resolver

Tu etapa del muñeco funciona. Cumple el contrato, pasa las pruebas, el torso sale verde. Ahora imagina tres pedidos que llegan en la misma semana. El equipo de Kedro quiere usar tu limpieza como un nodo del pipeline del Taller 2, sin levantar un servidor. Alguien de metodología pide cambiar el percentil de recorte y poder probar dos valores sin tocar código. Y se decide que el muñeco deja de hablar JSON y pasa a recibir Parquet.

Abre tu `app.py` y pregúntate cuántas de esas tres cosas puedes hacer sin reescribir la función `procesar`. Si la respuesta es "ninguna", no es porque esté mal escrita. Es porque en treinta líneas conviven cuatro cosas con razones distintas para cambiar: el transporte HTTP, la traducción de JSON a pandas, las reglas estadísticas y las decisiones metodológicas. Cuando cambia cualquiera, hay que tocar las otras tres.

Arquitectura de software es, en el fondo, decidir qué va con qué y qué depende de qué, de modo que cada cambio toque lo menos posible. Este taller te enseña una forma concreta de hacerlo, que se conoce como arquitectura hexagonal o de puertos y adaptadores, y que en los talleres 2 y 3 ya aplicaste sin nombrarla: los nodos de Kedro son funciones puras, el catálogo es un adaptador, el contrato del muñeco es un puerto.

### Lo que vas a construir

Vas a tomar la etapa 2 del muñeco, la limpieza, y la vas a reorganizar en tres capas: un **dominio** con las reglas estadísticas y nada más, una capa de **aplicación** que las orquesta, y **adaptadores** para cada forma de entrar y salir. Al final, la misma limpieza va a correr como servicio HTTP dentro del muñeco (y el probador del Taller 3 va a decir "cumple el contrato"), como nodo del pipeline del Taller 2 y como comando de terminal, sin una sola regla duplicada. Después vas a ponerle nombre a los patrones de diseño que ese código ya usa, vas a leer los principios SOLID señalándolos en tus propios archivos y vas a implementar dos patrones más, Strategy y Factory, porque dos pedidos reales los justifican. Y vas a dejar por escrito, en tres registros cortos, por qué decidiste lo que decidiste.

| Módulo | Tema | Qué vas a construir | Duración estimada |
|----|----|----|----|
| 0 | Preparar el terreno | Entorno listo y el material ubicado | 30 min |
| 1 | El problema del acoplamiento | Un diagnóstico de la etapa acoplada: qué cambia por qué razón | 1 h |
| 2 | El dominio en el centro | Las reglas de limpieza como paquete puro, con sus pruebas, sus puertos y su caso de uso | 2 h |
| 3 | Adaptadores | La misma limpieza por archivos, por terminal, por HTTP y como nodo de Kedro | 2 h |
| 4 | Los patrones que ya usaste | Los patrones de diseño y SOLID señalados en el código, más Strategy y Factory implementados con pruebas | 1.5 h |
| 5 | Decisiones que se documentan | Tres registros de decisión, una estructura que se explica sola y una segunda etapa refactorizada con IA | 1 h |

### ¿Cómo está organizada cada sección?

Igual que en los talleres anteriores. Cada módulo abre con lo que necesitas antes de empezar, avanza en secciones numeradas con checkpoints, incluye un ejercicio práctico y cierra con troubleshooting y una sección opcional para profundizar.

Los bloques de código son para que los escribas tú. Sin embargo, el proyecto terminado está en `material/etapa-limpiar`, de manera que siempre puedas comparar contra una versión que funciona y que pasa veinte pruebas.

### Convenciones tipográficas

| Elemento | Significado |
|----|----|
| `código en línea` | Nombres de archivos, comandos, rutas, variables o funciones |
| Bloque gris monospace | Comando para ejecutar en terminal, o código para escribir en un archivo |
| 📘 Concepto morado | Explicación de fondo: qué es y por qué existe |
| 💡 Tip azul | Atajo, recomendación o paralelo con lo que ya conoces |
| ⚠️ Atención amarillo | Error común o algo que debes leer con cuidado |
| ✅ Checkpoint verde | Estado esperado: si lo ves, vas bien |

### Cómo trabajar con la guía

Este taller tiene más texto y menos comandos que los anteriores, porque lo que enseña son criterios. Léelo con el código abierto al lado y, cada vez que la guía diga "esto es una regla" o "esto es transporte", detente a comprobarlo en el archivo. La habilidad que te llevas no es escribir adaptadores: es mirar una función y ver cuántas cosas distintas está haciendo.

> [!WARNING]
> **⚠️ Atención**
>
> Trabaja en tu computador personal, igual que en los talleres anteriores. Nada de lo que hacemos aquí toca datos reales: la encuesta es sintética y los fixtures son los mismos del Taller 3.
