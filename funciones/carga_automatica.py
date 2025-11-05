import requests
import os
from api.api_pokemon import obtener_pokemon
from .persistencia import guardar_pokemon, existe_pokemon_en_csv

# 🔹 Rangos de Pokémon por generación (según PokéAPI)
GENERACIONES = {
    "generation-i":  {"offset": 0, "limit": 151},      # Bulbasaur → Mew
    "generation-ii": {"offset": 151, "limit": 100},    # Chikorita → Celebi
    "generation-iii": {"offset": 251, "limit": 135},   # Treecko → Deoxys
    "generation-iv": {"offset": 386, "limit": 107},    # Turtwig → Arceus
    "generation-v": {"offset": 493, "limit": 156},     # Victini → Genesect
    "generation-vi": {"offset": 649, "limit": 72},     # Chespin → Volcanion
    "generation-vii": {"offset": 721, "limit": 88},    # Rowlet → Marshadow
    "generation-viii": {"offset": 809, "limit": 96},   # Grookey → Enamorus
    "generation-ix": {"offset": 905, "limit": 120},    # Sprigatito → Terapagos (aprox)
}

def obtener_lista_pokemon(limit, offset):
    """Devuelve una lista de nombres de Pokémon desde la PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [p["name"] for p in data["results"]]
    return []

def precargar_pokemon():
    """
    Carga automáticamente Pokémon por generación si no existen.
    Muestra solo un resumen por generación.
    """
    base_dir = "pokedex"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    print("\nIniciando precarga automática de Pokémon...")
    resumen = {}

    for gen, datos in GENERACIONES.items():
        nuevos = 0
        existentes = 0

        # Tomar solo los primeros 50 para no sobrecargar
        nombres = obtener_lista_pokemon(5, datos["offset"])
        if not nombres:
            print(f"No se pudieron obtener Pokémon de {gen}.")
            continue

        for nombre in nombres:
            pokemon = obtener_pokemon(nombre, gen)
            if not pokemon:
                continue

            path = os.path.join(base_dir, pokemon["generacion"], pokemon["tipo"])
            archivo = os.path.join(path, "pokemon.csv")

            if existe_pokemon_en_csv(nombre, archivo):
                existentes += 1
            else:
                guardar_pokemon(pokemon)
                nuevos += 1

        resumen[gen] = {"nuevos": nuevos, "existentes": existentes}

    print("\nPrecarga completada:\n")
    for gen, datos in resumen.items():
        print(f"📘 {gen}: {datos['nuevos']} nuevos | {datos['existentes']} ya existentes")
    print()