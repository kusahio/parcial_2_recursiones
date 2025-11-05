import requests
import os
from api.api_pokemon import obtener_pokemon
from .persistencia import guardar_pokemon, existe_pokemon_en_csv

# Rangos de Pokémon por generación (según PokéAPI)
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
    """
    Devuelve una lista de nombres de Pokémon desde la PokéAPI.
    
    Args:
        limit: Cantidad de pokémon a obtener
        offset: Posición inicial
        
    Returns:
        list: Lista de nombres de pokémon o lista vacía si hay error
    """
    try:
        # Validar que limit y offset sean números
        if not isinstance(limit, int) or not isinstance(offset, int):
            print("AVISO: Limit y offset deben ser números enteros")
            return []
        
        # Validar que sean positivos
        if limit < 0 or offset < 0:
            print("AVISO: Limit y offset deben ser positivos")
            return []
        
        # Validar límites razonables
        if limit > 1000:
            print("AVISO: Limit muy grande, limitando a 1000")
            limit = 1000
        
        url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
        
        # Realizar petición con timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Validar estructura de respuesta
        if not isinstance(data, dict):
            print("AVISO: Respuesta de la API con formato inválido")
            return []
        
        if "results" not in data:
            print("AVISO: Respuesta sin campo 'results'")
            return []
        
        if not isinstance(data["results"], list):
            print("AVISO: Campo 'results' no es una lista")
            return []
        
        # Extraer nombres con validación
        nombres = []
        for p in data["results"]:
            try:
                if isinstance(p, dict) and "name" in p:
                    nombre = p["name"]
                    if isinstance(nombre, str) and nombre.strip():
                        nombres.append(nombre)
            except Exception:
                continue
        
        return nombres
        
    except requests.exceptions.Timeout:
        print("AVISO: Timeout al obtener lista de Pokémon")
        return []
    except requests.exceptions.ConnectionError:
        print("AVISO: Error de conexión al obtener lista de Pokémon")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"AVISO: Error HTTP al obtener lista: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"AVISO: Error en la petición: {e}")
        return []
    except (ValueError, KeyError) as e:
        print(f"AVISO: Error al procesar respuesta: {e}")
        return []
    except Exception as e:
        print(f"AVISO: Error inesperado al obtener lista: {e}")
        return []


def verificar_si_ya_existe_precarga(base_dir="pokedex"):
    """
    Verifica si ya existe al menos un archivo CSV en la estructura.
    Si existe, asume que la precarga ya se realizó.
    
    Args:
        base_dir: Directorio base de la pokédex
        
    Returns:
        bool: True si ya existe precarga, False en caso contrario
    """
    try:
        # Validar que base_dir sea un string
        if not isinstance(base_dir, str):
            return False
        
        # Validar que no esté vacío
        if not base_dir or not base_dir.strip():
            return False
        
        if not os.path.exists(base_dir):
            return False
        
        # Validar que sea un directorio
        if not os.path.isdir(base_dir):
            return False
        
        # Buscar recursivamente cualquier archivo .csv
        try:
            for root, dirs, files in os.walk(base_dir):
                # Validar que files sea iterable
                if not isinstance(files, list):
                    continue
                
                for file in files:
                    try:
                        if isinstance(file, str) and file.endswith(".csv"):
                            return True
                    except Exception:
                        continue
        except OSError as e:
            print(f"AVISO: Error al recorrer directorios: {e}")
            return False
        
        return False
        
    except Exception as e:
        print(f"AVISO: Error al verificar precarga: {e}")
        return False


def precargar_pokemon():
    """
    Carga automáticamente Pokémon por generación SOLO si no existe ningún CSV.
    Muestra solo un resumen por generación.
    """
    try:
        base_dir = "pokedex"
        
        # Verificar si ya existe precarga
        if verificar_si_ya_existe_precarga(base_dir):
            print("\nAVISO: Ya tienes datos en tu Pokédex. Cancelando carga inicial\n")
            return
        
        print("\nAVISO: Importando tus registros de Pokémon a la Pokédex...")
        
        # Crear directorio base si no existe
        try:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
        except OSError as e:
            print(f"AVISO: No se pudo crear directorio {base_dir}: {e}")
            return
        
        # Validar que GENERACIONES sea un diccionario
        if not isinstance(GENERACIONES, dict):
            print("AVISO: Configuración de generaciones inválida")
            return
        
        resumen = {}
        
        for gen, datos in GENERACIONES.items():
            try:
                # Validar estructura de datos de generación
                if not isinstance(datos, dict):
                    print(f"AVISO: Datos inválidos para {gen}")
                    continue
                
                if "offset" not in datos or "limit" not in datos:
                    print(f"AVISO: Faltan campos en {gen}")
                    continue
                
                nuevos = 0
                existentes = 0
                
                # Validar offset y limit
                offset = datos.get("offset", 0)
                limit = datos.get("limit", 5)
                
                if not isinstance(offset, int) or not isinstance(limit, int):
                    print(f"AVISO: Valores numéricos inválidos en {gen}")
                    continue
                
                # Tomar solo los primeros 5 para no sobrecargar
                nombres = obtener_lista_pokemon(min(5, limit), offset)
                
                if not nombres:
                    print(f"\nAVISO: No se pudieron obtener Pokémon de {gen}.")
                    continue
                
                # Validar que nombres sea una lista
                if not isinstance(nombres, list):
                    continue
                
                for nombre in nombres:
                    try:
                        # Validar que nombre sea string
                        if not isinstance(nombre, str) or not nombre.strip():
                            continue
                        
                        pokemon = obtener_pokemon(nombre)
                        
                        if not pokemon:
                            continue
                        
                        # Validar que pokemon sea un diccionario
                        if not isinstance(pokemon, dict):
                            continue
                        
                        # Validar campos requeridos
                        if "generacion" not in pokemon or "tipo" not in pokemon:
                            continue
                        
                        path = os.path.join(base_dir, pokemon["generacion"], pokemon["tipo"])
                        archivo = os.path.join(path, "pokemon.csv")
                        
                        if existe_pokemon_en_csv(nombre, archivo):
                            existentes += 1
                        else:
                            guardar_pokemon(pokemon)
                            nuevos += 1
                            
                    except KeyboardInterrupt:
                        print("\nAVISO: Precarga cancelada por el usuario")
                        return
                    except Exception as e:
                        # Continuar con el siguiente pokémon si hay error
                        continue
                
                resumen[gen] = {"nuevos": nuevos, "existentes": existentes}
                
            except Exception as e:
                print(f"AVISO: Error al procesar {gen}: {e}")
                continue
        
        # Mostrar resumen
        if resumen:
            print("\nAVISO: Transferencia de datos a la Pokédex completada:\n")
            for gen, datos in resumen.items():
                try:
                    nuevos = datos.get("nuevos", 0)
                    print(f"{gen}: {nuevos} registros agregados a la Pokédex.")
                except Exception:
                    continue
            print()
        else:
            print("\nAVISO: No se pudieron cargar datos iniciales\n")
            
    except KeyboardInterrupt:
        print("\n\nAVISO: Precarga cancelada por el usuario")
    except Exception as e:
        print(f"AVISO: Error inesperado en precarga: {e}")