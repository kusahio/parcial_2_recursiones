import os
from .persistencia import leer_recursivo


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
    
    # Verificar que exista la Pokédex
    if not os.path.exists("pokedex"):
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
    Muestra los resultados de búsqueda por similitud de forma visual.
    
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
    
    # Mostrar encabezado
    print("\n" + "="*80)
    print(f"📋 RESULTADOS DE BÚSQUEDA: '{termino_busqueda.upper()}'")
    print("="*80)
    print(f"✅ Se encontraron {len(resultados)} coincidencia(s)\n")
    
    # Mostrar cada resultado
    for i, (pokemon, similitud) in enumerate(resultados, 1):
        # Crear barra de similitud visual
        barras_llenas = int(similitud / 10)
        barras_vacias = 10 - barras_llenas
        barra_visual = "█" * barras_llenas + "░" * barras_vacias
        
        # Determinar color/emoji según similitud
        if similitud >= 90:
            emoji = "🎯"
        elif similitud >= 75:
            emoji = "✅"
        elif similitud >= 60:
            emoji = "🔍"
        else:
            emoji = "❓"
        
        # Mostrar información del Pokémon
        print(f"{i}. {emoji} {pokemon['nombre'].upper()} [{similitud:.1f}% similitud]")
        print(f"   {barra_visual} {similitud:.1f}%")
        print(f"   ├─ ID: #{pokemon.get('id', 'N/A')}")
        print(f"   ├─ Tipo: {pokemon['tipo'].capitalize()}")
        print(f"   ├─ Generación: {pokemon['generacion']}")
        print(f"   ├─ Peso: {pokemon['peso']} | Altura: {pokemon['altura']}")
        print(f"   ├─ Experiencia base: {pokemon.get('base_experience', 'N/A')}")
        
        if pokemon.get('habilidades'):
            habilidades = pokemon['habilidades']
            print(f"   └─ Habilidades: {habilidades}")
        else:
            print(f"   └─ Habilidades: N/A")
        
        print()  # Línea en blanco entre resultados
    
    # Mostrar resumen final
    print("="*80)
    print(f"📊 Total de coincidencias: {len(resultados)}")
    print(f"🎯 Mejor coincidencia: {resultados[0][0]['nombre'].capitalize()} ({resultados[0][1]:.1f}%)")
    print("="*80 + "\n")