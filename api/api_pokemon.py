import requests

def obtener_generacion_pokemon(pokemon_data):
    """
    Obtiene la generación del Pokémon desde la species URL.
    """
    species_url = pokemon_data.get("species", {}).get("url")
    if not species_url:
        return "unknown"
    
    try:
        response = requests.get(species_url)
        if response.status_code == 200:
            species_data = response.json()
            generation = species_data.get("generation", {}).get("name", "unknown")
            return generation
    except:
        return "unknown"
    
    return "unknown"

def obtener_pokemon(nombre):
    """
    Obtiene los datos del Pokémon desde la PokéAPI.
    Detecta automáticamente la generación.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tipo = data["types"][0]["type"]["name"]
        
        # Obtener generación automáticamente
        generacion = obtener_generacion_pokemon(data)

        pokemon = {
            "id": data["id"],
            "nombre": data["name"],
            "tipo": tipo,
            "altura": data["height"],
            "peso": data["weight"],
            "base_experience": data["base_experience"],
            "habilidades": ", ".join([h["ability"]["name"] for h in data["abilities"]]),
            "areas_encuentro": "",  # Se puede llenar después si se desea
            "generacion": generacion
        }

        print("\nPokémon agregado a la Pokédex correctamente:")
        for k, v in pokemon.items():
            print(f"  {k.capitalize()}: {v}")

        return pokemon
    else:
        print(f"No se encontró el Pokémon '{nombre}' en la PokéAPI.")
        return None