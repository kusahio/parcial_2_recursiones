import os
from .persistencia import leer_recursivo
from .paginador import paginar_pokemon


def calcular_similitud(str1, str2):
    """
    Calcula la similitud entre dos strings usando el algoritmo de Levenshtein.
    
    Args:
        str1: Primera cadena
        str2: Segunda cadena
    
    Returns:
        float: Porcentaje de similitud (0-100)
    """
    str1, str2 = str1.lower(), str2.lower()
    
    # Si una cadena está contenida en la otra, alta similitud
    if str1 in str2 or str2 in str1:
        return 90
    
    # Algoritmo de distancia de Levenshtein
    if len(str1) < len(str2):
        str1, str2 = str2, str1
    
    if len(str2) == 0:
        return 0
    
    # Crear matriz de distancias
    previous_row = range(len(str2) + 1)
    for i, c1 in enumerate(str1):
        current_row = [i + 1]
        for j, c2 in enumerate(str2):
            # Calcular costo de operaciones
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    # Convertir distancia a porcentaje de similitud
    distancia = previous_row[-1]
    max_len = max(len(str1), len(str2))
    similitud = ((max_len - distancia) / max_len) * 100
    
    return similitud


def buscar_csv_recursivo(ruta):
    """
    Busca archivos CSV de forma recursiva en una estructura de directorios.
    
    Args:
        ruta: Directorio raíz desde donde buscar
    
    Returns:
        bool: True si encuentra al menos un archivo CSV
    """
    # Caso base: si la ruta no existe
    if not os.path.exists(ruta):
        return False
    
    # Verificar si es un archivo
    if os.path.isfile(ruta):
        return ruta.endswith('.csv')
    
    # Paso recursivo: explorar subdirectorios
    try:
        elementos = os.listdir(ruta)
    except PermissionError:
        return False
    
    for elemento in elementos:
        ruta_completa = os.path.join(ruta, elemento)
        
        # Si es un archivo CSV, retornar True
        if os.path.isfile(ruta_completa) and elemento.endswith('.csv'):
            return True
        
        # Si es un directorio, buscar recursivamente
        if os.path.isdir(ruta_completa):
            if buscar_csv_recursivo(ruta_completa):
                return True
    
    return False


def buscar_pokemon_por_similitud(termino_busqueda, umbral_similitud=60):
    """
    Busca Pokémon por similitud de nombre.
    
    Args:
        termino_busqueda: String a buscar (mínimo 3 caracteres)
        umbral_similitud: Porcentaje mínimo de similitud (default: 60)
    
    Returns:
        list: Lista de tuplas (pokemon_dict, porcentaje_similitud) ordenadas por similitud
    """
    # Validar longitud mínima
    if len(termino_busqueda) < 3:
        print("❌ Debes ingresar al menos 3 caracteres para buscar.\n")
        return []
    
    # Verificar que exista la Pokédex usando función recursiva
    if not buscar_csv_recursivo("pokedex"):
        print("📭 No hay datos en la Pokédex.\n")
        return []
    
    # Leer todos los Pokémon
    datos = leer_recursivo("pokedex")
    if not datos:
        print("📭 No hay Pokémon guardados.\n")
        return []
    
    # Calcular similitud para cada Pokémon
    resultados = []
    for pokemon in datos:
        nombre = pokemon.get("nombre", "")
        similitud = calcular_similitud(termino_busqueda, nombre)
        
        # Solo incluir si cumple el umbral
        if similitud >= umbral_similitud:
            resultados.append((pokemon, similitud))
    
    # Ordenar por similitud descendente (mayor similitud primero)
    resultados.sort(key=lambda x: x[1], reverse=True)
    
    return resultados


def mostrar_resultados_busqueda(termino_busqueda, umbral=60):
    """
    Muestra los resultados de búsqueda por similitud con paginación.
    
    Args:
        termino_busqueda: Término a buscar
        umbral: Umbral de similitud mínima (default: 60)
    """
    print(f"\n🔍 Buscando Pokémon similares a '{termino_busqueda}'...")
    
    # Obtener resultados
    resultados = buscar_pokemon_por_similitud(termino_busqueda, umbral)
    
    # Si no hay resultados
    if not resultados:
        print(f"\n❌ No se encontraron Pokémon similares a '{termino_busqueda}'.")
        print("💡 Intenta con:")
        print("   • Otro término de búsqueda")
        print("   • Al menos 3 caracteres")
        print("   • Verificar la ortografía\n")
        return
    
    # Extraer solo los pokémon (sin el porcentaje de similitud)
    pokemon_list = [pokemon for pokemon, similitud in resultados]
    
    # Mostrar con paginador
    paginar_pokemon(
        resultados=pokemon_list,
        pokemon_por_pagina=10,
        titulo=f"🔍 RESULTADOS DE BÚSQUEDA: '{termino_busqueda.upper()}'\n{len(resultados)} coincidencia(s) encontrada(s)",
        tipo_formato='completo'
    )