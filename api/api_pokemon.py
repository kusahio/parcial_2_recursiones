import requests

def obtener_pokemon(nombre, generacion):
    """Obtiene los datos del Pokémon desde la PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tipo = data["types"][0]["type"]["name"]

        pokemon = {
            "generacion": generacion,
            "tipo": tipo,
            "nombre": data["name"],
            "altura": data["height"],
            "peso": data["weight"],
            "base_experience": data["base_experience"]
        }

        print("\n✅ Pokémon obtenido correctamente:")
        for k, v in pokemon.items():
            print(f"  {k.capitalize()}: {v}")

        return pokemon
    else:
        print("No se encontró ese Pokémon en la PokéAPI.")
        return None