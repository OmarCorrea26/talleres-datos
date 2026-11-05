# Guía del facilitador — Taller 3 (solo para quien facilita)

Esta carpeta NO va al repositorio que ven los participantes ni al zip que reciben (`empaquetar.py` la excluye salvo que se pida `--con-facilitador`). Contiene las soluciones de referencia y el generador de fixtures.

## Antes de publicar el repo

1. Crea el repo `taller-api-muneco` en tu cuenta (público o privado; si es privado, agrega a los seis como colaboradores con permiso *Write*).
2. Sube el contenido de esta carpeta de taller tal cual, sin `facilitador/` ni `guia/` (incluye `fixtures/`, que ya están generados).
3. Protege `main`: Settings → Branches → Add rule: *Require a pull request before merging* (1 aprobación), *Require status checks to pass* (selecciona "Pruebas de contrato"), *Do not allow bypassing* opcional.
4. Asigna las etapas en la tabla del README y haz commit. Sugerencia: etapas 1 y 2 a quienes tengan menos experiencia; 3 y 5 a quienes se muevan bien con estadística; 4 y 6 son intermedias.
5. Verifica el flujo tú mismo: abre un PR de prueba y confirma que GitHub Actions corre.

## Durante el taller: el "cambio de contrato" planeado

El aprendizaje de `rebase` solo ocurre si `main` cambia debajo de ellos. Cuando 3 o 4 ya tengan su rama abierta, haz **un PR de contrato** con uno de estos cambios (elige uno, anúncialo en un Issue):

- **Opción suave:** agrega un campo `version_contrato: str = "1.1"` a `ResumenValidacion`, `ResumenLimpieza` y `ResumenCalibracion` (etapas 1-3 deben devolverlo). Cambia también `README.md` y el `pull_request_template.md`.
- **Opción fuerte:** cambia `UMBRAL_CV_BUENA` de 7.5 a 5.0 en `contrato/validaciones.py` (afecta a la etapa 6 y a los fixtures: regenera `etapa_6_salida.json` con `generar_fixtures.py`).

Al mezclarlo, todos tienen que `git fetch` + `git rebase origin/main`. Quienes hayan tocado un archivo del contrato (no deberían) verán conflicto; el resto verá el rebase limpio. Ambos casos están cubiertos en la guía (sección 3.8).

## Regenerar fixtures

Si cambias `generar_datos.py`, el contrato o una solución de referencia:

```powershell
cd taller-api-muneco
python datos/generar_datos.py
python ..\facilitador\generar_fixtures.py
```

`generar_fixtures.py` valida cada etapa de referencia contra el contrato antes de guardar.

## Rúbrica de revisión sugerida

| Criterio | Peso |
|---|---|
| `probar --etapa N` en OK y CI verde | 40 % |
| Código legible: nombres claros, funciones cortas, comentarios donde hay una decisión estadística | 20 % |
| Historia de Git limpia: rama propia, commits con convención, rebase hecho, solo archivos de su etapa | 20 % |
| Revisión hecha a otro compañero con al menos un comentario sustantivo | 20 % |
