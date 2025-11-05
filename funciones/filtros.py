import os
from .persistencia import leer_recursivo


def filtrar_por_criterio_recursivo(datos, criterio, valor):
    """
    Filtra una lista de Pokémon de forma recursiva basándose en un criterio.
    
    Recursión:
        - Caso base: Lista vacía retorna lista vacía
        - Paso recursivo: Compara el primer elemento y continúa con el resto
    
    Args:
        datos: Lista de diccionarios de Pokémon
        criterio: Campo por el cual filtrar (ej: "tipo", "generacion")
        valor: Valor que debe cumplir el criterio
    
    Returns:
        list: Lista filtrada de Pokémon
    """
    # Caso base: lista vacía
    if not datos:
        return []
    
    # Tomar primer elemento y el resto
    primero = datos[0]
    resto = datos[1:]
    
    # Verificar si el primer elemento cumple el criterio
    if primero.get(criterio, "").lower() == valor.lower():
        # Incluir el elemento actual y continuar recursivamente
        return [primero] + filtrar_por_criterio_recursivo(resto, criterio, valor)
    else:
        # Omitir el elemento actual y continuar recursivamente
        return filtrar_por_criterio_recursivo(resto, criterio, valor)


def obtener_valores_unicos_recursivo(datos, campo, valores_acumulados=None):
    """
    Obtiene todos los valores únicos de un campo de forma recursiva.
    
    Recursión:
        - Caso base: Lista vacía retorna valores acumulados
        - Paso recursivo: Agrega valor único y continúa con el resto
    
    Args:
        datos: Lista de diccionarios de Pokémon
        campo: Campo del cual extraer valores únicos
        valores_acumulados: Set de valores únicos encontrados (para recursión)
    
    Returns:
        set: Conjunto de valores únicos
    """
    # Inicializar set en primera llamada
    if valores_acumulados is None:
        valores_acumulados = set()
    
    # Caso base: lista vacía
    if not datos:
        return valores_acumulados
    
    # Agregar valor actual al set (automáticamente evita duplicados)
    valor = datos[0].get(campo, "desconocido")
    valores_acumulados.add(valor)
    
    # Paso recursivo: continuar con el resto
    return obtener_valores_unicos_recursivo(datos[1:], campo, valores_acumulados)


def mostrar_pokemon_filtrados(pokemon_lista, titulo_filtro):
    """
    Muestra una lista de Pokémon filtrados con formato visual.
    
    Args:
        pokemon_lista: Lista de Pokémon a mostrar
        titulo_filtro: Título descriptivo del filtro aplicado
    """
    if not pokemon_lista:
        print(f"\n❌ No se encontraron Pokémon con el filtro: {titulo_filtro}\n")
        return
    
    print("\n" + "="*80)
    print(f"🔍 {titulo_filtro.upper()}")
    print("="*80)
    print(f"✅ Se encontraron {len(pokemon_lista)} Pokémon\n")
    
    for i, pokemon in enumerate(pokemon_lista, 1):
        print(f"{i}. {pokemon['nombre'].upper()}")
        print(f"   ├─ ID: #{pokemon.get('id', 'N/A')}")
        print(f"   ├─ Tipo: {pokemon['tipo'].capitalize()}")
        print(f"   ├─ Generación: {pokemon['generacion']}")
        print(f"   ├─ Peso: {pokemon['peso']} | Altura: {pokemon['altura']}")
        print(f"   ├─ Experiencia base: {pokemon.get('base_experience', 'N/A')}")
        
        if pokemon.get('habilidades'):
            print(f"   └─ Habilidades: {pokemon['habilidades']}")
        else:
            print(f"   └─ Habilidades: N/A")
        
        print()
    
    print("="*80)
    print(f"📊 Total de coincidencias: {len(pokemon_lista)}")
    print("="*80 + "\n")


def filtrar_por_generacion():
    """
    Filtra y muestra Pokémon por generación usando recursión.
    """
    if not os.path.exists("pokedex"):
        print("\n📭 No hay datos en la Pokédex.\n")
        return
    
    # Leer todos los Pokémon
    datos = leer_recursivo("pokedex")
    if not datos:
        print("\n📭 No hay Pokémon guardados.\n")
        return
    
    # Obtener generaciones disponibles usando recursión
    generaciones = sorted(obtener_valores_unicos_recursivo(datos, "generacion"))
    
    print("\n" + "="*60)
    print("🌍 FILTRAR POR GENERACIÓN")
    print("="*60)
    print("\n📋 Generaciones disponibles:")
    
    for i, gen in enumerate(generaciones, 1):
        # Contar cuántos Pokémon hay de esta generación
        cantidad = len(filtrar_por_criterio_recursivo(datos, "generacion", gen))
        print(f"  {i}. {gen} ({cantidad} Pokémon)")
    
    print(f"  {len(generaciones) + 1}. Volver al menú principal")
    
    opcion = input("\nSelecciona una generación: ").strip()
    
    if not opcion.isdigit():
        print("\n❌ Opción inválida.\n")
        return
    
    opcion_int = int(opcion)
    
    if opcion_int == len(generaciones) + 1:
        return
    
    if 1 <= opcion_int <= len(generaciones):
        gen_seleccionada = generaciones[opcion_int - 1]
        
        # Filtrar usando recursión
        pokemon_filtrados = filtrar_por_criterio_recursivo(datos, "generacion", gen_seleccionada)
        
        # Mostrar resultados
        mostrar_pokemon_filtrados(
            pokemon_filtrados,
            f"Pokémon de {gen_seleccionada}"
        )
    else:
        print("\n❌ Opción inválida.\n")


def filtrar_por_tipo():
    """
    Filtra y muestra Pokémon por tipo usando recursión.
    """
    if not os.path.exists("pokedex"):
        print("\n📭 No hay datos en la Pokédex.\n")
        return
    
    # Leer todos los Pokémon
    datos = leer_recursivo("pokedex")
    if not datos:
        print("\n📭 No hay Pokémon guardados.\n")
        return
    
    # Obtener tipos disponibles usando recursión
    tipos = sorted(obtener_valores_unicos_recursivo(datos, "tipo"))
    
    print("\n" + "="*60)
    print("🎨 FILTRAR POR TIPO")
    print("="*60)
    print("\n📋 Tipos disponibles:")
    
    for i, tipo in enumerate(tipos, 1):
        # Contar cuántos Pokémon hay de este tipo
        cantidad = len(filtrar_por_criterio_recursivo(datos, "tipo", tipo))
        print(f"  {i}. {tipo.capitalize()} ({cantidad} Pokémon)")
    
    print(f"  {len(tipos) + 1}. Volver al menú principal")
    
    opcion = input("\nSelecciona un tipo: ").strip()
    
    if not opcion.isdigit():
        print("\n❌ Opción inválida.\n")
        return
    
    opcion_int = int(opcion)
    
    if opcion_int == len(tipos) + 1:
        return
    
    if 1 <= opcion_int <= len(tipos):
        tipo_seleccionado = tipos[opcion_int - 1]
        
        # Filtrar usando recursión
        pokemon_filtrados = filtrar_por_criterio_recursivo(datos, "tipo", tipo_seleccionado)
        
        # Mostrar resultados
        mostrar_pokemon_filtrados(
            pokemon_filtrados,
            f"Pokémon de tipo {tipo_seleccionado.capitalize()}"
        )
    else:
        print("\n❌ Opción inválida.\n")