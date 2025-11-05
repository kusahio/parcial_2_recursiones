import os
from .persistencia import guardar_pokemon, leer_recursivo, modificar_pokemon, eliminar_pokemon
from api.api_pokemon import obtener_pokemon
from .carga_automatica import precargar_pokemon


# CREATE
def agregar_pokemon():
    """
    Agrega un Pokémon a la Pokédex.
    Solo pide el nombre, la generación se detecta automáticamente.
    """
    nombre = input("Nombre del Pokémon: ").strip().lower()
    
    if not nombre:
        print("❌ Debes ingresar un nombre válido.\n")
        return
    
    print(f"\n🔍 Buscando '{nombre}' en la PokéAPI...")
    
    pokemon = obtener_pokemon(nombre)  # YA NO necesita el parámetro generacion
    if pokemon:
        guardar_pokemon(pokemon)
        print(f"\n✅ {nombre.capitalize()} agregado correctamente a la Pokédex.\n")
    else:
        print(f"\n❌ No se pudo agregar '{nombre}'. Verifica el nombre e intenta nuevamente.\n")


# READ
def mostrar_todos():
    if not os.path.exists("pokedex"):
        print("📭 No hay datos aún.\n")
        return

    datos = leer_recursivo("pokedex")
    if not datos:
        print("📭 No hay Pokémon guardados.\n")
        return

    print("\n" + "="*80)
    print("📚 LISTA GLOBAL DE POKÉMON EN LA POKÉDEX")
    print("="*80)
    
    for i, d in enumerate(datos, 1):
        print(f"\n{i}. {d['nombre'].upper()}")
        print(f"   └─ Tipo: {d['tipo']} | Generación: {d['generacion']}")
        print(f"   └─ Peso: {d['peso']} | Altura: {d['altura']}")
        print(f"   └─ Experiencia base: {d.get('base_experience', 'N/A')}")
        if d.get('habilidades'):
            print(f"   └─ Habilidades: {d['habilidades']}")

    print("\n" + "="*80)
    print(f"📊 Total: {len(datos)} Pokémon registrados")
    print("="*80 + "\n")


# UPDATE
def editar_pokemon():
    nombre = input("Nombre del Pokémon a modificar: ").strip().lower()
    
    if not nombre:
        print("❌ Debes ingresar un nombre válido.\n")
        return
    
    print("\nCampos modificables:")
    print("  - peso")
    print("  - altura")
    print("  - habilidades")
    print("  - areas_encuentro")
    print("  - base_experience")
    
    campo = input("\nCampo a modificar: ").strip().lower()
    nuevo_valor = input("Nuevo valor: ").strip()
    
    if modificar_pokemon(nombre, campo, nuevo_valor):
        print(f"\n✅ {nombre.capitalize()} modificado correctamente.\n")
    else:
        print(f"\n❌ No se pudo modificar '{nombre}'.\n")


# DELETE
def borrar_pokemon():
    nombre = input("Nombre del Pokémon a eliminar: ").strip().lower()
    
    if not nombre:
        print("❌ Debes ingresar un nombre válido.\n")
        return
    
    confirmacion = input(f"⚠️  ¿Estás seguro de eliminar a {nombre.capitalize()}? (s/n): ").lower()
    
    if confirmacion == 's':
        if eliminar_pokemon(nombre):
            print(f"\n✅ {nombre.capitalize()} eliminado correctamente.\n")
        else:
            print(f"\n❌ Pokémon '{nombre}' no encontrado.\n")
    else:
        print("\n❌ Eliminación cancelada.\n")


# 📊 ESTADÍSTICAS
def estadisticas():
    if not os.path.exists("pokedex"):
        print("📭 No hay datos registrados.\n")
        return

    datos = leer_recursivo("pokedex")
    if not datos:
        print("📭 No hay Pokémon guardados.\n")
        return

    total = len(datos)
    
    # Calcular promedios
    pesos = [float(p["peso"]) for p in datos if p.get("peso", "").replace(".", "").isdigit()]
    alturas = [float(p["altura"]) for p in datos if p.get("altura", "").replace(".", "").isdigit()]
    
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

    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS GLOBALES DE LA POKÉDEX")
    print("="*60)
    print(f"\n📈 Total de Pokémon registrados: {total}")
    print(f"⚖️  Peso promedio: {promedio_peso:.2f}")
    print(f"📏 Altura promedio: {promedio_altura:.2f}")
    
    print("\n🎨 Distribución por tipo:")
    for tipo, cantidad in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        print(f"   └─ {tipo.capitalize()}: {cantidad}")
    
    print("\n🌍 Distribución por generación:")
    for gen, cantidad in sorted(generaciones.items()):
        print(f"   └─ {gen}: {cantidad}")
    
    print("="*60 + "\n")


# CARGA AUTOMÁTICA AL INICIO
def iniciar_sistema():
    precargar_pokemon()