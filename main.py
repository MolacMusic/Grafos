"""
Realizado por: Alan Peñafiel

Programa principal para la gestión y análisis de rutas viales en Ecuador.
Algoritmos y Estructuras de Datos - Unidad 3: Grafos.
"""

from utilidades import (
    GRAFO_ECUADOR,
    mostrar_grafo,
    grado,
    bfs,
    reconstruir_ruta,
    verificar_conectividad,
    obtener_grafo_con_aislada,
    dijkstra,
    calcular_distancia_ruta,
    ruta_minima,
    graficar_grafo
)


def pedir_ciudad(grafo, mensaje="Ingrese la ciudad: "):
    """Solicita una ciudad y valida que pertenezca al grafo activo (insensible a mayúsculas)."""
    while True:
        entrada = input(mensaje).strip()
        coincidencia = next((c for c in grafo if c.lower() == entrada.lower()), None)
        if coincidencia:
            return coincidencia
        print(f"[Error] '{entrada}' no es válida. Elija entre: {', '.join(grafo.keys())}")


def elegir_red(grafo_base):
    """Permite seleccionar la red estándar o la de prueba con ciudad aislada."""
    print("\nModalidad de red:")
    print("  1. Red estándar (7 ciudades)")
    print("  2. Red de prueba con ciudad aislada ('Galápagos')")
    opc = input("Seleccione modalidad (1 o 2) [Enter para 1]: ").strip()
    if opc == "2":
        print("[i] Red con ciudad aislada activada.")
        return obtener_grafo_con_aislada(grafo_base, "Galápagos")
    return grafo_base


def mostrar_menu():
    """Muestra el menú principal optimizado en consola."""
    print("\n" + "=" * 54)
    print("       SISTEMA DE RUTAS VIALES DEL ECUADOR")
    print("=" * 54)
    print("1. Mostrar grafo y grados de las ciudades")
    print("2. Recorrido BFS: escalas y conectividad")
    print("3. Ruta más corta en distancia (Dijkstra)")
    print("4. Comparar rutas (BFS vs. Dijkstra)")
    print("5. Graficar grafo")
    print("0. Salir")
    print("-" * 54)


def main():
    """Función principal y bucle de control interactivo."""
    grafo = GRAFO_ECUADOR

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        # --------------------------------------------------------------------
        # 1. MOSTRAR GRAFO Y GRADOS
        # --------------------------------------------------------------------
        if opcion == "1":
            # Complejidad: O(V + E) para mostrar_grafo y O(V) para grado
            mostrar_grafo(grafo)
            grado(grafo)
            input("\nPresione Enter para continuar...")

        # --------------------------------------------------------------------
        # 2. BFS: ESCALAS Y CONECTIVIDAD
        # --------------------------------------------------------------------
        elif opcion == "2":
            print("\n--- RECORRIDO BFS Y CONECTIVIDAD ---")
            grafo_activo = elegir_red(grafo)

            ciudades_disponibles = list(grafo_activo.keys())
            print(f"Ciudades disponibles: {', '.join(ciudades_disponibles)}")

            origen = pedir_ciudad(grafo_activo, "\nIngrese la ciudad de origen: ")

            # BFS: O(V + E)
            escalas, padres = bfs(grafo_activo, origen)

            print(f"\n--- CIUDADES ALCANZABLES DESDE {origen.upper()} (BFS) ---")
            for ciudad, num in sorted(escalas.items(), key=lambda x: (x[1], x[0])):
                etiqueta = "(Origen)" if num == 0 else f"{num} escala(s)"
                print(f"• {ciudad}: {etiqueta}")

            verificar_conectividad(grafo_activo, escalas)

            if input("\n¿Desea consultar la ruta a un destino? (s/n) [n]: ").strip().lower() == "s":
                destino = pedir_ciudad(grafo_activo, "Ingrese la ciudad de destino: ")
                if destino in escalas:
                    ruta = reconstruir_ruta(padres, origen, destino)
                    print(f"-> Ruta: {' -> '.join(ruta)} ({escalas[destino]} escalas)")
                else:
                    print(f"[!] No existe ruta hacia {destino} (ciudad inalcanzable).")

            input("\nPresione Enter para continuar...")

        # --------------------------------------------------------------------
        # 3. DIJKSTRA: DISTANCIAS MÍNIMAS
        # --------------------------------------------------------------------
        elif opcion == "3":
            print("\n--- DISTANCIAS MÍNIMAS (DIJKSTRA) ---")
            grafo_activo = elegir_red(grafo)

            ciudades_disponibles = list(grafo_activo.keys())
            print(f"Ciudades disponibles: {', '.join(ciudades_disponibles)}")

            origen = pedir_ciudad(grafo_activo, "\nIngrese la ciudad de origen: ")

            # Dijkstra: O((V + E) log V)
            distancias = dijkstra(grafo_activo, origen)

            print(f"\n--- DISTANCIAS MÍNIMAS DESDE {origen.upper()} ---")
            for ciudad, d in sorted(distancias.items(), key=lambda x: (x[1], x[0])):
                print(f"• {ciudad}: {d} km" if d != float('inf') else f"• {ciudad}: inalcanzable")

            alcanzables = {c: d for c, d in distancias.items() if c != origen and d != float('inf')}
            if alcanzables:
                c_cercana = min(alcanzables, key=alcanzables.get)
                c_lejana = max(alcanzables, key=alcanzables.get)
                print(f"\n• Más CERCANA a {origen}: {c_cercana} ({alcanzables[c_cercana]} km)")
                print(f"• Más LEJANA de {origen}:  {c_lejana} ({alcanzables[c_lejana]} km)")

            inalcanzables = [c for c, d in distancias.items() if d == float('inf')]
            if inalcanzables:
                print(f"• Ciudades INALCANZABLES ({len(inalcanzables)}): {', '.join(inalcanzables)}")

            input("\nPresione Enter para continuar...")

        # --------------------------------------------------------------------
        # 4. COMPARAR RUTAS: BFS VS. DIJKSTRA
        # --------------------------------------------------------------------
        elif opcion == "4":
            print("\n--- COMPARACIÓN: BFS VS. DIJKSTRA ---")
            ciudades_disponibles = list(grafo.keys())
            print(f"Ciudades disponibles: {', '.join(ciudades_disponibles)}")

            origen = pedir_ciudad(grafo, "\nIngrese ciudad de origen: ")
            destino = pedir_ciudad(grafo, "Ingrese ciudad de destino: ")

            if origen == destino:
                print(f"\n[!] El origen y destino coinciden ({origen}): 0 escalas y 0 km.")
            else:
                # Comparación R4: O((V + E) log V)
                _escalas, padres_bfs = bfs(grafo, origen)
                ruta_bfs = reconstruir_ruta(padres_bfs, origen, destino)

                ruta_dijkstra = ruta_minima(grafo, origen, destino)
                distancias = dijkstra(grafo, origen)

                if not ruta_bfs or not ruta_dijkstra:
                    print(f"\n[!] No existe ruta entre {origen} y {destino}.")
                else:
                    dist_bfs = calcular_distancia_ruta(grafo, ruta_bfs)
                    esc_bfs = len(ruta_bfs) - 1

                    dist_dijk = distancias[destino]
                    esc_dijk = len(ruta_dijkstra) - 1

                    print(f"\n--- RESULTADOS: {origen.upper()} -> {destino.upper()} ---")
                    print(f"1. BFS (Menos escalas):  {' -> '.join(ruta_bfs)} | {esc_bfs} escala(s) | {dist_bfs} km")
                    print(f"2. Dijkstra (Menor km): {' -> '.join(ruta_dijkstra)} | {esc_dijk} escala(s) | {dist_dijk} km")

                    if ruta_bfs == ruta_dijkstra:
                        print("\n✔ Las rutas COINCIDEN.")
                    else:
                        print("\n✘ Las rutas NO COINCIDEN:")
                        print(f"  • BFS prioriza menos escalas: {esc_bfs} escala(s) recorriendo {dist_bfs} km.")
                        print(f"  • Dijkstra ahorra {dist_bfs - dist_dijk} km realizando {esc_dijk - esc_bfs} escala(s) más.")

            input("\nPresione Enter para continuar...")

        # --------------------------------------------------------------------
        # 5. GRAFICAR GRAFO
        # --------------------------------------------------------------------
        elif opcion == "5":
            print("\n--- GRÁFICA DEL GRAFO ---")
            grafo_activo = elegir_red(grafo)
            graficar_grafo(grafo_activo)
            input("\nPresione Enter para continuar...")

        # --------------------------------------------------------------------
        # 0. SALIR
        # --------------------------------------------------------------------
        elif opcion == "0":
            print("\nSaliendo del sistema de rutas viales. ¡Hasta pronto!")
            break

        else:
            print("\n[Error] Opción no válida. Por favor, seleccione un número del menú.")


if __name__ == "__main__":
    main()
