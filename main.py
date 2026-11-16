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
    obtener_grafo_con_aislada
)


## Función de Mostrar Menú en Consola
def mostrar_menu():
    """Muestra el menú principal de opciones en la consola."""
    print("\n" + "=" * 60)
    print("      SISTEMA DE RUTAS VIALES DEL ECUADOR")
    print("=" * 60)
    print("1. Mostrar grafo y grados de las ciudades")
    print("2. Recorrido BFS: escalas y conectividad desde una ciudad")
    print("3. [Aún sin implementar] Ruta más corta en distancia (Dijkstra)")
    print("4. [Aún sin implementar] Comparar rutas (Escalas vs. Distancia)")
    print("0. Salir")
    print("-" * 60)


## Función Principal y Bucle Interactivo
def main():
    """Función principal con el bucle interactivo de consola."""
    # Grafo cargado en memoria como lista de adyacencia
    grafo = GRAFO_ECUADOR

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            # Operación principal: Visualización y grados
            # Complejidad: O(V + E) para mostrar_grafo y O(V) para grado
            mostrar_grafo(grafo)
            grado(grafo)
            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            # R2: Recorrido BFS, escalas y análisis de conectividad
            print("\n--- RECORRIDO BFS Y VERIFICACIÓN DE CONECTIVIDAD ---")
            print("Modalidades de prueba:")
            print("  1. Usar red estándar de Ecuador (7 ciudades)")
            print("  2. Probar con red temporal que incluye una ciudad aislada ('Galápagos')")
            tipo_red = input("Seleccione modalidad (1 o 2) [Enter para 1]: ").strip()

            if tipo_red == "2":
                grafo_activo = obtener_grafo_con_aislada(grafo, "Galápagos")
                print("\n[i] Red temporal con 'Galápagos' (ciudad aislada) activada.")
            else:
                grafo_activo = grafo
                print("\n[i] Red estándar activa (7 ciudades).")

            ciudades_disponibles = list(grafo_activo.keys())
            print(f"Ciudades disponibles: {', '.join(ciudades_disponibles)}")

            # Validación de la ciudad de origen
            while True:
                entrada_origen = input("\nIngrese la ciudad de origen: ").strip()
                origen = next((c for c in grafo_activo if c.lower() == entrada_origen.lower()), None)
                if origen:
                    break
                print(f"[Error] La ciudad '{entrada_origen}' no existe en la red. Intente de nuevo.")

            # BFS: O(V + E)
            escalas, padres = bfs(grafo_activo, origen)

            # Mostrar cada ciudad alcanzable con sus escalas
            print(f"\n--- CIUDADES ALCANZABLES DESDE {origen.upper()} (BFS) ---")
            for ciudad, num_escalas in sorted(escalas.items(), key=lambda item: (item[1], item[0])):
                if num_escalas == 0:
                    print(f"• {ciudad}: {num_escalas} escalas (Punto de origen)")
                elif num_escalas == 1:
                    print(f"• {ciudad}: {num_escalas} escala (Conexión directa)")
                else:
                    print(f"• {ciudad}: {num_escalas} escalas")

            # Verificación de conectividad de la red
            verificar_conectividad(grafo_activo, escalas)

            # Consulta opcional para reconstruir la ruta (útil para verificar R2 y preparar R4)
            consulta_ruta = input("\n¿Desea consultar la ruta con menos escalas hacia algún destino? (s/n) [n]: ").strip().lower()
            if consulta_ruta == "s":
                entrada_dest = input("Ingrese la ciudad de destino: ").strip()
                destino = next((c for c in grafo_activo if c.lower() == entrada_dest.lower()), None)
                if destino and destino in escalas:
                    ruta = reconstruir_ruta(padres, origen, destino)
                    print(f"-> Ruta con menos escalas ({escalas[destino]} escalas): {' -> '.join(ruta)}")
                elif destino and destino not in escalas:
                    print(f"[!] No existe ruta hacia {destino} (ciudad aislada / inalcanzable).")
                else:
                    print(f"[Error] La ciudad destino ingresada no existe.")

            input("\nPresione Enter para continuar...")

        elif opcion in ("3", "4"):
            print("\n[!] Esta opción estará disponible próximamente en las siguientes entregas.")
            input("\nPresione Enter para continuar...")

        elif opcion == "0":
            print("\nSaliendo del sistema. ¡Hasta pronto!")
            break

        else:
            print("\n[Error] Opción no válida. Por favor, ingrese un número del menú.")


if __name__ == "__main__":
    main()
