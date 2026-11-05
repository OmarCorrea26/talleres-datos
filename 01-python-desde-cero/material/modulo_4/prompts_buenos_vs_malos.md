# Cómo pedirle código a una IA sin que te dé basura

Notas rápidas para el Módulo 4. No es un manual completo, son los aprendizajes prácticos de pedir código a asistentes de IA.

La diferencia entre un prompt útil y uno inútil casi nunca es la longitud. Es qué tan claro tienes lo que quieres, y cuánto contexto le diste a la IA para que apunte al lugar correcto.

## Una sola regla que importa

La IA propone, tú decides. Si te genera código que no entiendes, pídele que te lo explique antes de aceptarlo. Si después de la explicación sigues sin entender, no lo uses todavía — el atajo de copiar sin entender se devuelve en horas debugueando algo que no es tuyo. Ese es el costo oculto que casi nadie te cuenta.

## Cómo armar un prompt que sirva

Un prompt útil suele tener cuatro cosas: contexto (qué estás haciendo, qué archivo, qué dataset), objetivo (qué quieres lograr), restricciones (qué NO debe hacer, qué librerías usar), y formato esperado (función, snippet, explicación). No siempre necesitas las cuatro. Pero entre más críticas sean las dos primeras, mejor sale el resultado.

## Cuatro ejemplos comparados

### Agregar una función

Malo: `agregame una función para sacar la mediana`

Bueno:

```
Estoy trabajando en analisis_v2.py, un script que analiza un DataFrame
de pandas con columnas id, edad, sexo, ingreso, area. Ya tengo la función
promedio_por_grupo(df, variable, grupo). Quiero una análoga llamada
mediana_por_grupo(df, variable, grupo) con la misma firma. Mantén el
estilo del docstring que ya uso.
```

Por qué funciona: la IA sabe el archivo, sabe el patrón que ya existe, tiene la firma exacta y la instrucción de respetar el estilo. Sale algo utilizable al primer intento.

### Debugear un error

Malo: `no me funciona`

Bueno:

```
Al ejecutar `python analisis_v2.py` me sale:

  FileNotFoundError: [Errno 2] No such file or directory: 'datos_ejemplo.csv'

El archivo sí existe en la misma carpeta que el script (lo verifiqué con
ls). El comando lo corro desde la carpeta taller_python con el entorno
virtual activo ((.venv) sale en el prompt). ¿Qué puede estar pasando?
```

Por qué funciona: el error textual, lo que ya verificaste, el contexto del entorno. Le quitaste a la IA el trabajo de adivinar lo que tú ya sabes.

### Refactorizar código

Malo: `hazlo mejor`

Bueno:

```
Esta función de mi script funciona pero la siento larga:

[pegar la función completa]

¿Puedes proponer una versión más corta sin perder claridad? No quiero
agregar librerías nuevas, solo pandas que ya uso. Explícame qué cambió
y por qué.
```

Por qué funciona: el código exacto, qué significa "mejor" (más corta), la restricción (sin librerías nuevas) y la petición de explicación.

### Agregar manejo de errores

Bueno:

```
En mi función cargar_datos(ruta_csv) quiero manejo de errores robusto.
Cubre tres casos:

  1. El archivo no existe → mensaje claro y salida limpia
  2. El archivo existe pero no es CSV válido → mensaje y salida limpia
  3. El CSV existe pero le faltan las columnas esperadas (id, edad,
     sexo, ingreso, area) → mensaje listando las que faltan

Usa try/except y print, no logging. Devuelve la función completa.
```

## Antes de aceptar lo que te generó

Una lista corta que te puedes hacer mental cada vez:

¿Entiendes qué hace cada línea? Si responde no, pide explicación.

¿Las librerías importadas son las que ya usas? Si trae cosas nuevas, decide si las quieres.

¿Modifica funciones que ya tenías? Si sí, ¿la firma sigue siendo compatible con lo que las llama?

¿Los nombres de variables son consistentes con tu estilo? Si son raros, pídele que use tu convención.

¿Lo probaste al menos una vez con datos reales? Antes de hacer commit, pruébalo.

Si todo da check, pega y sigue. Si alguno da no, ahí está la conversación con la IA que falta.

## Cuándo no usar IA

Cuando no entiendes lo que produce, ya lo dije. Pero también: cuando la tarea va a producción sin revisión, cuando el dominio no lo dominas (los bugs sutiles en código de un dominio que no manejas son los peores), y cuando lo que vas a pegar en el prompt incluye datos personales identificables o credenciales. Las herramientas comerciales suelen tener acuerdos de no entrenar con tus datos, pero igual — no te confíes con cosas sensibles.
