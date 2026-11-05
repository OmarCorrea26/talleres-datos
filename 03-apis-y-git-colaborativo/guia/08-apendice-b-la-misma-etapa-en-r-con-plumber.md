# Apéndice B — La misma etapa en R con plumber

Para quienes trabajan en R: el contrato es JSON y HTTP, así que una etapa se puede implementar en R sin que el ensamblador lo note. `plumber` es al ecosistema R lo que FastAPI a Python: convierte funciones en rutas HTTP mediante comentarios especiales (`#* @get`, `#* @post`).

El archivo `apendice_r/etapa_plumber.R` del repositorio implementa la etapa 3 (calibrar). Instala y ejecuta:

```text
install.packages(c("plumber", "jsonlite", "dplyr"))
```

```powershell
Rscript -e "plumber::pr_run(plumber::pr('apendice_r/etapa_plumber.R'), port = 8003)"
```

Con el servicio de R corriendo en el puerto 8003, `python -m ensamblador.probar --etapa 3` debería dar `[OK]` igual que con la versión en Python. Puntos de atención al traducir:

- **Nulos.** `jsonlite::fromJSON` convierte `null` en `NA`; al devolver, `toJSON` por defecto omite o escribe `"NA"` según el tipo. Usa el serializador `unboxedJSON` (ya está en el ejemplo) y, si un campo nullable sale mal, `jsonlite::toJSON(x, na = "null")` explícito.
- **Enteros vs decimales.** R no distingue `1` de `1.0` en JSON salvo que uses `as.integer`. Para `ocupado` e `id_*`, conviértelos antes de devolver.
- **Listas vs objetos.** Un `data.frame` se serializa como lista de objetos (correcto para `registros`); una lista con nombres se serializa como objeto (correcto para `resumen`). Un vector con nombres **no** es un objeto: envuélvelo con `as.list`.
- **Equivalencias.** `httr2` para consumir APIs (como `httpx`), `testthat` para pruebas (como `pytest`), `renv` para entornos reproducibles (como el `.venv` + `requirements.txt`).

> [!TIP]
> **💡 Tip**
>
> Un equipo mixto Python/R es completamente normal en estadística oficial. Lo que lo hace viable no es que todos usen lo mismo, sino que el contrato entre las partes sea explícito y verificable. Ese es el argumento de fondo de todo este taller.
