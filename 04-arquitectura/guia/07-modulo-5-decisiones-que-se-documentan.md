# Módulo 5 — Decisiones que se documentan

Objetivo: dejar por escrito las tres decisiones que tomaste sin darte cuenta, comprobar que la estructura del proyecto se explica sola, y refactorizar una segunda etapa con ayuda de IA aplicando los criterios del taller. Una hora.

### Lo que necesitas antes de empezar

- El proyecto del Módulo 4 con `20 passed` y, si lo hiciste, el ejercicio 4.7.
- El asistente de IA del Taller 1 funcionando en VSCode.

## 5.1 Por qué escribir las decisiones

En seis meses, alguien va a abrir `dominio/reglas.py`, va a ver que recibe un DataFrame de pandas y va a decir "esto no es un dominio puro, el dominio no debería depender de pandas". Y va a tener razón según el libro. Lo que no va a saber es que lo pensaste, que lo decidiste con un motivo y que el motivo sigue siendo válido. Si no está escrito, la discusión vuelve a empezar desde cero, y a veces se deshace algo que funcionaba.

Un registro de decisión de arquitectura, o ADR por su sigla en inglés, es un archivo de veinte líneas que responde tres preguntas: en qué contexto estábamos, qué decidimos, y qué ganamos y qué pagamos. No es documentación del código. Es la memoria de por qué el código es así.

## 5.2 Tres decisiones que ya tomaste

Crea la carpeta `docs/decisiones/` y, primero, una plantilla:

```markdown
# NNNN. Título en una frase, en presente

Fecha: AAAA-MM-DD
Estado: propuesta | aceptada | reemplazada por NNNN

## Contexto

Qué situación nos obliga a decidir. Dos o tres frases. Si hay una restricción externa (una norma, un sistema con el que hay que hablar, un plazo), va aquí.

## Decisión

Qué decidimos, dicho de forma que alguien pueda verificar si el código la cumple.

## Consecuencias

Qué ganamos y qué pagamos. Las dos cosas. Una decisión sin costo no necesita registro.
```

Ahora escribe tres registros. Te doy el título y el contexto de cada uno; la decisión y las consecuencias escríbelas tú, porque son tuyas. Cuando termines, compara con los que están en `material/etapa-limpiar/docs/decisiones/`.

**0001. El dominio no importa ningún framework ni toca archivos.** Contexto: la etapa nació dentro de un servicio FastAPI con las reglas mezcladas con el transporte; para probar una regla había que levantar un servidor.

**0002. El DataFrame de pandas es el modelo de datos del dominio.** Contexto: la literatura dice que el dominio no debe depender de bibliotecas externas, pero las reglas estadísticas se expresan sobre columnas completas y quien las revisa piensa en tablas, no en objetos.

**0003. Cada mecanismo de entrega es un adaptador aparte, sin lógica propia.** Contexto: la misma limpieza se necesita por HTTP, por Kedro y por terminal, y la tentación es mantener una versión principal y copiar código para las otras.

> [!TIP]
> **💡 Tip**
>
> La sección de consecuencias es la que distingue un ADR útil de uno decorativo. Si solo lista ventajas, no es una decisión sino propaganda. El 0002 es el mejor ejemplo: la decisión contradice el libro, y el registro lo dice con todas las letras y explica por qué aquí es correcto.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `docs/decisiones/` tiene la plantilla y tres archivos numerados. Cada uno cabe en una pantalla y tiene al menos una consecuencia negativa escrita.

## 5.3 Una estructura que grita de qué trata

Abre el explorador de VSCode con todo el proyecto colapsado salvo `src/limpieza/`. Léelo como si no supieras nada:

```text
limpieza/
  dominio/       politica.py  reglas.py  puertos.py
  aplicacion/    limpiar_encuesta.py
  adaptadores/   archivos.py  cli.py  contrato_json.py  http.py  kedro.py
```

Sin abrir un archivo sabes que el proyecto limpia algo, que hay una política y unas reglas, que existe un caso de uso llamado limpiar encuesta, y que se puede usar por archivos, terminal, HTTP y Kedro. Compara con lo que te dice una estructura como `utils/`, `helpers/`, `core/`, `services/`, `handlers/`: nombres de la tecnología, no del problema.

> [!NOTE]
> **📘 Concepto**
>
> A esto se le llama arquitectura que grita, por una idea de Robert Martin: los planos de un edificio te dicen si es una biblioteca o un hospital antes de leer una sola etiqueta, por la forma de los espacios. La estructura de un proyecto debería decirte de qué trata antes de leer código. Si lo primero que se ve es el framework, el framework se convirtió en el proyecto.

Haz la prueba con el proyecto Kedro del Taller 2: `pipelines/preparacion/` y `pipelines/estimacion/` gritan. `nodes.py` y `pipeline.py` adentro no, pero son convención del framework y están en el nivel que corresponde. Es un buen equilibrio.

## 5.4 Ejercicio práctico: la etapa 1 con ayuda de IA

Vas a refactorizar la etapa 1 del muñeco, la validación, con la misma estructura, usando el asistente para escribir el cuerpo de las funciones y tú para todo lo demás. La solución de referencia del facilitador reproduce los conteos del fixture `etapa_1_salida.json` del Taller 3.

1. Crea `src/limpieza/dominio/validacion.py`. Antes de pedir nada, decide tú la firma: `validar(encuesta: pd.DataFrame) -> ResultadoValidacion`, con un `ResumenValidacion` que tenga `n_filas`, `columnas` y `n_nulos_por_columna`, tal como el contrato del Taller 3.
2. Pide al asistente el cuerpo con un prompt que diga dónde va el archivo, qué recibe, qué devuelve, que solo puede importar pandas y dataclasses, y que debe fallar con `ValueError` si falta una columna. Pásalo por la lista de verificación del Módulo 4 del Taller 2, con una pregunta más: ¿importa algo que no sea pandas o la biblioteca estándar?
3. Escribe tú `adaptadores/kedro.py` con `nodo_validar` y agrega a `http.py` nada: la validación es otra etapa y tendría su propio servicio. Anota esa decisión en un ADR 0004 de cinco líneas.
4. Pruebas del dominio con cuatro filas, una de ellas sin una columna.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> `pytest` reporta al menos tres pruebas más en verde, `dominio/validacion.py` no importa nada fuera de pandas y la biblioteca estándar, y el ADR 0004 explica por qué validar y limpiar comparten paquete pero no servicio.

## 5.5 Cuándo esta arquitectura sobra

Sería deshonesto cerrar sin decirlo: no todo necesita dominio, puertos y adaptadores. Un script que corre una vez para responder una pregunta no los necesita. Un análisis exploratorio en un notebook tampoco. La estructura de este taller paga cuando se cumple al menos una de tres condiciones: el mismo proceso se usa desde más de un lugar, las reglas cambian con más frecuencia que el transporte, o más de una persona lo mantiene.

La pregunta que vale la pena hacerse no es "¿aplico arquitectura hexagonal?" sino "¿cuántas razones para cambiar tiene este archivo?". Si la respuesta es una, déjalo como está. Si son tres o cuatro, ya sabes qué hacer, y sabes que cuesta un día y ahorra meses.

### Reflexión final del taller

Vuelve a `app_acoplada.py` y a la tabla del Módulo 1. Responde las cinco filas otra vez, ahora con `etapa-limpiar`. Cada pedido toca un archivo, y nunca el mismo. Eso no lo logró ningún patrón sofisticado: lo logró separar lo que cambia por razones distintas.

## 5.6 Entregable: Issue de validación

Crea un repositorio `arquitectura-limpieza-<tu-nombre>` con tu proyecto, súbelo y abre un Issue con el título `Entrega Taller 4 — [tu nombre]`:

```markdown
## Entrega Taller 4

- Repositorio: <enlace>
- `pytest`: N pruebas en verde
- `dominio/` importa únicamente: (lista)
- ADR escritos: 0001 a 0004
- Patrones del Módulo 4 implementados: Strategy (media recortada) y Factory (Excel): sí / no

## El pedido del Módulo 1 que más me costó ubicar

(dos o tres líneas: cuál era y en qué capa terminó)

## Un script de mi trabajo que tiene más de una razón para cambiar

(dos o tres líneas, sin refactorizarlo todavía)
```

Asigna el Issue a quien facilita el taller.

## 5.7 Para profundizar (opcional)

- El sitio adr.github.io recopila plantillas y ejemplos de registros de decisión. La que usamos es la más corta que sirve.
- Si quieres ver la misma idea en R, busca cómo los paquetes bien hechos separan funciones puras en `R/` de la interfaz en `plumber.R` o en una aplicación Shiny. El Apéndice B del Taller 3 ya apuntaba en esa dirección.
