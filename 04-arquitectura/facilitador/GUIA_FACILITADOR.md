# Guía del facilitador — Taller 4 (solo para quien facilita)

Esta carpeta no va al zip que reciben los participantes: `herramientas/empaquetar.py` la excluye salvo que se pida `--con-facilitador`.

## Qué hay aquí

| Archivo | Ejercicio |
|----|----|
| `solucion_modulo_4_patrones.py` | 4.7, la estrategia de media recortada y el adaptador Excel registrado en la fábrica |
| `solucion_modulo_5_validacion.py` | 5.4, la etapa 1 refactorizada con la misma estructura, con pruebas |

Los ejercicios 2.8 (regla nueva) y 3.9 (adaptador Parquet) no tienen solución de referencia: el checkpoint de la guía y la sección 3.7 (el mapa de dependencias) bastan para verificarlos, y la gracia del 2.8 es justamente la conversación que provoca en la sección 3.5.

## Antes de dictar

1. Corre el proyecto de referencia siguiendo `material/README.md`, con el muñeco del Taller 3 levantado para la sección 3.8. Es la demostración más convincente del taller y conviene hacerla en vivo.
2. Verifica que los fixtures en `material/etapa-limpiar/tests/fixtures/` sean los mismos del Taller 3. Si el contrato del muñeco cambió, regénalos allá y cópialos.
3. Genera el zip con `python herramientas/empaquetar.py 04-arquitectura` desde la raíz del repositorio de talleres.

## Dónde se atascan

- **Módulo 1.** La tabla de razones para cambiar parece trivial y por eso la saltan. Insiste: es el único momento en que miden el costo del acoplamiento antes de pagarlo.
- **Módulo 2, `pip install -e`.** Quien no lo haga desde la raíz del proyecto o con el entorno equivocado va a pasar media hora con `ModuleNotFoundError`. Es el error número uno.
- **Módulo 2, la palabra `registros`.** Alguien va a devolver `{"registros": ..., "resumen": ...}` desde el dominio porque así era en el Taller 3. La caja de Atención de la sección 2.3 existe por eso; vale la pena leerla en voz alta.
- **Módulo 3, sección 3.5.** Quienes hicieron el ejercicio 2.8 ven fallar la prueba del fixture y creen que rompieron algo. No rompieron nada: es la conversación de contrato que el taller busca provocar. Déjalos discutir las tres salidas antes de dar la opinión.
- **Módulo 4.** Van a querer meter un `if metodo == ...` dentro de `imputar_ingresos` en vez de la estrategia. Funciona, y por eso hay que preguntarles qué pasa con el cuarto método. También conviene cortar temprano la discusión de "¿y por qué no un Singleton?": la sección 4.6 existe para eso.
- **Módulo 5.** El asistente de IA tiende a meter `import json` o `from pathlib import Path` en el dominio "por si acaso". La pregunta extra de la lista de verificación ("¿importa algo que no sea pandas o la biblioteca estándar?") no alcanza para eso, porque `json` es biblioteca estándar. La pregunta correcta es "¿lo usa para leer o escribir algo?".

## Rúbrica de revisión sugerida

| Criterio | Peso |
|----|----|
| `pytest` en verde y el probador del muñeco aceptando el adaptador HTTP | 30 % |
| `dominio/` sin importaciones de frameworks ni de archivos, verificado con la sección 3.7 | 30 % |
| ADR 0001 a 0004 con al menos una consecuencia negativa cada uno | 20 % |
| Strategy y Factory extendidos en el ejercicio 4.7 sin tocar `dominio/reglas.py` ni los adaptadores existentes | 10 % |
| La etapa 1 refactorizada con pruebas propias, y el código generado con IA revisado con la lista | 10 % |
