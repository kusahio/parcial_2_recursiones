import os
from .persistencia import leer_recursivo
from .paginador import paginar_pokemon


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
    try:
        # Validar que datos sea una lista
        if not isinstance(datos, list):
            return []
        
        # Caso base: lista vacía
        if not datos:
            return []
        
        # Validar criterio y valor
        if not isinstance(criterio, str) or not isinstance(valor, str):
            return []
        
        if not criterio.strip() or not valor.strip():
            return []
        
        # Tomar primer elemento y el resto
        primero = datos[0]
        resto = datos[1:]
        
        # Validar que el primer elemento sea un diccionario
        if not isinstance(primero, dict):
            # Omitir elemento inválido y continuar
            return filtrar_por_criterio_recursivo(resto, criterio, valor)
        
        # Verificar si el primer elemento cumple el criterio
        valor_campo = primero.get(criterio, "")
        
        # Validar que el valor del campo sea un string
        if not isinstance(valor_campo, str):
            valor_campo = str(valor_campo)
        
        if valor_campo.lower() == valor.lower():
            # Incluir el elemento actual y continuar recursivamente
            return [primero] + filtrar_por_criterio_recursivo(resto, criterio, valor)
        else:
            # Omitir el elemento actual y continuar recursivamente
            return filtrar_por_criterio_recursivo(resto, criterio, valor)
            
    except RecursionError:
        print("\nAVISO: Límite de recursión alcanzado")
        return []
    except Exception as e:
        print(f"\nAVISO: Error en filtro recursivo: {e}")
        return []


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
    try:
        # Validar que datos sea una lista
        if not isinstance(datos, list):
            return set()
        
        # Validar que campo sea un string
        if not isinstance(campo, str) or not campo.strip():
            return set()
        
        # Inicializar set en primera llamada
        if valores_acumulados is None:
            valores_acumulados = set()
        
        # Validar que valores_acumulados sea un set
        if not isinstance(valores_acumulados, set):
            valores_acumulados = set()
        
        # Caso base: lista vacía
        if not datos:
            return valores_acumulados
        
        # Validar que el primer elemento sea un diccionario
        if isinstance(datos[0], dict):
            valor = datos[0].get(campo, "desconocido")
            
            # Validar que el valor sea un string
            if isinstance(valor, str) and valor.strip():
                valores_acumulados.add(valor)
        
        # Paso recursivo: continuar con el resto
        return obtener_valores_unicos_recursivo(datos[1:], campo, valores_acumulados)
        
    except RecursionError:
        print("\nAVISO: Límite de recursión alcanzado")
        return valores_acumulados if valores_acumulados else set()
    except Exception as e:
        print(f"\nAVISO: Error al obtener valores únicos: {e}")
        return valores_acumulados if valores_acumulados else set()


def mostrar_pokemon_filtrados(pokemon_lista, titulo_filtro):
    """
    Muestra una lista de Pokémon filtrados con paginación.
    
    Args:
        pokemon_lista: Lista de Pokémon a mostrar
        titulo_filtro: Título descriptivo del filtro aplicado
    """
    try:
        # Validar que pokemon_lista sea una lista
        if not isinstance(pokemon_lista, list):
            print(f"\nAVISO: Error en los datos filtrados\n")
            return
        
        if not pokemon_lista:
            print(f"\nAVISO: No se encontraron Pokémon con el filtro: {titulo_filtro}\n")
            return
        
        # Validar titulo_filtro
        if not isinstance(titulo_filtro, str):
            titulo_filtro = "Resultados filtrados"
        
        # Usar el paginador para mostrar los resultados
        paginar_pokemon(
            resultados=pokemon_lista,
            pokemon_por_pagina=10,
            titulo=titulo_filtro,
            tipo_formato='completo'
        )
        
    except Exception as e:
        print(f"\nAVISO: Error al mostrar Pokémon filtrados: {e}")


def filtrar_por_generacion():
    """
    Filtra y muestra Pokémon por generación usando recursión y paginación.
    """
    try:
        if not os.path.exists("pokedex"):
            print("\nAVISO: No hay datos en la Pokédex.\n")
            return
        
        # Leer todos los Pokémon
        datos = leer_recursivo("pokedex")
        
        if not datos:
            print("\nAVISO: No hay Pokémon guardados.\n")
            return
        
        # Validar que datos sea una lista
        if not isinstance(datos, list):
            print("\nAVISO: Formato de datos inválido.\n")
            return
        
        # Obtener generaciones disponibles usando recursión
        generaciones = sorted(obtener_valores_unicos_recursivo(datos, "generacion"))
        
        # Validar que se obtuvieron generaciones
        if not generaciones:
            print("\nAVISO: No se pudieron obtener las generaciones disponibles.\n")
            return
        
        print("\n" + "="*60)
        print("Filtrar por generación")
        print("="*60)
        print("\nGeneraciones disponibles:")
        
        for i, gen in enumerate(generaciones, 1):
            try:
                # Contar cuántos Pokémon hay de esta generación
                cantidad = len(filtrar_por_criterio_recursivo(datos, "generacion", gen))
                print(f"  {i}. {gen} ({cantidad} Pokémon)")
            except Exception:
                continue
        
        print(f"  {len(generaciones) + 1}. Volver al menú principal")
        
        opcion = input("\nSelecciona una generación: ").strip()
        
        # Validar que la opción no esté vacía
        if not opcion:
            print("\nAVISO: Debes seleccionar una opción.\n")
            return
        
        # Validar que sea un número
        if not opcion.isdigit():
            print("\nAVISO: Opción inválida.\n")
            return
        
        opcion_int = int(opcion)
        
        # Validar rango
        if opcion_int < 1 or opcion_int > len(generaciones) + 1:
            print("\nAVISO: Opción fuera de rango.\n")
            return
        
        if opcion_int == len(generaciones) + 1:
            return
        
        if 1 <= opcion_int <= len(generaciones):
            gen_seleccionada = generaciones[opcion_int - 1]
            
            # Filtrar usando recursión
            pokemon_filtrados = filtrar_por_criterio_recursivo(datos, "generacion", gen_seleccionada)
            
            # Validar resultados
            if not isinstance(pokemon_filtrados, list):
                print("\nAVISO: Error al filtrar Pokémon.\n")
                return
            
            # Contar cantidad para el título
            cantidad = len(pokemon_filtrados)
            
            # Mostrar resultados con paginación
            mostrar_pokemon_filtrados(
                pokemon_filtrados,
                f"Pokémon de {gen_seleccionada.replace('generation-', 'generación ').upper()} | {cantidad} Pokémon encontrado(s)"
            )
        else:
            print("\nAVISO: Opción inválida.\n")
            
    except KeyboardInterrupt:
        print("\nAVISO: Operación cancelada por el usuario.\n")
    except ValueError as e:
        print(f"\nAVISO: Error de valor: {e}\n")
    except Exception as e:
        print(f"\nAVISO: Error inesperado al filtrar por generación: {e}\n")


def filtrar_por_tipo():
    """
    Filtra y muestra Pokémon por tipo usando recursión y paginación.
    """
    try:
        if not os.path.exists("pokedex"):
            print("\nAVISO: No hay datos en la Pokédex.\n")
            return
        
        # Leer todos los Pokémon
        datos = leer_recursivo("pokedex")
        
        if not datos:
            print("\nAVISO: No hay Pokémon guardados.\n")
            return
        
        # Validar que datos sea una lista
        if not isinstance(datos, list):
            print("\nAVISO: Formato de datos inválido.\n")
            return
        
        # Obtener tipos disponibles usando recursión
        tipos = sorted(obtener_valores_unicos_recursivo(datos, "tipo"))
        
        # Validar que se obtuvieron tipos
        if not tipos:
            print("\nAVISO: No se pudieron obtener los tipos disponibles.\n")
            return
        
        print("\n" + "="*60)
        print("Filtrar por tipo")
        print("="*60)
        print("\nTipos disponibles:")
        
        for i, tipo in enumerate(tipos, 1):
            try:
                # Contar cuántos Pokémon hay de este tipo
                cantidad = len(filtrar_por_criterio_recursivo(datos, "tipo", tipo))
                print(f"  {i}. {tipo.capitalize()} ({cantidad} Pokémon)")
            except Exception:
                continue
        
        print(f"  {len(tipos) + 1}. Volver al menú principal")
        
        opcion = input("\nSelecciona un tipo: ").strip()
        
        # Validar que la opción no esté vacía
        if not opcion:
            print("\nAVISO: Debes seleccionar una opción.\n")
            return
        
        # Validar que sea un número
        if not opcion.isdigit():
            print("\nAVISO: Opción inválida.\n")
            return
        
        opcion_int = int(opcion)
        
        # Validar rango
        if opcion_int < 1 or opcion_int > len(tipos) + 1:
            print("\nAVISO: Opción fuera de rango.\n")
            return
        
        if opcion_int == len(tipos) + 1:
            return
        
        if 1 <= opcion_int <= len(tipos):
            tipo_seleccionado = tipos[opcion_int - 1]
            
            # Filtrar usando recursión
            pokemon_filtrados = filtrar_por_criterio_recursivo(datos, "tipo", tipo_seleccionado)
            
            # Validar resultados
            if not isinstance(pokemon_filtrados, list):
                print("\nAVISO: Error al filtrar Pokémon.\n")
                return
            
            # Contar cantidad para el título
            cantidad = len(pokemon_filtrados)
            
            # Mostrar resultados con paginación
            mostrar_pokemon_filtrados(
                pokemon_filtrados,
                f"Pokémon de tipo {tipo_seleccionado.upper()} | {cantidad} Pokémon encontrado(s)"
            )
        else:
            print("\nAVISO: Opción inválida.\n")
            
    except KeyboardInterrupt:
        print("\nAVISO: Operación cancelada por el usuario.\n")
    except ValueError as e:
        print(f"\nAVISO: Error de valor: {e}\n")
    except Exception as e:
        print(f"\nAVISO: Error inesperado al filtrar por tipo: {e}\n")