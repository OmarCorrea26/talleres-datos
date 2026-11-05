# Módulo 4 — IA en el IDE

Los asistentes de IA dentro del editor cambiaron la forma de escribir código en los últimos dos años. La ventaja real es bastante concreta: te ahorran tiempo escribiendo código repetitivo y te enseñan al sugerirte patrones que no conocías. La trampa es igual de concreta: si copias sin entender, terminas con código que parece funcionar pero tiene bugs sutiles que aparecen meses después. Este módulo es para que aproveches la ventaja sin caer en la trampa.

Una regla que vale la pena tener en mente todo el módulo: la IA propone, tú decides. Nunca pegues código que no entiendes — el atajo de copiar sin entender se paga después en horas debugueando algo de cuya lógica no eres dueño. Por eso este módulo va al final del taller y no al principio: necesitas los Módulos 1, 2 y 3 dominados para poder evaluar lo que la IA produce.

Al final vas a haber escogido un asistente, instalado en VSCode, y extendido tu analisis_v2.py con apoyo de IA. Calcula una hora y media.

## 4.1 Panorama de opciones

No hay UNA herramienta correcta. Depende de tu presupuesto, preferencia de UI, y qué tan profundo quieras integrarte. Esta tabla resume las principales opciones en el momento de escribir esta guía. Investiga las versiones actuales antes de decidir.

| Herramienta | Costo | Fortaleza |
|----|----|----|
| GitHub Copilot | USD 10/mes (gratis para estudiantes y educadores) | Autocompletado fluido, el más integrado a VSCode |
| Cursor | Gratis con límites; Pro USD 20/mes | IDE separado basado en VSCode; chat con contexto del proyecto |
| Cline | Gratis (extensión); pagas la API que uses (Anthropic, OpenAI) | Más agéntico: ejecuta tareas largas, edita varios archivos |
| Continue | Gratis (extensión); pagas la API o usa modelos locales | Configurable, soporta modelos locales con Ollama |
| Codeium / Windsurf | Capa gratuita generosa | Autocompletado tipo Copilot sin costo de entrada |
| Claude Code | Suscripción Claude (USD 20/mes) | Asistente en terminal, agéntico, fuerte en refactorings grandes |

> [!TIP]
> **💡 Tip**
>
> Si vas a probar uno por primera vez sin gastar, empieza con Codeium o Continue. Si tu organización tiene presupuesto y quieres la mejor experiencia integrada, GitHub Copilot. Si quieres flujos más agénticos, Cursor o Cline. Cualquiera te sirve para este módulo.

## 4.2 Instalar tu asistente (ejemplo con Continue)

Las instrucciones específicas varían por herramienta, pero el patrón es similar. Como ejemplo, instalamos Continue (gratis):

1. En VSCode, panel de extensiones (Ctrl + Shift + X).
1. Busca "Continue" y haz clic en Install.
1. Aparecerá un nuevo ícono de Continue en la barra lateral izquierda.
1. Sigue el setup wizard. Te va a pedir una API key (Anthropic, OpenAI, o modelos locales).

Para Copilot, Cursor o cualquier otro, el flujo es análogo: instalar extensión, autenticarse, listo.

## 4.3 Cómo escribir buenos prompts

La diferencia entre un prompt bueno y uno malo no es la longitud, es la especificidad y el contexto. Un buen prompt tiene cuatro partes:

| Parte | Qué incluye |
|----|----|
| Contexto | Qué estás haciendo, qué archivo, qué dataset |
| Objetivo | Qué quieres lograr concretamente |
| Restricciones | Qué NO debe hacer, qué librerías usar |
| Formato | Código completo, snippet, explicación |

### Ejemplo — agregar una función

**❌ Prompt malo:**

```text
agregame una función para sacar la mediana
```

**✅ Prompt bueno:**

```text
Estoy trabajando en analisis_v2.py, un script que analiza un DataFrame con columnas id, edad, sexo, ingreso, area. Ya tengo la función promedio_por_grupo(df, variable, grupo). Quiero agregar una función análoga llamada mediana_por_grupo(df, variable, grupo) con la misma firma. Mantén el mismo estilo de docstring que la función existente.
```

Por qué funciona el segundo: contexto del archivo, especifica el patrón existente, da la firma exacta, pide respeto al estilo. La IA tiene material suficiente para devolver algo útil al primer intento.

En el material complementario del Módulo 4 está prompts_buenos_vs_malos.md con más ejemplos, incluyendo cómo debugear errores, cómo refactorizar y cómo agregar manejo de errores.

## 4.4 Checklist antes de aceptar código generado

Antes de pegar lo que te dio la IA en tu archivo, pregúntate cinco cosas: ¿entiendo qué hace cada línea?; ¿las librerías importadas son las que ya uso o agrega nuevas que no tengo instaladas?; ¿cambia el comportamiento de funciones existentes sin avisarme?; ¿los nombres de variables son consistentes con mi estilo?; y ¿lo probé al menos una vez con datos reales?

Si alguna respuesta es "no", vuelve a preguntarle a la IA. No aceptes ciegamente. La velocidad inicial que te da copiar sin entender se devuelve después en horas debugueando algo que no comprendes.

## 4.5 Ejercicio práctico — Extender el script con IA

En el material complementario tienes ejercicio_ia.py. Es el punto de partida del ejercicio. Cópialo a tu carpeta taller_python y trabájalo con tu asistente de IA preferido.

### Las cuatro tareas, en orden de dificultad

1. FÁCIL — Agrega una función percentil_por_grupo(df, variable, grupo, p) que devuelva el percentil p (entre 0 y 100) de la variable agrupada.
1. MEDIA — Agrega validación al inicio de main(): si datos_ejemplo.csv no existe, imprime un mensaje claro pidiendo correr generar_datos.py y termina limpiamente sin traceback.
1. MEDIA — Agrega logging básico a las funciones existentes: cada función imprime un mensaje cuando empieza y cuando termina, con timestamp.
1. DIFÍCIL — Refactoriza main() para que reciba la ruta del CSV como argumento de línea de comandos. Si se llama sin argumentos, usa "datos_ejemplo.csv" por defecto.

### Cómo trabajar el ejercicio

- Trabájalo en tu repo de GitHub. Cada tarea = un commit. Así puedes ver cuánto fue IA y cuánto fuiste tú.
- Para cada tarea: escribe un prompt claro, lee la propuesta de la IA con calma, decide si la aceptas o pides ajustes.
- Después de aplicar cambios, ejecuta el script y verifica que sigue funcionando.
- Si la IA propone algo que no entiendes, pídele que te explique antes de aceptar.

## 4.6 Cuándo NO usar IA

Hay contextos donde el riesgo de usar IA supera el beneficio. Cuando no entiendes lo que la IA produce, no es un atajo — es deuda técnica con intereses. Cuando la tarea es crítica y no va a haber revisión humana (autenticación, cifrado, manejo de datos sensibles, lógica de negocio importante), tampoco. Si estás escribiendo código en un dominio donde no tienes base, los errores sutiles que pueda meter la IA son difíciles de detectar para alguien no experto en ese dominio. Y nunca metas información sensible en los prompts: datos personales identificables, credenciales, secretos, contraseñas.

### Reflexión final del taller

Al terminar el ejercicio del Módulo 4, dedica 10 minutos a responder estas preguntas (escríbelas como comentarios en tu repo o en un Issue):

1. ¿Cuál tarea te resultó más difícil de pedirle a la IA? ¿Qué terminó haciendo IA y qué terminaste haciendo tú?
1. ¿Cuántas veces la IA propuso algo incorrecto o subóptimo y tuviste que pedirle ajustes?
1. ¿En qué parte sentiste que la IA te ahorró más tiempo? ¿En qué parte te lo hizo perder?
1. Si vuelves a hacer este ejercicio mañana, ¿qué harías diferente en cómo pides ayuda?

## 4.7 Para profundizar (opcional)

Recursos para seguir aprendiendo sobre IA en desarrollo:

- Documentación de GitHub Copilot: https://docs.github.com/copilot
- Documentación de Cursor: https://docs.cursor.com
- Documentación de Continue: https://docs.continue.dev
- Buenas prácticas de prompting (Anthropic): https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
