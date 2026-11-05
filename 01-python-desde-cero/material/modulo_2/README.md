# Material complementario — Módulo 2

Archivos de referencia para el Módulo 2.

## Qué hay adentro

`generar_datos.py` es el mismo del Módulo 1, lo dejo aquí para que no tengas que buscarlo en otra carpeta. `analisis.ipynb` es el notebook Jupyter "antes" — la versión exploratoria del análisis. `analisis_v2.py` es el "después": el mismo análisis migrado a un script con funciones reutilizables. La diferencia entre los dos es exactamente lo que el módulo te enseña a hacer.

En `soluciones_retos/` está la solución al reto principal (agregar `mediana_por_grupo` y exportar a dos hojas de Excel).

## Antes de empezar

Si no tienes `datos_ejemplo.csv` en esta carpeta, genéralo:

```powershell
.venv\Scripts\activate
python generar_datos.py
```

## El notebook

Abre `analisis.ipynb` haciendo doble clic en VSCode. La primera vez te va a pedir seleccionar un kernel — escoge el de tu `.venv`. Luego ejecutas celda por celda con Shift + Enter.

Si te sale `ModuleNotFoundError: pandas` al ejecutar, VSCode escogió el intérprete equivocado. En la esquina superior derecha del notebook dice "Select Kernel" — haz clic y elige el del `.venv`.

## El script migrado

```powershell
python analisis_v2.py
```

La diferencia clave con `analisis.py` del Módulo 1: este está organizado en funciones reutilizables y se puede importar desde otros scripts. Por ejemplo:

```python
from analisis_v2 import promedio_por_grupo
```

Eso lo hace base para construir aplicativos más grandes — es la práctica estándar en Python.

## Si algo falla

Sección 2.7 de la guía (Troubleshooting del Módulo 2).
