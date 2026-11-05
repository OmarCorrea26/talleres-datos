# 0003. Cada mecanismo de entrega es un adaptador aparte, sin lógica propia

Fecha: 2026-11-05
Estado: aceptada

## Contexto

La misma limpieza se necesita en tres contextos: como servicio HTTP dentro del muñeco del Taller 3, como nodo del pipeline Kedro del Taller 2, y como comando de terminal para corridas puntuales. La tentación es tener una versión principal y "adaptar" las otras copiando código.

## Decisión

Cada mecanismo tiene su archivo en `limpieza/adaptadores/` y hace exactamente dos cosas: traducir lo que recibe al idioma del dominio, y traducir lo que el dominio devuelve al idioma de quien llamó. Un adaptador no contiene reglas, no contiene constantes metodológicas y no conoce a los demás adaptadores. La traducción del contrato JSON del Taller 3 se comparte en `contrato_json.py` porque más de un adaptador podría necesitarla.

## Consecuencias

Ganamos que un cambio en una regla se haga una vez y aparezca en los tres contextos, y que agregar un cuarto (una tarea programada, una función en la nube) sea un archivo nuevo sin tocar nada existente. Pagamos que los adaptadores parecen "demasiado simples" y alguien va a sentir la tentación de meterles lógica. La prueba `tests/adaptadores/test_http.py` contra los fixtures del Taller 3 es el guardián: si un adaptador deja de ser una traducción fiel, falla.
