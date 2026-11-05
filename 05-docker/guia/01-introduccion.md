# Introducción

### ¿A quién va dirigido este taller?

A quienes completaron los cuatro talleres anteriores. Tienes un pipeline Kedro que corre con un comando, un servicio HTTP que cumple un contrato, un muñeco que se arma con seis servicios y un paquete con el dominio separado de sus adaptadores. Todo eso funciona en tu computador. Este taller se ocupa de la frase que sigue: "en mi máquina funciona".

### El problema que vamos a resolver

Un compañero clona tu repositorio, crea el entorno, instala las dependencias y algo falla. Tiene otra versión de Python, o de pandas, o le falta una librería del sistema que tú instalaste hace un año y olvidaste. Pierden una tarde los dos. Después, el proceso tiene que correr en un servidor que administra otra área, con reglas sobre qué se puede instalar. Pierden una semana.

El problema no es tu código: es que tu código depende de un entorno completo (intérprete, paquetes, archivos de configuración, variables) que vive en tu máquina y en ningún otro lugar. Docker resuelve eso empaquetando el código junto con su entorno en una imagen, un archivo que se construye una vez y corre igual en cualquier computador que tenga Docker. No "parecido": igual, byte por byte.

Lo que en el Taller 1 hiciste con un entorno virtual, aislar las dependencias de Python, Docker lo hace con todo lo demás, incluido el sistema operativo. Y tal como aprendiste en el Taller 4, un servicio que no sabe en qué máquina corre y un pipeline que declara sus entradas y salidas son exactamente lo que un contenedor necesita. Esa separación la hiciste allá; aquí la cobras.

### Lo que vas a construir

Tres imágenes, de menor a mayor. Primero, la del servicio de limpieza del Taller 4: un Dockerfile de veinte líneas, construido, corriendo en un puerto y validado por el probador del muñeco sin que este note que ahora es un contenedor. Segundo, la del pipeline Kedro del Taller 2, con los datos fuera de la imagen, montados al correr. Tercero, el muñeco completo: una imagen, siete servicios, y un solo comando que levanta todo y lo deja verde en el navegador. La etapa 2 de ese muñeco va a ser el contenedor del Taller 4, para que veas dos imágenes de dos repositorios distintos hablando entre sí.

Cierra con integración continua que construye y arranca la imagen en cada Pull Request, y con la lista de verificación para revisar Dockerfiles escritos por un asistente de IA.

| Módulo | Tema | Qué vas a construir | Duración estimada |
|----|----|----|----|
| 0 | Preparar el terreno | Docker Desktop instalado y un contenedor corriendo | 45 min |
| 1 | En mi máquina funciona | El script del Taller 2 corriendo dentro de un contenedor ajeno, sin instalar nada en tu máquina | 1 h |
| 2 | La primera imagen | El servicio de limpieza empaquetado, con usuario sin privilegios, verificación de salud y tamaño medido | 2 h |
| 3 | Datos afuera, servicios juntos | El pipeline Kedro con volúmenes y el muñeco completo con Docker Compose | 2 h |
| 4 | Confiar en la imagen | Integración continua que construye y prueba la imagen, Dockerfiles con IA revisados, y el Issue de entrega | 1 h |

### ¿Cómo está organizada cada sección?

Igual que en los talleres anteriores. Cada módulo abre con lo que necesitas, avanza en secciones numeradas con checkpoints, incluye un ejercicio práctico y cierra con troubleshooting y lecturas opcionales.

El material incluye copias de los proyectos de los talleres 2, 3 y 4 con sus Dockerfiles ya escritos, en `material/`. Sirven para comparar; la guía está hecha para que los escribas tú.

### Convenciones tipográficas

| Elemento | Significado |
|----|----|
| `código en línea` | Nombres de archivos, comandos, rutas, variables o funciones |
| Bloque gris monospace | Comando para ejecutar en terminal, o contenido para escribir en un archivo |
| 📘 Concepto morado | Explicación de fondo: qué es y por qué existe |
| 💡 Tip azul | Atajo, recomendación o paralelo con lo que ya conoces |
| ⚠️ Atención amarillo | Error común o algo que debes leer con cuidado |
| ✅ Checkpoint verde | Estado esperado: si lo ves, vas bien |

### Cómo trabajar con la guía

Los comandos de esta guía están escritos para PowerShell en Windows, que es donde Docker Desktop presenta más sorpresas. Donde macOS o Linux difieren, se anota. Mantén una terminal abierta para los comandos de Docker y otra para los comandos de los proyectos, porque varias veces vas a necesitar un contenedor corriendo mientras lo pruebas desde afuera.

> [!WARNING]
> **⚠️ Atención**
>
> Más que en cualquier taller anterior: trabaja en tu computador personal. Docker Desktop necesita permisos de administrador para instalarse, activa la virtualización del sistema y abre puertos locales. En un equipo institucional eso suele estar bloqueado por política, y la instalación puede quedar a medias de una forma difícil de deshacer. Nada de lo que hacemos toca datos reales: la encuesta es sintética.
