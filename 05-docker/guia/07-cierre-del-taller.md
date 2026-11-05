# Cierre del taller

Empezaste con un proceso que funcionaba en tu máquina. Terminas con tres imágenes que corren igual en cualquiera: un servicio con usuario propio y verificación de salud, un pipeline que recibe los datos de afuera y los devuelve procesados, y un muñeco entero que se levanta con un comando y se verifica solo en cada Pull Request. La etapa 2 de ese muñeco vino de otro repositorio y de otra imagen, y el contrato la unió al resto sin que nadie tocara nada.

Con esto cierra la ruta de cinco talleres. Si volvieras al script del Taller 1 hoy, sabrías qué es un nodo, qué es un parámetro, qué es un adaptador y qué es un volumen. Ninguna de esas palabras es un fin: cada una es una separación que hace que lo siguiente sea posible.

Una última sugerencia, la misma de siempre pero ahora completa. Elige el proceso de tu trabajo que más te duela, el que solo corre en tu máquina. No lo migres entero. Escríbele un Dockerfile de diez líneas, construye la imagen y pásasela a un compañero. Si corre, ya sabes todo lo que necesitas saber. Si no corre, el error te va a decir exactamente qué dependencia invisible tenías, y esa es la primera cosa que vale la pena arreglar.
