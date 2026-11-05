# Introducción

### ¿A quién va dirigido este taller?

A quienes completaron el Taller 1. Ya sabes crear un entorno virtual, escribir un script con funciones y pandas, subir tu trabajo a un repositorio en GitHub y pedirle código a un asistente de IA sin aceptarlo a ciegas. Este taller no repite nada de eso: lo da por hecho y construye encima.

Si llegas sin el Taller 1 puedes seguir igual, aunque te vas a detener más seguido en dudas de Python básico, de entornos virtuales o de Git que esta guía ya no explica.

### El problema que vamos a resolver

En el Taller 1 escribiste `analisis_v2.py`: un script con funciones que carga un CSV y calcula promedios. Funcionó, y por eso mismo creció. Imagina que seis meses después ese script ya valida columnas, elimina duplicados, imputa ingresos, calibra factores de expansión, estima indicadores y exporta a Excel. Doscientas líneas, cinco rutas de archivo escritas a mano, un orden de ejecución que solo tú recuerdas y un compañero que te pregunta "¿y esto cómo lo corro?".

Ese es el momento en el que un análisis deja de ser un script y pasa a ser un proceso. Un proceso necesita cosas que un script no ofrece por sí solo: saber de dónde entra cada dato y a dónde sale, poder correr una parte sin correr el resto, cambiar un umbral sin tocar código, y probar cada paso por separado. Kedro es un marco de trabajo en Python que resuelve exactamente eso. Te da una estructura de proyecto estándar en la que los datos se declaran en un catálogo, los pasos son funciones puras llamadas nodos, y los nodos se encadenan en pipelines que Kedro ordena y ejecuta por ti.

### Lo que vas a construir

Vas a tomar una encuesta de hogares sintética con 1.215 registros y problemas deliberados (duplicados, ingresos faltantes, valores atípicos y factores de expansión sin calibrar) y la vas a convertir en un proyecto Kedro con dos pipelines. El primero prepara la base: valida, limpia y calibra. El segundo estima: calcula tasas de ocupación e ingresos promedio ponderados, les agrega error estándar e intervalos de confianza, clasifica la calidad de cada estimación y publica un Excel con sus metadatos.

Es el mismo proceso que en el Taller 3 vas a partir en seis servicios, uno por persona. Por eso conviene que lo entiendas completo aquí, de punta a punta y en tu propia máquina.

| Módulo | Tema | Qué vas a construir | Duración estimada |
|----|----|----|----|
| 0 | Preparar el terreno | Entorno nuevo con Kedro y Kedro-Viz instalados y verificados | 30 min |
| 1 | Del script al proyecto | El proyecto creado, la encuesta registrada en el catálogo y cargada sin rutas en el código | 1.5 h |
| 2 | Pipelines | Los dos pipelines corriendo con `kedro run`, parametrizados, visibles en Kedro-Viz, con namespaces y un hook | 3 h |
| 3 | Calidad y entrega | Pruebas con pytest, el proyecto en tu repositorio de GitHub y empaquetado | 1.5 h |
| 4 | IA en el IDE | Un indicador nuevo agregado con apoyo de IA, revisado por ti, y el Issue de entrega | 1 h |

### ¿Cómo está organizada cada sección?

Igual que en el Taller 1. Cada módulo abre con lo que necesitas antes de empezar, avanza en secciones numeradas con pasos concretos y checkpoints verificables, incluye un ejercicio práctico y cierra con una tabla de troubleshooting y una sección opcional para profundizar.

Los bloques de código son para que los escribas tú. Sin embargo, no estás solo: la carpeta `material/encuesta-hogares` contiene el proyecto completo y verificado, de manera que siempre puedas comparar tu versión contra una que funciona.

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

Sigue los módulos en orden, porque cada uno asume que el anterior quedó funcionando. Cuando aparezca un checkpoint, detente y compara. Si algo no coincide, resuélvelo antes de seguir: en Kedro, un nombre de dataset mal escrito en el Módulo 1 se convierte en un error incomprensible en el Módulo 2.

Ten dos ventanas abiertas, VSCode con tu proyecto y esta guía al lado. De acuerdo con lo aprendido en el Taller 1, cuando uses un asistente de IA primero entiende, después aceptas. En el Módulo 4 vamos a trabajar justamente eso aplicado a Kedro.

> [!WARNING]
> **⚠️ Atención**
>
> Trabaja en tu computador personal, no en el equipo institucional. Vas a instalar paquetes y a levantar un servidor local para Kedro-Viz, y en un equipo corporativo eso suele estar restringido por políticas que no tienen nada que ver con el taller. Nada de lo que hacemos aquí toca datos reales: la encuesta es sintética y se genera con una semilla fija.
