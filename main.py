from funciones.crud import agregar_pokemon, mostrar_todos, buscar_pokemon, editar_pokemon, borrar_pokemon, estadisticas
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
                buscar_pokemon()
            case 4:
                editar_pokemon()  # ✅ Llama a la función del CRUD, no a la de persistencia
            case 5:
                borrar_pokemon()
            case 6:
                estadisticas()
            case 7:
                print("\n👋 Gracias por usar la Pokédex. ¡Hasta pronto!")
                break
            case _:
                print("❌ Opción inválida, intenta de nuevo.\n")

if __name__ == "__main__":
    main()