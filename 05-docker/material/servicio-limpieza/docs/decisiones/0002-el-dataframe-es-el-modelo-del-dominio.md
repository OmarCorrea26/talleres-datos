# 0002. El DataFrame de pandas es el modelo de datos del dominio

Fecha: 2026-11-05
Estado: aceptada

## Contexto

En la literatura de arquitectura limpia el dominio suele representarse con clases propias (una `Persona`, un `Hogar`) y nunca con estructuras de una biblioteca externa. En un proceso estadístico, sin embargo, las reglas se expresan sobre columnas completas (percentiles, medianas por grupo, duplicados por llave), y traducir mil registros a objetos y de vuelta para cada regla sería lento y, sobre todo, ajeno a cómo piensa quien escribe las reglas.

## Decisión

Las reglas del dominio reciben y devuelven `pandas.DataFrame`. Lo que sí se modela con clases propias son las decisiones (`PoliticaDeLimpieza`) y los resultados (`ResumenLimpieza`), porque son pocos valores con significado y conviene que tengan nombre, validación y tipo.

## Consecuencias

Ganamos reglas que se leen igual que el análisis que las originó y que un analista puede revisar. Pagamos una dependencia del dominio hacia pandas, que aceptamos con los ojos abiertos: pandas es, para este equipo, parte del lenguaje, no un framework. Si algún día el volumen obliga a cambiar a otra biblioteca de tablas, este registro marca el lugar exacto donde se tomó la decisión contraria.
