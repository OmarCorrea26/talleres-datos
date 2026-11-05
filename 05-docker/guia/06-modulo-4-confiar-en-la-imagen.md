# Módulo 4 — Confiar en la imagen

Objetivo: que GitHub construya y arranque la imagen en cada Pull Request, que sepas revisar un Dockerfile escrito por un asistente de IA, y cerrar el taller y la ruta con el Issue de entrega. Una hora.

### Lo que necesitas antes de empezar

- El proyecto del Taller 4 con su Dockerfile del Módulo 2, en un repositorio de GitHub.
- El asistente de IA del Taller 1 funcionando en VSCode.

## 4.1 Lo que se prueba es lo que se despliega

En el Taller 3, GitHub Actions corría `pytest` en cada Pull Request. Eso verifica el código. No verifica que el código, empaquetado en la imagen con las dependencias que el Dockerfile instala, arranque. Hay un espacio entre "las pruebas pasan" y "la imagen corre", y en ese espacio viven los errores más incómodos: una dependencia que falta en `pyproject.toml` pero está en tu entorno, un archivo que `.dockerignore` excluyó y el servicio necesita, un `CMD` con una ruta mal escrita.

La solución es que la integración continua construya la imagen y la arranque, igual que lo hiciste a mano en el Módulo 2.

## 4.2 El flujo

En el repositorio del Taller 4, crea `.github/workflows/imagen.yml`:

```yaml
# .github/workflows/imagen.yml
# Integración continua para un servicio en contenedor: en cada Pull Request,
# GitHub corre las pruebas, construye la imagen y la arranca para comprobar que
# responde. Si cualquiera de las tres cosas falla, el PR queda en rojo.
#
# Comparar con el flujo del Taller 3: allá solo se corría pytest. Aquí, además,
# se verifica que lo que se va a desplegar es exactamente lo que se probó.
name: Imagen del servicio

on:
  push:
    branches: [main]
  pull_request:

jobs:
  pruebas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[http,parquet,dev]"
      - run: pytest -q

  imagen:
    needs: pruebas
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Construir la imagen
        run: docker build -t limpieza:${{ github.sha }} .
      - name: Arrancarla y comprobar que responde
        run: |
          docker run -d --rm --name prueba -p 8002:8002 limpieza:${{ github.sha }}
          for i in $(seq 1 15); do
            if curl -fs http://localhost:8002/salud; then exit 0; fi
            sleep 2
          done
          echo "El servicio no respondió a tiempo"
          docker logs prueba
          exit 1
      - name: Detener
        if: always()
        run: docker stop prueba || true
```

Dos trabajos. El primero es el del Taller 3. El segundo depende de él (`needs`), construye la imagen con una etiqueta que es el identificador del commit, la arranca y durante treinta segundos pregunta a `/salud`. Si responde, termina en verde; si no, imprime el registro del contenedor para que se vea por qué y falla. El último paso detiene el contenedor pase lo que pase.

Haz commit en una rama, abre un Pull Request y mira la pestaña Actions.

> [!IMPORTANT]
> **✅ Checkpoint**
>
> Dos checks en el Pull Request: `pruebas` y `imagen`, ambos en verde. En el registro de `imagen` se ve la construcción capa por capa y la respuesta `{"etapa":2,"nombre":"limpiar","estado":"ok"}` de `/salud`. Las máquinas de GitHub ya traen Docker, de modo que no hubo que instalar nada.

> [!NOTE]
> **📘 Concepto**
>
> La etiqueta `${{ github.sha }}` no es decorativa. Cada construcción queda identificada por el commit exacto del que salió, de modo que si un día una imagen falla en producción se sabe con precisión qué código contiene. El paso siguiente, que este taller no da, es subir esa imagen a un registro con esa misma etiqueta, para que el servidor la descargue en vez de construirla. Es una línea más en el flujo y una conversación con quien administra el registro.

## 4.3 Dockerfiles pedidos a la IA: la lista de verificación

Un asistente de IA escribe un Dockerfile funcional en segundos, y casi siempre con los mismos tres defectos: corre como root, usa `latest` en alguna parte y copia todo el proyecto con `COPY . .`. Funciona, pasa el checkpoint, y es exactamente lo que un equipo de seguridad rechaza. Pasa cada propuesta por esta lista antes de aceptarla.

1. ¿El `FROM` nombra una versión concreta? `python:3.11-slim` sí; `python`, `python:3` o `python:latest` no.
2. ¿Hay un `USER` que no sea root antes del `CMD`? Si no lo hay, pídelo.
3. ¿Las dependencias se instalan antes de copiar el código? Si copia todo y después instala, cada cambio reinstala.
4. ¿Hay un `.dockerignore`? Si el asistente no lo propuso, el entorno virtual va a viajar en cada construcción.
5. ¿Copia solo lo que el proceso necesita? `COPY . .` trae pruebas, documentación y lo que haya. Mejor nombrar las carpetas.
6. ¿Instala solo lo que el proceso necesita? Si ves pytest o kedro-viz en la imagen de un servicio, sobra.
7. ¿El `CMD` escucha en `0.0.0.0`? Si dice `localhost` o no dice nada, no va a funcionar desde afuera.
8. ¿Hay algún secreto escrito? Contraseñas, tokens o rutas a credenciales en `ENV` o en `COPY` son inaceptables: eso entra por variables de entorno al correr, nunca a la imagen.
9. ¿Entiendes cada instrucción? Si hay una que no, pide que la explique. Si sigue sin quedar clara, no la uses.

> [!TIP]
> **💡 Tip**
>
> Un prompt que ahorra la mitad de estas correcciones: "Escribe un Dockerfile para este proyecto con base `python:3.11-slim` fijada, usuario sin privilegios, dependencias instaladas antes de copiar el código, copiando solo `pyproject.toml` y `src/`, con `HEALTHCHECK` sobre `/salud` y uvicorn en `0.0.0.0`. Incluye el `.dockerignore`." Decir lo que quieres es más barato que corregir lo que no pediste.

## 4.4 Ejercicio práctico: una imagen con IA, revisada

Pídele al asistente el `Dockerfile.cli` del ejercicio 2.9, sin darle la lista de la sección 4.3. Revísalo con la lista, anota qué puntos falló, corrígelo y construye. Después pídeselo de nuevo con el prompt del Tip y compara cuántos puntos falló esta vez. Guarda las dos versiones en `docs/` del proyecto con un párrafo sobre la diferencia: es el mejor argumento que vas a tener para explicarle a alguien por qué se revisa lo que la IA produce.

## 4.5 Hasta dónde llega este taller

Lo que no cubre, para que sepas qué viene después si lo necesitas. Subir imágenes a un registro privado, para que un servidor las descargue sin construirlas. Orquestadores como Kubernetes, que corren muchos contenedores en muchas máquinas con reinicio automático; para siete servicios en un servidor, Compose alcanza y sobra. Y gestión de secretos, que en producción se resuelve con herramientas del proveedor de infraestructura.

Lo que sí tienes al terminar: procesos que corren igual en cualquier máquina, descritos en archivos que viven en el repositorio junto al código, verificados en cada Pull Request. Para la mayoría de los procesos estadísticos de un equipo, eso es el noventa por ciento del camino a producción.

### Reflexión final de la ruta

Vuelve al Taller 1 un momento: un script con tres funciones que calculaba promedios de un CSV. Cinco talleres después, ese mismo proceso es un pipeline con linaje, seis servicios con contrato, un dominio con pruebas y patrones con nombre, y un `compose.yaml` que lo levanta entero en cualquier computador. Ninguno de los pasos fue grande. Cada uno separó algo que antes estaba junto: los datos del código, los pasos entre sí, las reglas del transporte, el proceso del entorno. Eso es lo que te llevas de la ruta, y es más que cualquier herramienta.

## 4.6 Entregable: Issue de validación

En el repositorio del Taller 4, ahora con su Dockerfile y su flujo, abre un Issue con el título `Entrega Taller 5 — [tu nombre]`:

```markdown
## Entrega Taller 5

- Repositorio: <enlace>
- Pull Request con los checks `pruebas` e `imagen` en verde: <enlace>
- Tamaño de la imagen `limpieza` (`docker images`): N MB
- `docker compose up` del muñeco con las seis partes verdes: sí / no

## El punto de la lista de verificación que la IA más falló

(dos o tres líneas)

## El proceso de mi trabajo que empaquetaría primero, y qué datos tendría que montar

(dos o tres líneas)
```

Asigna el Issue a quien facilita el taller. Con eso queda entregada la ruta completa.

## 4.7 Para profundizar (opcional)

- La documentación de GitHub sobre `docker/build-push-action` muestra cómo subir la imagen a GitHub Container Registry desde el mismo flujo, con tres líneas más.
- "The Twelve-Factor App" es el texto corto que resume las reglas de la sección 3.4 del Módulo 3 y de este módulo: configuración en el entorno, procesos sin estado, dependencias declaradas. Está en español y se lee en media hora.
