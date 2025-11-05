import requests
from typing import Optional, Dict, Any

def obtener_generacion_pokemon(pokemon_data: Dict[str, Any]) -> str:
    """
    Obtiene la generación del Pokémon desde la species URL.
    
    Args:
        pokemon_data: Diccionario con los datos del Pokémon
        
    Returns:
        str: Nombre de la generación o "unknown" si no se puede obtener
    """
    try:
        # Validar que pokemon_data no sea None o vacío
        if not pokemon_data:
            print("  [Advertencia] Datos del Pokémon vacíos")
            return "unknown"
        
        # Validar que existe la estructura species
        if "species" not in pokemon_data:
            print("  [Advertencia] No se encontró información de especies")
            return "unknown"
        
        species_url = pokemon_data.get("species", {}).get("url")
        
        # Validar que la URL existe y es válida
        if not species_url or not isinstance(species_url, str):
            print("  [Advertencia] URL de especies no válida")
            return "unknown"
        
        # Realizar petición con timeout
        response = requests.get(species_url, timeout=10)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        
        species_data = response.json()
        
        # Validar estructura de la respuesta
        if not isinstance(species_data, dict):
            print("  [Advertencia] Respuesta de especies con formato inválido")
            return "unknown"
        
        generation = species_data.get("generation", {}).get("name", "unknown")
        
        # Validar que la generación es un string
        if not isinstance(generation, str):
            return "unknown"
        
        return generation
        
    except requests.exceptions.Timeout:
        print("  [Error] Timeout al obtener información de la generación")
        return "unknown"
    except requests.exceptions.ConnectionError:
        print("  [Error] Error de conexión al obtener la generación")
        return "unknown"
    except requests.exceptions.HTTPError as e:
        print(f"  [Error] Error HTTP al obtener la generación: {e}")
        return "unknown"
    except requests.exceptions.RequestException as e:
        print(f"  [Error] Error en la petición de generación: {e}")
        return "unknown"
    except (ValueError, KeyError) as e:
        print(f"  [Error] Error al procesar datos de generación: {e}")
        return "unknown"
    except Exception as e:
        print(f"  [Error] Error inesperado al obtener generación: {e}")
        return "unknown"


def obtener_pokemon(nombre: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene los datos del Pokémon desde la PokéAPI.
    Detecta automáticamente la generación.
    
    Args:
        nombre: Nombre o ID del Pokémon a buscar
        
    Returns:
        Dict con los datos del Pokémon o None si no se encuentra/hay error
    """
    try:
        # Validar que el nombre no esté vacío
        if not nombre or not isinstance(nombre, str):
            print("[Error] El nombre del Pokémon no puede estar vacío")
            return None
        
        # Limpiar y validar el nombre
        nombre = nombre.strip()
        if not nombre:
            print("[Error] El nombre del Pokémon no puede estar vacío")
            return None
        
        # Validar longitud razonable del nombre
        if len(nombre) > 50:
            print("[Error] El nombre del Pokémon es demasiado largo")
            return None
        
        # Construir URL
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
        
        # Realizar petición con timeout
        response = requests.get(url, timeout=10)
        
        # Verificar el código de estado
        if response.status_code == 404:
            print(f"[Error] No se encontró el Pokémon '{nombre}' en la PokéAPI")
            return None
        
        response.raise_for_status()  # Lanza excepción para otros errores HTTP
        
        # Parsear JSON
        data = response.json()
        
        # Validar que la respuesta tiene la estructura esperada
        if not isinstance(data, dict):
            print("[Error] Respuesta de la API con formato inválido")
            return None
        
        # Validar campos obligatorios
        campos_requeridos = ["id", "name", "types", "height", "weight", "abilities"]
        campos_faltantes = [campo for campo in campos_requeridos if campo not in data]
        
        if campos_faltantes:
            print(f"[Error] Faltan campos en la respuesta: {', '.join(campos_faltantes)}")
            return None
        
        # Validar que types no esté vacío
        if not data["types"] or not isinstance(data["types"], list):
            print("[Error] El Pokémon no tiene tipos definidos")
            return None
        
        # Obtener tipo principal con validación
        try:
            tipo = data["types"][0]["type"]["name"]
            if not isinstance(tipo, str):
                tipo = "unknown"
        except (KeyError, IndexError, TypeError):
            print("  [Advertencia] No se pudo obtener el tipo, usando 'unknown'")
            tipo = "unknown"
        
        # Obtener generación automáticamente
        generacion = obtener_generacion_pokemon(data)
        
        # Validar y convertir valores numéricos
        try:
            pokemon_id = int(data["id"])
            altura = int(data["height"])
            peso = int(data["weight"])
        except (ValueError, TypeError) as e:
            print(f"[Error] Error al convertir valores numéricos: {e}")
            return None
        
        # Validar valores numéricos positivos
        if pokemon_id <= 0 or altura < 0 or peso < 0:
            print("[Error] Los valores numéricos deben ser positivos")
            return None
        
        # Obtener base_experience con validación
        try:
            base_experience = int(data.get("base_experience", 0))
            if base_experience < 0:
                base_experience = 0
        except (ValueError, TypeError):
            print("  [Advertencia] Base experience inválida, usando 0")
            base_experience = 0
        
        # Obtener habilidades con validación
        try:
            if isinstance(data["abilities"], list) and data["abilities"]:
                habilidades = ", ".join([
                    h["ability"]["name"] 
                    for h in data["abilities"] 
                    if isinstance(h, dict) and "ability" in h and "name" in h["ability"]
                ])
                if not habilidades:
                    habilidades = "sin habilidades"
            else:
                habilidades = "sin habilidades"
        except (KeyError, TypeError) as e:
            print(f"  [Advertencia] Error al procesar habilidades: {e}")
            habilidades = "sin habilidades"
        
        # Crear diccionario del Pokémon
        pokemon = {
            "id": pokemon_id,
            "nombre": data["name"],
            "tipo": tipo,
            "altura": altura,
            "peso": peso,
            "base_experience": base_experience,
            "habilidades": habilidades,
            "areas_encuentro": "",  # Se puede llenar después si se desea
            "generacion": generacion
        }
        
        print("\n✓ Pokémon agregado a la Pokédex correctamente:")
        for k, v in pokemon.items():
            print(f"  {k.capitalize()}: {v}")
        
        return pokemon
        
    except requests.exceptions.Timeout:
        print(f"[Error] Timeout al buscar el Pokémon '{nombre}'")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[Error] Error de conexión. Verifica tu conexión a internet")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[Error] Error HTTP al buscar el Pokémon: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[Error] Error en la petición: {e}")
        return None
    except (ValueError, KeyError, TypeError) as e:
        print(f"[Error] Error al procesar los datos del Pokémon: {e}")
        return None
    except Exception as e:
        print(f"[Error] Error inesperado: {e}")
        return None