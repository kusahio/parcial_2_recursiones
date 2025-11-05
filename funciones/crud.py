import os
from .persistencia import guardar_pokemon, leer_recursivo, modificar_pokemon, eliminar_pokemon
from api.api_pokemon import obtener_pokemon
from .carga_automatica import precargar_pokemon


# CREATE
def agregar_pokemon():
    nombre = input("Nombre del Pokémon: ").lower()
    generacion = input("Generación (ej. generation-i): ").lower()

    pokemon = obtener_pokemon(nombre, generacion)
    if pokemon:
        guardar_pokemon(pokemon)
        print(f"\n{nombre.capitalize()} agregado correctamente.\n")


# READ
def mostrar_todos():
    if not os.path.exists("pokedex"):
        print("No hay datos aún.")
        return

    datos = leer_recursivo("pokedex")
    if not datos:
        print("No hay Pokémon guardados.")
        return

    print("\nLista global de Pokémon:")
    for d in datos:
        print(f"- {d['nombre']} | Tipo: {d['tipo']} | Gen: {d['generacion']} | Peso: {d['peso']} | Habilidades: {d['habilidades']}")

    print(f"\nTotal: {len(datos)} Pokémon cargados.\n")


# UPDATE
def editar_pokemon():
    nombre = input("Nombre del Pokémon a modificar: ").lower()
    campo = input("Campo a modificar (peso, altura, habilidades, areas_encuentro): ").lower()
    nuevo_valor = input("Nuevo valor: ")
    modificar_pokemon(nombre, campo, nuevo_valor)


# DELETE
def borrar_pokemon():
    nombre = input("Nombre del Pokémon a eliminar: ").lower()
    if not eliminar_pokemon(nombre):
        print("Pokémon no encontrado.\n")


# 📊 ESTADÍSTICAS
def estadisticas():
    if not os.path.exists("pokedex"):
        print("No hay datos registrados.")
        return

    datos = leer_recursivo("pokedex")
    if not datos:
        print("No hay Pokémon guardados.")
        return

    total = len(datos)
    promedio_peso = sum(float(p["peso"]) for p in datos if p["peso"].isdigit()) / total
    promedio_altura = sum(float(p["altura"]) for p in datos if p["altura"].isdigit()) / total

    print(f"\nEstadísticas globales:")
    print(f"- Total Pokémon: {total}")
    print(f"- Peso promedio: {promedio_peso:.2f}")
    print(f"- Altura promedio: {promedio_altura:.2f}\n")


# CARGA AUTOMÁTICA AL INICIO
def iniciar_sistema():
    precargar_pokemon()