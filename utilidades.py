"""
Módulo de utilidades para el manejo de grafos de rutas viales en Ecuador.
Unidad 3: Grafos - Algoritmos y Estructuras de Datos.
"""

# Red de ejemplo de 7 ciudades de Ecuador representada como lista de adyacencia.
# Grafo no dirigido ponderado: cada clave es una ciudad y el valor es una lista
# de tuplas (ciudad_vecina, distancia_en_km).
#


# ============================================================================
# R1: MODELADO DEL GRAFO
# ============================================================================
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


# ============================================================================
# R2: RECORRIDO EN ANCHURA (BFS), RUTAS Y CONECTIVIDAD
# ============================================================================

def bfs(grafo, origen):
    """
    Realiza un recorrido BFS propio desde un vértice origen usando deque.
    Devuelve un diccionario {ciudad: escalas_desde_origen} y el diccionario de padres.
    
    # BFS: O(V + E)
    donde V es el número de vértices y E el número de aristas.
    """
    if origen not in grafo:
        return {}, {}

    escalas = {origen: 0}
    padres = {origen: None}
    cola = deque([origen])

    while cola:
        actual = cola.popleft()

        for vecino, _ in grafo.get(actual, []):
            if vecino not in escalas:
                escalas[vecino] = escalas[actual] + 1
                padres[vecino] = actual
                cola.append(vecino)

    return escalas, padres
    return escalas, padres


def reconstruir_ruta(padres, origen, destino):
    """
    Reconstruye la ruta con menor número de escalas desde origen hasta destino
    a partir del diccionario de padres devuelto por BFS.
    
    Retorna:
        list: Lista de ciudades en orden [origen, ..., destino] o [] si no es alcanzable.
    """
    if destino not in padres:
        return []

    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = padres.get(actual)

    ruta.reverse()
    if ruta and ruta[0] == origen:
        return ruta
    return []


def verificar_conectividad(grafo, alcanzables):
    """
    Detecta si la red está completamente conectada o si existen ciudades aisladas
    comparando las ciudades alcanzables con la totalidad de ciudades del grafo.
    """
    todas_las_ciudades = set(grafo.keys())
    ciudades_visitadas = set(alcanzables.keys()) if isinstance(alcanzables, dict) else set(alcanzables)
    aisladas = sorted(list(todas_las_ciudades - ciudades_visitadas))

    print("\n--- ESTADO DE CONECTIVIDAD DE LA RED ---")
    """El bucle if muestra si todo está conectado o hay ciudades no alcanzables"""
    if not aisladas:
        print("✔ La red está COMPLETAMENTE CONECTADA. Todas las ciudades son alcanzables.")
        return True, []
    else:
        print("✘ La red NO está completamente conectada.")
        print(f"Ciudades aisladas / inalcanzables ({len(aisladas)}): {', '.join(aisladas)}")
        return False, aisladas


def obtener_grafo_con_aislada(grafo_base=GRAFO_ECUADOR, ciudad_aislada="Galápagos"):
    """
    Genera una copia de la red agregando una ciudad aislada (sin aristas)
    para pruebas de conectividad, sin alterar el grafo original.
    """
    nuevo_grafo = {ciudad: list(vecinos) for ciudad, vecinos in grafo_base.items()}
    nuevo_grafo[ciudad_aislada] = []
    return nuevo_grafo
