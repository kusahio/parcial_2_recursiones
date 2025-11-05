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
    try:
        # Validar que ambos parámetros sean strings
        if not isinstance(str1, str) or not isinstance(str2, str):
            return 0
        
        # Validar que no estén vacíos
        if not str1 or not str2:
            return 0
        
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
        
        # Validar división por cero
        if max_len == 0:
            return 0
        
        similitud = ((max_len - distancia) / max_len) * 100
        
        return similitud
        
    except (TypeError, ValueError) as e:
        print(f"\nAVISO: Error al calcular similitud: {e}")
        return 0
    except Exception as e:
        print(f"\nAVISO: Error inesperado en cálculo de similitud: {e}")
        return 0


def buscar_csv_recursivo(ruta):
    """
    Busca archivos CSV de forma recursiva en una estructura de directorios.
    
    Args:
        ruta: Directorio raíz desde donde buscar
    
    Returns:
        bool: True si encuentra al menos un archivo CSV
    """
    try:
        # Validar que la ruta sea un string
        if not isinstance(ruta, str):
            return False
        
        # Validar que la ruta no esté vacía
        if not ruta or not ruta.strip():
            return False
        
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
            print(f"\nAVISO: Sin permisos para acceder a: {ruta}")
            return False
        except OSError as e:
            print(f"\nAVISO: Error al listar directorio {ruta}: {e}")
            return False
        
        # Validar que elementos sea una lista
        if not isinstance(elementos, list):
            return False
        
        for elemento in elementos:
            try:
                ruta_completa = os.path.join(ruta, elemento)
                
                # Si es un archivo CSV, retornar True
                if os.path.isfile(ruta_completa) and elemento.endswith('.csv'):
                    return True
                
                # Si es un directorio, buscar recursivamente
                if os.path.isdir(ruta_completa):
                    if buscar_csv_recursivo(ruta_completa):
                        return True
            except (OSError, Exception) as e:
                # Continuar con el siguiente elemento si hay error
                continue
        
        return False
        
    except Exception as e:
        print(f"\nAVISO: Error inesperado en búsqueda recursiva: {e}")
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
    try:
        # Validar que termino_busqueda sea un string
        if not isinstance(termino_busqueda, str):
            print("\nAVISO: El término de búsqueda debe ser un texto")
            return []
        
        # Limpiar y validar el término
        termino_busqueda = termino_busqueda.strip()
        
        if not termino_busqueda:
            print("\nAVISO: El término de búsqueda no puede estar vacío")
            return []
        
        # Validar longitud mínima
        if len(termino_busqueda) < 3:
            print("Debes ingresar al menos 3 caracteres para buscar.\n")
            return []
        
        # Validar umbral de similitud
        if not isinstance(umbral_similitud, (int, float)):
            print("\nAVISO: Umbral inválido, usando 60 por defecto")
            umbral_similitud = 60
        
        # Asegurar que el umbral esté en rango válido
        umbral_similitud = max(0, min(100, umbral_similitud))
        
        # Verificar que exista la Pokédex usando función recursiva
        if not buscar_csv_recursivo("pokedex"):
            print("No hay datos en la Pokédex.\n")
            return []
        
        # Leer todos los Pokémon
        datos = leer_recursivo("pokedex")
        
        if not datos:
            print("No hay Pokémon guardados.\n")
            return []
        
        # Validar que datos sea una lista
        if not isinstance(datos, list):
            print("\nAVISO: Formato de datos inválido")
            return []
        
        # Calcular similitud para cada Pokémon
        resultados = []
        for pokemon in datos:
            try:
                # Validar que pokemon sea un diccionario
                if not isinstance(pokemon, dict):
                    continue
                
                nombre = pokemon.get("nombre", "")
                
                # Validar que el nombre sea válido
                if not nombre or not isinstance(nombre, str):
                    continue
                
                similitud = calcular_similitud(termino_busqueda, nombre)
                
                # Solo incluir si cumple el umbral
                if similitud >= umbral_similitud:
                    resultados.append((pokemon, similitud))
                    
            except Exception as e:
                # Continuar con el siguiente pokémon si hay error
                continue
        
        # Ordenar por similitud descendente (mayor similitud primero)
        try:
            resultados.sort(key=lambda x: x[1], reverse=True)
        except (TypeError, ValueError) as e:
            print(f"\nAVISO: Error al ordenar resultados: {e}")
        
        return resultados
        
    except Exception as e:
        print(f"\nAVISO: Error inesperado en búsqueda por similitud: {e}")
        return []


def mostrar_resultados_busqueda(termino_busqueda, umbral=60):
    """
    Muestra los resultados de búsqueda por similitud con paginación.
    
    Args:
        termino_busqueda: Término a buscar
        umbral: Umbral de similitud mínima (default: 60)
    """
    try:
        # Validar entrada
        if not isinstance(termino_busqueda, str):
            print("\nAVISO: El término de búsqueda debe ser texto")
            return
        
        termino_busqueda = termino_busqueda.strip()
        
        if not termino_busqueda:
            print("\nAVISO: El término de búsqueda no puede estar vacío")
            return
        
        # Validar umbral
        if not isinstance(umbral, (int, float)):
            umbral = 60
        
        umbral = max(0, min(100, umbral))
        
        print(f"\nBuscando Pokémon similares a '{termino_busqueda}'...")
        
        # Obtener resultados
        resultados = buscar_pokemon_por_similitud(termino_busqueda, umbral)
        
        # Si no hay resultados
        if not resultados:
            print(f"\nNo se encontraron Pokémon similares a '{termino_busqueda}'.")
            print("Intenta con:")
            print("   • Otro término de búsqueda")
            print("   • Al menos 3 caracteres")
            print("   • Verificar la ortografía\n")
            return
        
        # Validar que resultados sea una lista
        if not isinstance(resultados, list):
            print("\nAVISO: Formato de resultados inválido")
            return
        
        # Extraer solo los pokémon (sin el porcentaje de similitud)
        pokemon_list = []
        for item in resultados:
            try:
                if isinstance(item, tuple) and len(item) >= 1:
                    pokemon_list.append(item[0])
            except Exception:
                continue
        
        if not pokemon_list:
            print(f"\nNo se pudieron procesar los resultados de búsqueda\n")
            return
        
        # Mostrar con paginador
        paginar_pokemon(
            resultados=pokemon_list,
            pokemon_por_pagina=10,
            titulo=f"🔍 RESULTADOS DE BÚSQUEDA: '{termino_busqueda.upper()}'\n{len(resultados)} coincidencia(s) encontrada(s)",
            tipo_formato='completo'
        )
        
    except KeyboardInterrupt:
        print("\n\n[Aviso] Búsqueda cancelada por el usuario")
    except Exception as e:
        print(f"\nAVISO: Error inesperado al mostrar resultados: {e}")