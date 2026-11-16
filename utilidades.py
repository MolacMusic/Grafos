"""
Módulo de utilidades para el manejo de grafos de rutas viales en Ecuador.
Unidad 3: Grafos - Algoritmos y Estructuras de Datos.
"""

from collections import deque
import heapq

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


# ============================================================================
# R3: CAMINO MÁS CORTO EN DISTANCIA (DIJKSTRA)
# ============================================================================

import heapq

# Dijkstra: O((V + E) log V)  (el factor log V viene de las operaciones push/pop del heap, cada una cuesta O(log V)).
def dijkstra(grafo, origen):
    """Devuelve {ciudad: distancia_minima_desde_origen}."""
    dist = {ciudad: float('inf') for ciudad in grafo}
    dist[origen] = 0
    heap = [(0, origen)]  # cola de prioridad
    while heap:
        d, u = heapq.heappop(heap)  # el mas cercano pendiente
        if d > dist[u]:
            continue  # ya teniamos una ruta mejor
        for vecino, peso in grafo[u]:
            if dist[u] + peso < dist[vecino]:  # relajacion
                dist[vecino] = dist[u] + peso
                heapq.heappush(heap, (dist[vecino], vecino))
    return dist


# ============================================================================
# R4: COMPARACIÓN DE RUTAS (ESCALAS BFS VS. DISTANCIA DIJKSTRA)
# ============================================================================

def calcular_distancia_ruta(grafo, ruta):
    """
    Calcula la distancia total acumulada en km de una ruta (secuencia de ciudades).
    Retorna 0 si la ruta tiene menos de dos ciudades o float('inf') si no es válida.
    """
    if not ruta or len(ruta) < 2:
        return 0
    distancia_total = 0
    for i in range(len(ruta) - 1):
        actual, siguiente = ruta[i], ruta[i + 1]
        encontrado = False
        for vecino, peso in grafo.get(actual, []):
            if vecino == siguiente:
                distancia_total += peso
                encontrado = True
                break
        if not encontrado:
            return float('inf')
    return distancia_total


# Comparación R4: O((V + E) log V) (por Dijkstra)
def ruta_minima(grafo, origen, destino):
    """
    Reconstruye el camino de menor distancia entre origen y destino usando
    las distancias calculadas por dijkstra().
    
    Partiendo del destino, retrocede eligiendo el vecino v tal que
    dist[v] + peso == dist[actual]. Devuelve la lista de ciudades.
    """
    if origen not in grafo or destino not in grafo:
        return []
    if origen == destino:
        return [origen]

    dist = dijkstra(grafo, origen)
    if dist.get(destino, float('inf')) == float('inf'):
        return []

    camino = [destino]
    actual = destino

    while actual != origen:
        retrocedio = False
        for vecino, peso in grafo.get(actual, []):
            if dist[vecino] + peso == dist[actual]:
                camino.append(vecino)
                actual = vecino
                retrocedio = True
                break
        if not retrocedio:
            return []

    camino.reverse()
    return camino


# ============================================================================
# R5: GRAFICAR GRAFO (FONDO BLANCO, PESOS EN KM Y NOMBRES DE CIUDADES)
# ============================================================================

def graficar_grafo(grafo):
    """
    Muestra el grafo en una ventana con fondo blanco, nombres de ciudades y pesos (km).
    No más, no menos. Utiliza Tkinter (biblioteca estándar, liviana y nativa).
    """
    try:
        import tkinter as tk
    except ImportError:
        print("[Error] No se encontró 'tkinter'. Instálelo en su entorno de Python.")
        return

    # Coordenadas relativas de las ciudades (distribución geográfica limpia)
    posiciones = {
        "Quito": (380, 80),
        "Ambato": (370, 175),
        "Riobamba": (380, 265),
        "Guayaquil": (200, 335),
        "Cuenca": (360, 405),
        "Machala": (210, 475),
        "Loja": (350, 545),
        "Galápagos": (90, 200)
    }

    try:
        ventana = tk.Tk()
    except tk.TclError as e:
        print(f"[Aviso] No fue posible abrir la interfaz gráfica: {e}")
        return

    ventana.title("Grafo de Rutas - Ecuador")
    ventana.geometry("700x620")
    ventana.resizable(False, False)
    ventana.configure(bg="white")

    canvas = tk.Canvas(ventana, width=700, height=620, bg="white", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # 1. Dibujar aristas y pesos en km
    aristas_dibujadas = set()
    for ciudad, vecinos in grafo.items():
        if ciudad not in posiciones:
            continue
        x1, y1 = posiciones[ciudad]

        for vecino, peso in vecinos:
            if vecino not in posiciones:
                continue
            arista = tuple(sorted([ciudad, vecino]))
            if arista in aristas_dibujadas:
                continue
            aristas_dibujadas.add(arista)

            x2, y2 = posiciones[vecino]

            # Quito - Cuenca directa: curva suave hacia la derecha para no tapar ciudades intermedias
            if arista == ("Cuenca", "Quito"):
                cx, cy = 510, 240
                canvas.create_line(x1, y1, cx, cy, x2, y2, smooth=True, fill="#64748b", width=2)
                canvas.create_rectangle(cx - 24, cy - 9, cx + 24, cy + 9, fill="white", outline="white")
                canvas.create_text(cx, cy, text=f"{peso} km", font=("Arial", 8, "bold"), fill="#334155")
            else:
                canvas.create_line(x1, y1, x2, y2, fill="#94a3b8", width=1)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                canvas.create_rectangle(mx - 24, my - 9, mx + 24, my + 9, fill="white", outline="white")
                canvas.create_text(mx, my, text=f"{peso} km", font=("Arial", 8), fill="#334155")

    # 2. Dibujar nodos y nombres de ciudades
    radio = 14
    for ciudad in grafo:
        if ciudad not in posiciones:
            continue
        cx, cy = posiciones[ciudad]

        # Nodo
        canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio, fill="#38bdf8", outline="#0284c7", width=2)

        # Nombre de la ciudad
        offset_x, offset_y = 0, -22
        if ciudad in ("Guayaquil", "Machala"):
            offset_x, offset_y = -50, 0

        canvas.create_text(cx + offset_x, cy + offset_y, text=ciudad, font=("Arial", 9, "bold"), fill="#0f172a")

    print("\n[i] Mostrando ventana del grafo. Ciérrela para volver al menú.")
    ventana.mainloop()



