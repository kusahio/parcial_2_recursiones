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
    """
    # Construir ruta según jerarquía
    path = os.path.join(base_dir, pokemon["generacion"], pokemon["tipo"])
    os.makedirs(path, exist_ok=True)

    archivo = os.path.join(path, "pokemon.csv")

    # Verificar si ya existe el Pokémon
    if existe_pokemon_en_csv(pokemon["nombre"], archivo):
        print(f"{pokemon['nombre']} ya existe en {archivo}. No se duplicará.")
        return

    # Escribir o crear CSV
    with open(archivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(pokemon)

    print(f"\nPokémon agregado correctamente:")
    print(f"Archivo: {archivo}")
    print(f"Datos guardados:")
    for campo in CAMPOS:
        print(f"  {campo}: {pokemon.get(campo, '—')}")
    print("-" * 40)


def existe_pokemon_en_csv(nombre, archivo):
    """Verifica si un Pokémon ya existe en el CSV."""
    if not os.path.exists(archivo):
        return False

    with open(archivo, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["nombre"].lower() == nombre.lower():
                return True
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
    datos = []

    for elemento in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, elemento)

        if os.path.isdir(ruta_completa):
            # Paso recursivo: explorar subdirectorio
            datos.extend(leer_recursivo(ruta_completa))
        elif ruta_completa.endswith(".csv"):
            # Caso base: leer archivo CSV
            with open(ruta_completa, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                datos.extend(list(reader))

    return datos


def buscar_y_modificar_recursivo(ruta, nombre, campo, nuevo_valor):
    """
    Busca y modifica un Pokémon de forma recursiva en la estructura de directorios.
    REEMPLAZA os.walk() completamente.
    
    Recursión:
        - Caso base: Si es archivo CSV, busca y modifica el Pokémon
        - Paso recursivo: Si es directorio, explora cada elemento
    
    Args:
        ruta: Directorio actual a explorar
        nombre: Nombre del Pokémon a modificar
        campo: Campo a modificar
        nuevo_valor: Nuevo valor para el campo
    
    Returns:
        bool: True si se modificó exitosamente
    """
    # Caso base: ruta no existe
    if not os.path.exists(ruta):
        return False
    
    # Caso base: es un archivo CSV
    if os.path.isfile(ruta) and ruta.endswith(".csv"):
        with open(ruta, newline="", encoding="utf-8") as f:
            data = list(csv.DictReader(f))
        
        modificado = False
        for d in data:
            if d["nombre"].lower() == nombre.lower():
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
    
    # Paso recursivo: explorar subdirectorios
    if os.path.isdir(ruta):
        try:
            elementos = os.listdir(ruta)
        except PermissionError:
            return False
        
        for elemento in elementos:
            ruta_completa = os.path.join(ruta, elemento)
            if buscar_y_modificar_recursivo(ruta_completa, nombre, campo, nuevo_valor):
                return True
    
    return False


# UPDATE
def modificar_pokemon(nombre, campo, nuevo_valor, ruta_base="pokedex"):
    """
    Modifica un campo de un Pokémon específico usando recursión.
    """
    if buscar_y_modificar_recursivo(ruta_base, nombre, campo, nuevo_valor):
        return True
    
    print("Pokémon no encontrado.")
    return False


def eliminar_pokemon_recursivo(ruta, nombre):
    """
    Elimina un Pokémon de forma recursiva en la estructura de directorios.
    
    Recursión:
        - Caso base: Si es archivo CSV, busca y elimina el Pokémon
        - Paso recursivo: Si es directorio, explora cada elemento
    
    Args:
        ruta: Directorio actual a explorar
        nombre: Nombre del Pokémon a eliminar
    
    Returns:
        bool: True si se eliminó exitosamente
    """
    # Caso base: ruta no existe
    if not os.path.exists(ruta):
        return False
    
    # Caso base: es un archivo CSV
    if os.path.isfile(ruta) and ruta.endswith(".csv"):
        with open(ruta, newline="", encoding="utf-8") as f:
            data = list(csv.DictReader(f))
        
        nueva_lista = [d for d in data if d["nombre"].lower() != nombre.lower()]
        
        if len(nueva_lista) != len(data):
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CAMPOS)
                writer.writeheader()
                writer.writerows(nueva_lista)
            
            print(f"Pokémon {nombre.capitalize()} eliminado de {ruta}")
            return True
        
        return False
    
    # Paso recursivo: explorar subdirectorios
    if os.path.isdir(ruta):
        try:
            elementos = os.listdir(ruta)
        except PermissionError:
            return False
        
        for elemento in elementos:
            ruta_completa = os.path.join(ruta, elemento)
            if eliminar_pokemon_recursivo(ruta_completa, nombre):
                return True
    
    return False


# DELETE
def eliminar_pokemon(nombre, ruta="pokedex"):
    """
    Elimina un Pokémon recorriendo recursivamente las carpetas.
    Reemplaza completamente el uso de os.walk().
    """
    return eliminar_pokemon_recursivo(ruta, nombre)