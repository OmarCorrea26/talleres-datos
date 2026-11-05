# Guía del facilitador — Taller 2 (solo para quien facilita)

Esta carpeta no va al zip que reciben los participantes: `herramientas/empaquetar.py` la excluye salvo que se pida `--con-facilitador`. Contiene las soluciones de los tres ejercicios con solución única y notas para dictar el taller.

## Qué hay aquí

| Archivo | Ejercicio |
|----|----|
| `solucion_modulo_2_contar_hogares.py` | 2.12, un nodo más en la preparación |
| `solucion_modulo_3_test_contar_hogares.py` | 3.8, la prueba de ese nodo |
| `solucion_modulo_4_ingreso_mediano.py` | 4.4, el ingreso mediano ponderado con IA |

Los ejercicios 1.9 (registrar y guardar un dataset) y los de "para profundizar" no tienen solución de referencia porque el checkpoint de la guía basta para verificarlos.

## Antes de dictar

1. Corre el proyecto de referencia en una máquina limpia siguiendo `material/README.md`. Si Kedro publicó una versión nueva y algo cambió de nombre, el material fija `kedro~=1.7.0` y conviene mantenerlo así hasta revisar la guía.
2. Verifica que la encuesta en `material/datos/` sea la misma del Taller 3 (`03-apis-y-git-colaborativo/datos/encuesta_hogares.csv`). Los valores de los checkpoints del Módulo 2 dependen de ella.
3. Genera el zip con `python herramientas/empaquetar.py 02-orquestacion-con-kedro` desde la raíz del repositorio de talleres.

## Dónde se atascan

- **Módulo 1, indentación del YAML.** Es el error más frecuente y el mensaje de Kedro no ayuda. Pídeles que te muestren el catálogo antes de buscar otra causa.
- **Módulo 2, `conf/local` sobreescribe por bloque.** Alguien va a crear un `parameters_preparacion.yml` local con una sola línea y va a recibir `KeyError: 'grupos_imputacion'`. Está en el troubleshooting, pero vale la pena anticiparlo en voz alta.
- **Módulo 2, sección 2.9.** El registro manual de pipelines confunde a quienes ya se habían acostumbrado a `find_pipelines()`. La explicación que mejor funciona: "la variante rural no tiene carpeta, así que nadie la puede descubrir; hay que presentarla".
- **Módulo 3, `.load()` en la prueba de pipeline.** Lo olvidan casi todos la primera vez. Dejar que les falle y lean el mensaje enseña más que advertirlo.
- **Módulo 4.** El asistente propone `median()` sin ponderar en la mayoría de los casos. Es el momento para insistir en que la estadística la decide la persona.

## Rúbrica de revisión sugerida

| Criterio | Peso |
|----|----|
| `kedro run` completa las ocho tareas y `pytest` está en verde | 40 % |
| Parámetros en YAML y ninguna ruta ni número suelto en los nodos | 20 % |
| Pruebas propias para los nodos nuevos, con datos mínimos armados a mano | 20 % |
| README que permite a otra persona instalar, correr y probar sin preguntar | 20 % |
