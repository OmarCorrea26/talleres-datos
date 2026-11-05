# Taller de Python — [Tu Nombre]

Repositorio personal del taller "Python para Analistas Estadísticos".

## Sobre este repositorio

Este repo contiene mis avances de los cinco módulos del taller. Cada módulo tiene su propósito específico, y al final voy a tener una base sólida de Python, control de versiones y uso de IA para desarrollo.

## Estructura

```
.
├── hola.py                  # Mi primer script (Módulo 1)
├── generar_datos.py         # Genera el dataset sintético (Módulo 1)
├── analisis.py              # Análisis básico — versión inicial (Módulo 1)
├── analisis_v2.py           # Análisis modularizado en funciones (Módulo 2)
├── analisis.ipynb           # Notebook Jupyter del análisis (Módulo 2)
└── README.md                # Este archivo
```

## Cómo correr el código

Asumiendo que ya está clonado el repo:

```powershell
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar dependencias
pip install pandas openpyxl

# 3. Generar los datos (la primera vez)
python generar_datos.py

# 4. Correr el análisis
python analisis_v2.py
```

## Sobre el taller

El taller cubre cinco módulos secuenciales:

| Módulo | Tema |
|---|---|
| 0 | Antes de empezar — instalación |
| 1 | Tu primer proyecto en Python |
| 2 | De Jupyter a `.py` — funciones |
| 3 | Git y GitHub — desarrollo colaborativo |
| 4 | IA en el IDE |
