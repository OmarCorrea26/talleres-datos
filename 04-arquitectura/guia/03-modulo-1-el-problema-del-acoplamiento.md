# Módulo 1 — El problema del acoplamiento

Objetivo: correr la etapa acoplada, comprobar que funciona, y hacerle un diagnóstico preciso: qué responsabilidades conviven en ella y qué pasa cuando cada una cambia. Una hora.

### Lo que necesitas antes de empezar

- El entorno `.venv-arquitectura` activo.
- `material/modulo_1/app_acoplada.py` abierto en VSCode.

## 1.1 Primero, comprobar que funciona

No vamos a criticar código que no hayamos visto correr. Desde la carpeta `material/modulo_1`:

```powershell
uvicorn app_acoplada:app --port 8002 --reload
```

Abre `http://localhost:8002/docs`, despliega `POST /procesar` y pruébalo con un cuerpo mínimo:

```json
{"registros": [
  {"id_persona": 1, "id_hogar": 1, "departamento": "Bogota", "area": "Urbana", "sexo": "H", "edad": 30, "ocupado": 1, "ingreso": 1000000, "factor_expansion": 100},
  {"id_persona": 1, "id_hogar": 1, "departamento": "Bogota", "area": "Urbana", "sexo": "H", "edad": 30, "ocupado": 1, "ingreso": 1000000, "factor_expansion": 100},
  {"id_persona": 2, "id_hogar": 1, "departamento": "Bogota", "area": "Urbana", "sexo": "H", "edad": 40, "ocupado": 1, "ingreso": null, "factor_expansion": 100}
]}
```

> [!IMPORTANT]
> **✅ Checkpoint**
>
> La respuesta trae dos registros, el resumen dice un duplicado eliminado y un ingreso imputado, y la persona 2 tiene `ingreso_imputado: true` con el ingreso de la persona 1. Si tienes el muñeco del Taller 3 a la mano, `python -m ensamblador.probar --etapa 2` desde su carpeta también responde que cumple el contrato.

Funciona. Detén el servidor con Ctrl + C y ahora sí, a leerlo.

## 1.2 Cuatro cosas en treinta líneas

Lee la función `procesar` de arriba abajo y marca, al margen, a cuál de estas cuatro categorías pertenece cada línea. Los comentarios del archivo te dan pistas, pero hazlo tú antes de mirarlos.

**Transporte.** Recibir la petición HTTP, extraer el JSON, devolver una respuesta con su código de estado. Las líneas con `request`, `JSONResponse` y `HTTPException`.

**Traducción.** Convertir la lista de diccionarios en un DataFrame y, al final, el DataFrame en una lista de diccionarios donde los vacíos sean `null`. Son líneas de pandas, y sin embargo no son estadística: son el idioma del contrato convertido al idioma de las reglas.

**Reglas.** Eliminar duplicados por `id_persona`, recortar los ingresos por encima del percentil, imputar a los ocupados sin ingreso con la mediana de su grupo. Esto es lo que un metodólogo revisaría, y es lo único que no podría escribir otra persona por ti.

**Decisiones.** El percentil 99 y los grupos `area` y `sexo`. Son constantes al inicio del archivo, lo que ya es mejor que tenerlas sueltas, pero siguen siendo parte del código: cambiarlas es editar y reiniciar.

> [!NOTE]
> **📘 Concepto**
>
> Que cuatro cosas convivan en una función no es un error en sí mismo. El problema aparece cuando cambian por razones distintas y a ritmos distintos. El transporte cambia cuando cambia la infraestructura (otra versión de FastAPI, otro formato de intercambio). Las reglas cambian cuando cambia la metodología. Las decisiones cambian cada vez que alguien quiere probar un escenario. Si todo vive junto, cada cambio arrastra a los demás, y cada prueba exige levantar todo. A esa dependencia innecesaria entre cosas que cambian por razones distintas se le llama acoplamiento.

## 1.3 Ejercicio: la tabla de razones para cambiar

Llena esta tabla con el archivo abierto. Para cada pedido, anota qué líneas tocarías y qué otras cosas corres el riesgo de romper al tocarlas.

| Pedido | Líneas que cambian | Qué se puede romper sin querer |
|----|----|----|
| Metodología pide recortar al percentil 95 y probar también con 97.5 | | |
| El equipo de Kedro quiere usar la limpieza como nodo, sin HTTP | | |
| El muñeco pasa a intercambiar Parquet en vez de JSON | | |
| Hay que probar la imputación con cinco filas, sin servidor | | |
| Se agrega una regla: descartar personas con edad mayor a 120 | | |

La fila que más enseña es la cuarta. Para probar una regla estadística con datos mínimos tienes que simular una petición HTTP, porque la regla está dentro del manejador de la ruta. Eso significa que la mayoría de la gente no la prueba.

> [!TIP]
> **💡 Tip**
>
> Si vienes de SAS o de R, piensa en una macro o una función que calcula un indicador y además imprime el reporte, guarda el Excel y manda el correo. Cuando cambia el formato del correo hay que volver a probar el cálculo. Es el mismo acoplamiento, en otro lenguaje.

## 1.4 Hacia dónde vamos

Lo que sigue en los módulos 2 y 3 se puede resumir en un dibujo. Las reglas y las decisiones van al centro, en un paquete que no importa nada que no sea pandas. Alrededor, un anillo con lo que esas reglas necesitan del exterior, dicho como interfaces. Y afuera, un adaptador por cada forma de entrar y salir, todos apuntando hacia el centro.

```text
                 +-------------------------------+
   HTTP  ----->  |  adaptador http               |
   Kedro ----->  |  adaptador kedro   -->  +------------------+
   CLI   ----->  |  adaptador cli     -->  |     dominio      |
   CSV   <----   |  adaptador archivos     |  reglas, política |
                 |                         +------------------+
                 +-------------------------------+
```

Una forma de verlo, si te sirve la analogía: en un edificio, la estructura se calcula y se construye una vez, y las instalaciones (eléctrica, hidráulica, red) van por fuera de ella, en ductos. Se pueden cambiar sin tocar una viga. Nadie vacía los cables dentro del concreto, aunque sería más rápido el primer día. En `app_acoplada.py`, los cables están dentro del concreto.

## 1.5 Troubleshooting del Módulo 1

| Síntoma | Causa probable | Solución |
|----|----|----|
| `uvicorn` dice que no encuentra `app_acoplada` | Lo corriste desde otra carpeta | Ubícate en `material/modulo_1` |
| `/docs` responde pero `/procesar` da error 500 con `KeyError` | El JSON de prueba no tiene todas las columnas | Usa el cuerpo de la sección 1.1 completo |
| El `probar` del muñeco dice "no responde" | El puerto 8002 está ocupado por tu propia etapa del Taller 3 | Cierra la otra terminal o usa `--port 8012` en ambos |

## 1.6 Para profundizar (opcional)

- Busca en tu trabajo el script más grande que tengas y hazle la misma tabla de la sección 1.3 con tres pedidos reales que te hayan hecho este año. No lo refactorices. Solo mide cuánto arrastra cada cambio.
