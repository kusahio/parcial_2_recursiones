import os
from .persistencia import guardar_pokemon, leer_recursivo, modificar_pokemon, eliminar_pokemon
from api.api_pokemon import obtener_pokemon
from .carga_automatica import precargar_pokemon
from .busqueda import mostrar_resultados_busqueda
from .paginador import paginar_pokemon


# CREATE
def agregar_pokemon():
    """
    Agrega un Pokémon a la Pokédex.
    Solo pide el nombre, la generación se detecta automáticamente.
    """
    nombre = input("Nombre del Pokémon: ").strip().lower()
    
    if not nombre:
        print("AVISO: Debes ingresar un nombre válido.\n")
        return
    
    print(f"\nBuscando '{nombre}' en la PokéAPI...")
    
    pokemon = obtener_pokemon(nombre)
    if pokemon:
        guardar_pokemon(pokemon)
        print(f"\n{nombre.capitalize()} agregado correctamente a la Pokédex.")
    else:
        print(f"\nNo se pudo agregar '{nombre}' a la Pokédex. Verifica el nombre e intenta nuevamente.")


# READ
def mostrar_todos():
    """
    Muestra todos los Pokémon guardados en la Pokédex.
    """
    if not os.path.exists("pokedex"):
        print("AVISO: No hay datos aún.\n")
        return

    datos = leer_recursivo("pokedex")
    if not datos:
        print("\nAVISO: No hay registros en la Pokédex.\n")
        return

    # print("\n" + "="*80)
    # print("LISTA DE POKÉMON EN LA POKÉDEX")
    # print("="*80)
    
    # for i, d in enumerate(datos, 1):
    #     print(f"\n{i}. {d['nombre'].upper()}")
    #     print(f"    Tipo: {d['tipo']} | Generación: {d['generacion']}")
    #     print(f"    Peso: {d['peso']} | Altura: {d['altura']}")
    #     print(f"    Experiencia base: {d.get('base_experience', 'N/A')}")
    #     if d.get('habilidades'):
    #         print(f"        Habilidades: {d['habilidades']}")

    # print("\n" + "="*80)
    # print(f"Total: {len(datos)} Pokémon registrados")
    # print("="*80 + "\n")

    paginar_pokemon(
        resultados=datos,
        pokemon_por_pagina=10,
        titulo='LISTA DE POKÉMON EN LA POKÉDEX',
        tipo_formato='completo'
    )

# Buscar
def buscar_pokemon():
    """
    Busca Pokémon por similitud de nombre con un mínimo de 3 caracteres.
    Muestra todas las coincidencias ordenadas por porcentaje de similitud.
    """
    print("\n" + "="*60)
    print("Buscar Pokémon")
    print("="*60)
    
    termino = input("\nIngresa el nombre (mínimo 3 caracteres): ").strip()
    
    if len(termino) < 3:
        print("\nAVISO: Debes ingresar al menos 3 caracteres para realizar la búsqueda.\n")
        return
    
    mostrar_resultados_busqueda(termino)


# UPDATE
def editar_pokemon():
    """
    Modifica un campo específico de un Pokémon existente.
    """
    print("\n" + "="*60)
    print("Modificar registro de Pokémon en la Pokédex")
    print("="*60)
    
    nombre = input("\nNombre del Pokémon a modificar: ").strip().lower()
    
    if not nombre:
        print("\nAVISO: Debes ingresar un nombre válido.\n")
        return
    
    print("\nCampos disponibles a editar:")
    print("  • peso")
    print("  • altura")
    print("  • habilidades")
    print("  • areas_encuentro")
    print("  • base_experience")
    
    campo = input("\nCampo a modificar: ").strip().lower()
    
    # Validar que el campo existe
    campos_validos = ["peso", "altura", "habilidades", "areas_encuentro", "base_experience"]
    if campo not in campos_validos:
        print(f"\nAVISO: Campo '{campo}' no válido. Elige uno de la lista.\n")
        return
    
    nuevo_valor = input("Nuevo valor: ").strip()
    
    if not nuevo_valor:
        print("AVISO: El valor no puede estar vacío.\n")
        return
    
    if modificar_pokemon(nombre, campo, nuevo_valor):
        print(f"\n{nombre.capitalize()} modificado correctamente.\n")
    else:
        print(f"\nAVISO: No se pudo modificar '{nombre}'. Verifica que el Pokémon exista en el registro de la Pokédex.\n")


# DELETE
def borrar_pokemon():
    """
    Elimina un Pokémon de la Pokédex después de confirmar la acción.
    """
    print("\n" + "="*60)
    print("Eliminar registro de Pokémon de la Pokédex")
    print("="*60)
    
    nombre = input("\nNombre del Pokémon a eliminar: ").strip().lower()
    
    if not nombre:
        print("AVISO: Debes ingresar un nombre válido.\n")
        return
    
    confirmacion = input(f"\nAVISO: ¿Estás seguro de eliminar a {nombre.capitalize()}? (s/n): ").lower()
    
    if confirmacion == 's':
        if eliminar_pokemon(nombre):
            print(f"\n{nombre.capitalize()} eliminado correctamente de la Pokédex.\n")
        else:
            print(f"\nAVISO: Pokémon '{nombre}' no encontrado en la Pokédex.\n")
    else:
        print("\nAVISO: Eliminación cancelada.\n")


# Estadísticas
def estadisticas():
    """
    Muestra estadísticas generales de la Pokédex:
    - Total de Pokémon
    - Promedios de peso y altura
    - Distribución por tipo
    - Distribución por generación
    """
    if not os.path.exists("pokedex"):
        print("\nNo hay datos registrados.\n")
        return

    datos = leer_recursivo("pokedex")
    if not datos:
        print("\nNo hay Pokémon guardados.\n")
        return

    total = len(datos)
    
    # Calcular promedios de peso y altura
    pesos = [float(poke["peso"]) for poke in datos if poke.get("peso", "").replace(".", "").isdigit()]
    alturas = [float(poke["altura"]) for poke in datos if poke.get("altura", "").replace(".", "").isdigit()]
    
    promedio_peso = sum(pesos) / len(pesos) if pesos else 0
    promedio_altura = sum(alturas) / len(alturas) if alturas else 0
    
    # Contar por tipo
    tipos = {}
    for p in datos:
        tipo = p.get("tipo", "desconocido")
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    # Contar por generación
    generaciones = {}
    for p in datos:
        gen = p.get("generacion", "desconocida")
        generaciones[gen] = generaciones.get(gen, 0) + 1

    # Mostrar estadísticas
    print("\n" + "="*70)
    print("Registros de la Pokédex")
    print("="*70)
    print(f"\nTotal de Pokémon registrados: {total}")
    print(f"Peso promedio: {promedio_peso:.2f}")
    print(f"Altura promedio: {promedio_altura:.2f}")
    
    print("\nDistribución por tipo:")
    for tipo, cantidad in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (cantidad / total) * 100
        #barra = "█" * int(porcentaje / 5)
        print(f"    {tipo.capitalize():<15}: {cantidad:>3} ({porcentaje:>5.1f}%)")
    
    print("\n🌍 Distribución por generación:")
    for gen, cantidad in sorted(generaciones.items()):
        porcentaje = (cantidad / total) * 100
        #barra = "█" * int(porcentaje / 5)
        print(f"    {gen:<20}: {cantidad:>3} ({porcentaje:>5.1f}%)")
    
    print("="*70 + "\n")


# Carga Automática
def iniciar_sistema():
    """
    Precarga automática de Pokémon al iniciar el sistema.
    """
    precargar_pokemon()