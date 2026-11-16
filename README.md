# Algoritmos_Estructuras de Datos
# PROGRAMA DE RED DE CIUDADES: MODELADO, RECORRIDOS Y RUTA MÍNIMA
## Elaborado por: Alan Guillermo Peñafiel Gonzalez

Programa en Python que modela una red de ciudades de Ecuador conectadas por carreteras y responde preguntas sobre ella usando grafos: lista de adyacencia, BFS y Dijkstra.

## Cómo ejecutar
```bash
python main.py
```
No requiere librerías externas (solo Python 3.x). La red de ejemplo ya viene cargada.

## Archivos
 `main.py`: menú de consola principal.

 `utilidades.py`: funciones de cada requerimiento.

## Menú de Opciones

`1. Mostrar grafo y grados de las ciudades`

`2. Ruta con menor número de escalas (BFS) y conectividad`

`3. Ruta más corta en distancia (Dijkstra)`

`4. Comparación de rutas (BFS vs Dijkstra)`

`0. Salir`

## Tabla de Complejidades

| Requerimiento | Operación principal | Complejidad |
|---|---|---|
| R1 | Lista de adyacencia y cálculo de grados | O(V + E) |
| R2 | BFS desde una ciudad de origen | O(V + E) |
| R3 | Dijkstra con cola de prioridad (heap) | O((V + E) log V) |
| R4 | Comparación BFS vs Dijkstra | O((V + E) log V) |
