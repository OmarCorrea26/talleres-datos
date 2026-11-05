# Cierre del taller

Empezaste con una etapa que funcionaba y que nadie podía cambiar sin miedo. Terminas con la misma etapa partida en lo que cambia por razones distintas: unas reglas que se prueban con cinco filas, unas decisiones con nombre y validación, y cuatro adaptadores de pocas líneas que la sirven por archivos, por terminal, por HTTP y por Kedro. El probador del Taller 3 no notó la diferencia, y esa indiferencia es la prueba de que el contrato se respetó.

Lo que viene en el Taller 5 parte de aquí. Un paquete con dependencias declaradas, un adaptador HTTP que no sabe en qué máquina corre y un comando de terminal con entradas y salidas explícitas son exactamente lo que Docker necesita para empaquetar un proceso y correrlo igual en cualquier lugar. Si la limpieza siguiera siendo `app_acoplada.py`, el contenedor sería posible; con esta estructura, es casi trivial.

Antes de pasar al siguiente, una sola cosa: vuelve al script de tu trabajo que anotaste en el Issue y escríbele el ADR 0001. No lo refactorices. Solo deja escrito qué debería ser dominio y qué debería ser adaptador. Cuando llegue el pedido que te obligue a tocarlo, ya vas a saber por dónde empezar.
