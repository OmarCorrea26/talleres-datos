# Soluciones a los retos del Módulo 1

Esta carpeta contiene las soluciones de referencia a los 4 retos opcionales
de la sección 1.12 "Para profundizar" de la guía del taller.

## ⚠️ Antes de mirar aquí

Estos archivos son **material de respaldo**, no una solución para copiar.
Intenta primero resolver cada reto por tu cuenta modificando tu propio
`analisis.py`. Si te quedas atascado más de 15 minutos en un reto, abre
el archivo de solución correspondiente, entiéndelo, y vuelve a tu código.

Aprender programación se trata mucho más de equivocarse y corregir que
de copiar respuestas correctas.

## Cómo ejecutarlos

Estos scripts esperan estar en la subcarpeta `soluciones_retos/`,
con el archivo `datos_ejemplo.csv` un nivel arriba (en la carpeta
del proyecto). Si los moviste a otra ubicación, ajusta la ruta en
`pd.read_csv("../datos_ejemplo.csv")` a la que corresponda en tu caso.

Para ejecutar cualquiera de ellos, con el entorno virtual `.venv` activo:

```
cd soluciones_retos
python reto1_groupby_area.py
```

## Lista de retos

| Archivo | Tema |
|---|---|
| `reto1_groupby_area.py` | Agrupar por área en lugar de sexo |
| `reto2_mediana.py` | Usar mediana en vez de promedio |
| `reto3_edad_por_sexo.py` | Calcular edad promedio por sexo |
| `reto4_exportar_excel.py` | Exportar resultados a un archivo .xlsx |
