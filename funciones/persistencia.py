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


# READ (Recursivo real)
def leer_recursivo(ruta):
    """
    Lee todos los CSVs de forma recursiva y devuelve una lista de Pokémon.
    Paso recursivo: entra a subcarpetas.
    Caso base: lee los archivos .csv.
    """
    datos = []

    for elemento in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, elemento)

        if os.path.isdir(ruta_completa):
            # Paso recursivo
            datos.extend(leer_recursivo(ruta_completa))
        elif ruta_completa.endswith(".csv"):
            # Caso base
            with open(ruta_completa, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                datos.extend(list(reader))

    return datos


# UPDATE
def modificar_pokemon(nombre, campo, nuevo_valor, ruta_base="pokedex"):
    """
    Modifica un campo de un Pokémon específico.
    """
    for root, _, files in os.walk(ruta_base):
        for file in files:
            if file.endswith(".csv"):
                archivo = os.path.join(root, file)
                with open(archivo, newline="", encoding="utf-8") as f:
                    data = list(csv.DictReader(f))

                modificado = False
                for d in data:
                    if d["nombre"].lower() == nombre.lower():
                        valor_viejo = d.get(campo, "")
                        d[campo] = nuevo_valor
                        modificado = True
                        print(f"\n{nombre.capitalize()} → {campo}: '{valor_viejo}' → '{nuevo_valor}'")

                if modificado:
                    with open(archivo, "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=CAMPOS)
                        writer.writeheader()
                        writer.writerows(data)
                    print(f"✅ {nombre.capitalize()} modificado correctamente en {archivo}")
                    return True
    print("Pokémon no encontrado.")
    return False


# DELETE
def eliminar_pokemon(nombre, ruta="pokedex"):
    """
    Elimina un Pokémon recorriendo recursivamente las carpetas.
    """
    for elemento in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, elemento)

        if os.path.isdir(ruta_completa):
            eliminado = eliminar_pokemon(nombre, ruta_completa)
            if eliminado:
                return True

        elif ruta_completa.endswith(".csv"):
            with open(ruta_completa, newline="", encoding="utf-8") as f:
                data = list(csv.DictReader(f))

            nueva_lista = [d for d in data if d["nombre"].lower() != nombre.lower()]

            if len(nueva_lista) != len(data):
                with open(ruta_completa, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=CAMPOS)
                    writer.writeheader()
                    writer.writerows(nueva_lista)

                print(f"Pokémon {nombre.capitalize()} eliminado de {ruta_completa}")
                return True
    return False