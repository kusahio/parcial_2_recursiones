from funciones.crud import agregar_pokemon, mostrar_todos, modificar_pokemon, eliminar_pokemon, estadisticas
from funciones.carga_automatica import precargar_pokemon
from funciones.menu import menu
def main():
    # Precarga automática al iniciar
    precargar_pokemon()

    while True:
        

        opcion = menu()
        opcion_int = int(opcion) if opcion.isdigit() else 0

        match opcion_int:
            case 1:
                agregar_pokemon()
            case 2:
                mostrar_todos()
            case 3:
                modificar_pokemon()
            case 4:
                nombre = input("Nombre del Pokémon a eliminar: ")
                if not eliminar_pokemon(nombre):
                    print("❌ Pokémon no encontrado.\n")
            case 5:
                estadisticas()
            case 6:
                print("Cerrando Pokédex...")
                break
            case _:
                print("❌ Opción inválida, intenta de nuevo.\n")

if __name__ == "__main__":
    main()