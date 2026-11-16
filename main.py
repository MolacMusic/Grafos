"""
Realizado por: Alan Peñafiel

Programa principal para la gestión y análisis de rutas viales en Ecuador.
Algoritmos y Estructuras de Datos - Unidad 3: Grafos.
"""

from utilidades import GRAFO_ECUADOR, mostrar_grafo, grado

##Función de Mostrar Menú en Consola
def mostrar_menu():
    """Muestra el menú principal de opciones en la consola."""
    print("\n" + "=" * 60)
    print("      SISTEMA DE RUTAS VIALES DEL ECUADOR")
    print("=" * 60)
    print("1. Mostrar grafo y grados de las ciudades")
    print("2. [Aún sin implementar] (BFS)")
    print("3. [Aún sin implementar] (Dijkstra)")
    print("4. [Aún sin implementar] conectividad")
    print("0. Salir")
    print("-" * 60)

##Función Principal y Bucle Interactivo
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

        elif opcion in ("2", "3", "4"):
            print("\n[!] Esta opción estará disponible próximamente en las siguientes entregas.")
            input("\nPresione Enter para continuar...")

        elif opcion == "0":
            print("\nSaliendo del sistema. ¡Hasta pronto!")
            break

        else:
            print("\n[Error] Opción no válida. Por favor, ingrese un número del menú.")


if __name__ == "__main__":
    main()
