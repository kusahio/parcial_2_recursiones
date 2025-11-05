import os
import csv

# Campos globales que tendrán todos los Pokémon en los CSV
CAMPOS = [
    "id",
    "nombre",
    "tipo",
    "altura",
    "peso",
    "base_experience",
    "habilidades",
    "areas_encuentro",
    "generacion"
]


# CREATE / UPDATE
def guardar_pokemon(pokemon, base_dir="pokedex"):
    """
    Guarda un Pokémon en su CSV correspondiente.
    Si el archivo no existe, lo crea.
    Si el Pokémon ya está, no lo duplica.
    
    Args:
        pokemon: Diccionario con los datos del Pokémon
        base_dir: Directorio base de la pokédex
    """
    try:
        # Validar que pokemon sea un diccionario
        if not isinstance(pokemon, dict):
            print("\nAVISO: Los datos del Pokémon deben ser un diccionario")
            return
        
        # Validar que base_dir sea un string
        if not isinstance(base_dir, str) or not base_dir.strip():
            print("\nAVISO: Directorio base inválido")
            return
        
        # Validar campos requeridos
        campos_requeridos = ["generacion", "tipo", "nombre"]
        for campo in campos_requeridos:
            if campo not in pokemon:
                print(f"\nAVISO: Falta el campo requerido: {campo}")
                return
            if not isinstance(pokemon[campo], str) or not pokemon[campo].strip():
                print(f"\nAVISO: El campo '{campo}' debe ser un texto válido")
                return
        
        # Construir ruta según jerarquía
        path = os.path.join(base_dir, pokemon["generacion"], pokemon["tipo"])
        
        # Crear directorios si no existen
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            print(f"\nAVISO: No se pudo crear el directorio {path}: {e}")
            return

        archivo = os.path.join(path, "pokemon.csv")

        # Verificar si ya existe el Pokémon
        if existe_pokemon_en_csv(pokemon["nombre"], archivo):
            print(f"\nAVISO: {pokemon['nombre']} ya existe en {archivo}. No se duplicará.")
            return

        # Escribir o crear CSV
        try:
            with open(archivo, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CAMPOS)
                
                # Escribir encabezado si el archivo está vacío
                if f.tell() == 0:
                    writer.writeheader()
                
                # Asegurar que todos los campos existan en el diccionario
                pokemon_completo = {campo: pokemon.get(campo, "") for campo in CAMPOS}
                writer.writerow(pokemon_completo)

            print(f"\n✓ Pokémon agregado correctamente:")
            print(f"Archivo: {archivo}")
            print(f"Datos guardados:")
            for campo in CAMPOS:
                valor = pokemon.get(campo, "—")
                print(f"  {campo}: {valor}")
            print("-" * 40)
            
        except IOError as e:
            print(f"\nAVISO: Error al escribir en el archivo {archivo}: {e}")
        except csv.Error as e:
            print(f"\nAVISO: Error de CSV al guardar: {e}")
            
    except Exception as e:
        print(f"\nAVISO: Error inesperado al guardar Pokémon: {e}")


def existe_pokemon_en_csv(nombre, archivo):
    """
    Verifica si un Pokémon ya existe en el CSV.
    
    Args:
        nombre: Nombre del Pokémon a buscar
        archivo: Ruta del archivo CSV
        
    Returns:
        bool: True si existe, False en caso contrario
    """
    try:
        # Validar parámetros
        if not isinstance(nombre, str) or not nombre.strip():
            return False
        
        if not isinstance(archivo, str) or not archivo.strip():
            return False
        
        if not os.path.exists(archivo):
            return False
        
        # Validar que sea un archivo
        if not os.path.isfile(archivo):
            return False

        with open(archivo, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Validar que row sea un diccionario
                if not isinstance(row, dict):
                    continue
                
                nombre_row = row.get("nombre", "")
                
                # Validar y comparar nombres
                if isinstance(nombre_row, str) and nombre_row.lower() == nombre.lower():
                    return True
        
        return False
        
    except IOError as e:
        print(f"\nAVISO: Error al leer archivo {archivo}: {e}")
        return False
    except csv.Error as e:
        print(f"\nAVISO: Error de CSV: {e}")
        return False
    except Exception as e:
        print(f"\nAVISO: Error inesperado al verificar existencia: {e}")
        return False


# READ
def leer_recursivo(ruta):
    """
    Lee todos los CSVs de forma recursiva y devuelve una lista de Pokémon.
    
    Recursión:
        - Caso base: Lee archivos .csv
        - Paso recursivo: Entra a subcarpetas
    
    Args:
        ruta: Directorio raíz desde donde leer
    
    Returns:
        list: Lista de diccionarios con datos de Pokémon
    """
    try:
        # Validar que ruta sea un string
        if not isinstance(ruta, str) or not ruta.strip():
            return []
        
        # Verificar que la ruta existe
        if not os.path.exists(ruta):
            return []
        
        # Verificar que sea un directorio
        if not os.path.isdir(ruta):
            return []
        
        datos = []

        try:
            elementos = os.listdir(ruta)
        except PermissionError:
            print(f"\nAVISO: Sin permisos para acceder a: {ruta}")
            return []
        except OSError as e:
            print(f"\nAVISO: Error al listar {ruta}: {e}")
            return []

        for elemento in elementos:
            try:
                ruta_completa = os.path.join(ruta, elemento)

                if os.path.isdir(ruta_completa):
                    # Paso recursivo: explorar subdirectorio
                    datos.extend(leer_recursivo(ruta_completa))
                    
                elif ruta_completa.endswith(".csv"):
                    # Caso base: leer archivo CSV
                    try:
                        with open(ruta_completa, newline="", encoding="utf-8") as f:
                            reader = csv.DictReader(f)
                            
                            for row in reader:
                                # Validar que row sea un diccionario
                                if isinstance(row, dict):
                                    datos.append(row)
                                    
                    except IOError as e:
                        print(f"\nAVISO: Error al leer {ruta_completa}: {e}")
                    except csv.Error as e:
                        print(f"\nAVISO: Error de CSV en {ruta_completa}: {e}")
                        
            except Exception as e:
                # Continuar con el siguiente elemento si hay error
                continue

        return datos
        
    except RecursionError:
        print("\nAVISO: Límite de recursión alcanzado")
        return []
    except Exception as e:
        print(f"\nAVISO: Error inesperado en lectura recursiva: {e}")
        return []


def buscar_y_modificar_recursivo(ruta, nombre, campo, nuevo_valor):
    """
    Busca y modifica un Pokémon de forma recursiva en la estructura de directorios.
    
    Args:
        ruta: Directorio actual a explorar
        nombre: Nombre del Pokémon a modificar
        campo: Campo a modificar
        nuevo_valor: Nuevo valor para el campo
    
    Returns:
        bool: True si se modificó exitosamente
    """
    try:
        # Validar parámetros
        if not isinstance(ruta, str) or not ruta.strip():
            return False
        
        if not isinstance(nombre, str) or not nombre.strip():
            return False
        
        if not isinstance(campo, str) or not campo.strip():
            return False
        
        # nuevo_valor puede ser cualquier tipo, convertirlo a string
        nuevo_valor = str(nuevo_valor)
        
        # Caso base: ruta no existe
        if not os.path.exists(ruta):
            return False
        
        # Caso base: es un archivo CSV
        if os.path.isfile(ruta) and ruta.endswith(".csv"):
            try:
                with open(ruta, newline="", encoding="utf-8") as f:
                    data = list(csv.DictReader(f))
                
                # Validar que data sea una lista
                if not isinstance(data, list):
                    return False
                
                modificado = False
                for d in data:
                    # Validar que d sea un diccionario
                    if not isinstance(d, dict):
                        continue
                    
                    nombre_pokemon = d.get("nombre", "")
                    
                    if isinstance(nombre_pokemon, str) and nombre_pokemon.lower() == nombre.lower():
                        valor_viejo = d.get(campo, "")
                        d[campo] = nuevo_valor
                        modificado = True
                        print(f"\n{nombre.capitalize()} → {campo}: '{valor_viejo}' → '{nuevo_valor}'")
                
                if modificado:
                    with open(ruta, "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=CAMPOS)
                        writer.writeheader()
                        writer.writerows(data)
                    print(f"{nombre.capitalize()} modificado correctamente en {ruta}")
                    return True
                
                return False
                
            except IOError as e:
                print(f"\nAVISO: Error al acceder al archivo {ruta}: {e}")
                return False
            except csv.Error as e:
                print(f"\nAVISO: Error de CSV en {ruta}: {e}")
                return False
        
        # Paso recursivo: explorar subdirectorios
        if os.path.isdir(ruta):
            try:
                elementos = os.listdir(ruta)
            except PermissionError:
                print(f"\nAVISO: Sin permisos para acceder a: {ruta}")
                return False
            except OSError as e:
                print(f"\nAVISO: Error al listar {ruta}: {e}")
                return False
            
            for elemento in elementos:
                try:
                    ruta_completa = os.path.join(ruta, elemento)
                    if buscar_y_modificar_recursivo(ruta_completa, nombre, campo, nuevo_valor):
                        return True
                except Exception:
                    continue
        
        return False
        
    except RecursionError:
        print("\nAVISO: Límite de recursión alcanzado")
        return False
    except Exception as e:
        print(f"\nAVISO: Error inesperado al modificar: {e}")
        return False


# UPDATE
def modificar_pokemon(nombre, campo, nuevo_valor, ruta_base="pokedex"):
    """
    Modifica un campo de un Pokémon específico usando recursión.
    
    Args:
        nombre: Nombre del Pokémon a modificar
        campo: Campo a modificar
        nuevo_valor: Nuevo valor
        ruta_base: Directorio base de la pokédex
        
    Returns:
        bool: True si se modificó exitosamente
    """
    try:
        # Validar parámetros
        if not isinstance(nombre, str) or not nombre.strip():
            print("\nAVISO: Nombre inválido")
            return False
        
        if not isinstance(campo, str) or not campo.strip():
            print("\nAVISO: Campo inválido")
            return False
        
        if not isinstance(ruta_base, str) or not ruta_base.strip():
            print("\nAVISO: Ruta base inválida")
            return False
        
        if buscar_y_modificar_recursivo(ruta_base, nombre, campo, nuevo_valor):
            return True
        
        print("\nAVISO: Pokémon no encontrado.")
        return False
        
    except Exception as e:
        print(f"\nAVISO: Error inesperado al modificar Pokémon: {e}")
        return False


def eliminar_pokemon_recursivo(ruta, nombre):
    """
    Elimina un Pokémon de forma recursiva en la estructura de directorios.
    
    Args:
        ruta: Directorio actual a explorar
        nombre: Nombre del Pokémon a eliminar
    
    Returns:
        bool: True si se eliminó exitosamente
    """
    try:
        # Validar parámetros
        if not isinstance(ruta, str) or not ruta.strip():
            return False
        
        if not isinstance(nombre, str) or not nombre.strip():
            return False
        
        # Caso base: ruta no existe
        if not os.path.exists(ruta):
            return False
        
        # Caso base: es un archivo CSV
        if os.path.isfile(ruta) and ruta.endswith(".csv"):
            try:
                with open(ruta, newline="", encoding="utf-8") as f:
                    data = list(csv.DictReader(f))
                
                # Validar que data sea una lista
                if not isinstance(data, list):
                    return False
                
                # Filtrar el Pokémon a eliminar
                nueva_lista = []
                for d in data:
                    if isinstance(d, dict):
                        nombre_pokemon = d.get("nombre", "")
                        if isinstance(nombre_pokemon, str) and nombre_pokemon.lower() != nombre.lower():
                            nueva_lista.append(d)
                
                # Si se eliminó algún registro
                if len(nueva_lista) != len(data):
                    with open(ruta, "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=CAMPOS)
                        writer.writeheader()
                        writer.writerows(nueva_lista)
                    
                    print(f"Pokémon {nombre.capitalize()} eliminado de {ruta}")
                    return True
                
                return False
                
            except IOError as e:
                print(f"\nAVISO: Error al acceder al archivo {ruta}: {e}")
                return False
            except csv.Error as e:
                print(f"\nAVISO: Error de CSV en {ruta}: {e}")
                return False
        
        # Paso recursivo: explorar subdirectorios
        if os.path.isdir(ruta):
            try:
                elementos = os.listdir(ruta)
            except PermissionError:
                print(f"\nAVISO: Sin permisos para acceder a: {ruta}")
                return False
            except OSError as e:
                print(f"\nAVISO: Error al listar {ruta}: {e}")
                return False
            
            for elemento in elementos:
                try:
                    ruta_completa = os.path.join(ruta, elemento)
                    if eliminar_pokemon_recursivo(ruta_completa, nombre):
                        return True
                except Exception:
                    continue
        
        return False
        
    except RecursionError:
        print("\nAVISO: Límite de recursión alcanzado")
        return False
    except Exception as e:
        print(f"\nAVISO: Error inesperado al eliminar: {e}")
        return False


# DELETE
def eliminar_pokemon(nombre, ruta="pokedex"):
    """
    Elimina un Pokémon recorriendo recursivamente las carpetas.
    
    Args:
        nombre: Nombre del Pokémon a eliminar
        ruta: Directorio base de la pokédex
        
    Returns:
        bool: True si se eliminó exitosamente
    """
    try:
        # Validar parámetros
        if not isinstance(nombre, str) or not nombre.strip():
            print("\nAVISO: Nombre inválido")
            return False
        
        if not isinstance(ruta, str) or not ruta.strip():
            print("\nAVISO: Ruta inválida")
            return False
        
        return eliminar_pokemon_recursivo(ruta, nombre)
        
    except Exception as e:
        print(f"\nAVISO: Error inesperado al eliminar Pokémon: {e}")
        return False