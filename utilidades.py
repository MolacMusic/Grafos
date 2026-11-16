"""
Módulo de utilidades para el manejo de grafos de rutas viales en Ecuador.
Unidad 3: Grafos - Algoritmos y Estructuras de Datos.
"""

# Red de ejemplo de 7 ciudades de Ecuador representada como lista de adyacencia.
# Grafo no dirigido ponderado: cada clave es una ciudad y el valor es una lista
# de tuplas (ciudad_vecina, distancia_en_km).
#
# NOTA DE DISEÑO:
# La conexión directa Quito - Cuenca es de 520 km (1 sola arista / 0 escalas intermedias).
# Sin embargo, la ruta Quito -> Ambato -> Riobamba -> Cuenca suma 135 + 55 + 255 = 445 km
# (3 aristas / 2 escalas intermedias). Esto permite que la ruta con menos escalas
# sea diferente a la ruta con menor distancia en kilómetros.
GRAFO_ECUADOR = {
    "Quito": [
        ("Ambato", 135),
        ("Cuenca", 520)
    ],
    "Ambato": [
        ("Quito", 135),
        ("Riobamba", 55),
        ("Guayaquil", 275)
    ],
    "Riobamba": [
        ("Ambato", 55),
        ("Cuenca", 255),
        ("Guayaquil", 230)
    ],
    "Cuenca": [
        ("Quito", 520),
        ("Riobamba", 255),
        ("Guayaquil", 195),
        ("Machala", 170),
        ("Loja", 210)
    ],
    "Guayaquil": [
        ("Ambato", 275),
        ("Riobamba", 230),
        ("Cuenca", 195),
        ("Machala", 180)
    ],
    "Machala": [
        ("Guayaquil", 180),
        ("Cuenca", 170),
        ("Loja", 215)
    ],
    "Loja": [
        ("Cuenca", 210),
        ("Machala", 215)
    ]
}


def mostrar_grafo(grafo):
    """
    Muestra las ciudades y sus conexiones con las distancias.
    """
    print("\n--- GRAFO: LISTA DE ADYACENCIA ---")
    # Complejidad: O(V + E)
    for ciudad, vecinos in grafo.items():
        conexiones = [f"{vecino} ({distancia} km)" for vecino, distancia in vecinos]
        if conexiones:
            print(f"• {ciudad} -> [{', '.join(conexiones)}]")
        else:
            print(f"• {ciudad} -> [Sin conexiones]")


def grado(grafo):
    """
    Muestra cuántas conexiones tiene cada ciudad.
    """
    print("\n--- GRADO DE LAS CIUDADES ---")
    # Complejidad: O(V), ya que len() obtiene el tamaño de cada lista.
    """ 
    Para el grado de los gráfos se calcula la longitud de la lista de vecinos"""
    for ciudad, vecinos in grafo.items():
        print(f"• {ciudad}: grado {len(vecinos)}")