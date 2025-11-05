def formatear_pokemon(pokemon, index, tipo_formato='simple'):
    '''
    Formatea la información de un Pokémon para mostrar en pantalla.
    
    Args:
        pokemon (dict): Diccionario con información del Pokémon
        index (int): Número de índice a mostrar
        tipo_formato (str): Tipo de formato: 'simple', 'detallado', 'completo'
    
    Ejemplos:
        formatear_pokemon({'nombre': 'pikachu', 'tipo': 'electric'}, 1, 'simple')
        → ' 1. PIKACHU - Tipo: Electric'
        
        formatear_pokemon({'nombre': 'charizard', 'tipo': 'fire', ...}, 1, 'completo')
        → Formato completo con todos los detalles
    '''
    try:
        # Formato completo: muestra toda la información del Pokémon
        if tipo_formato == 'completo':
            habilidades = pokemon.get('habilidades', 'N/A')
            return (f' {index}. {pokemon["nombre"].upper()}\n'
                    f'   ├─ ID: #{pokemon.get("id", "N/A")}\n'
                    f'   ├─ Tipo: {pokemon["tipo"].capitalize()}\n'
                    f'   ├─ Generación: {pokemon["generacion"]}\n'
                    f'   ├─ Peso: {pokemon["peso"]} | Altura: {pokemon["altura"]}\n'
                    f'   ├─ Experiencia base: {pokemon.get("base_experience", "N/A")}\n'
                    f'   └─ Habilidades: {habilidades}')

        # Formato detallado: información resumida en 3 líneas
        elif tipo_formato == 'detallado':
            return (f' {index}. {pokemon["nombre"].upper()}\n'
                    f'   Tipo: {pokemon["tipo"].capitalize()} | Generación: {pokemon["generacion"]}\n'
                    f'   Peso: {pokemon["peso"]} | Altura: {pokemon["altura"]} | EXP: {pokemon.get("base_experience", "N/A")}')

        # Formato simple (por defecto): una sola línea
        else:
            return (f' {index}. {pokemon["nombre"].upper()} - '
                    f'Tipo: {pokemon["tipo"].capitalize()} | '
                    f'Generación: {pokemon["generacion"]}')

    # Si falta alguna clave esperada en el diccionario
    except KeyError as e:
        return f' {index}. Error: Falta el campo {e}'

    # Si se reciben tipos erróneos o hay problemas de formato
    except (TypeError, ValueError) as e:
        return f' {index}. Error de formato: {e}'


def mostrar_pagina_pokemon(pokemon_lista, inicio_idx, titulo_pagina, tipo_formato='simple'):
    '''
    Función auxiliar para mostrar una página de Pokémon.
    
    Args:
        pokemon_lista (list): Lista de Pokémon a mostrar
        inicio_idx (int): Índice inicial para la numeración visual
        titulo_pagina (str): Título a mostrar en el encabezado
        tipo_formato (str): Tipo de formato a usar en formatear_pokemon
    '''
    # Encabezado visual de la página
    print('\n' + '=' * 80)
    print(f'{titulo_pagina}')
    print('=' * 80, '\n')

    # Recorre y muestra cada Pokémon usando el formateador elegido
    for i, pokemon in enumerate(pokemon_lista, start=inicio_idx):
        print(formatear_pokemon(pokemon, i, tipo_formato))

    # Separador inferior
    print('\n' + '-' * 80)


def paginar_pokemon(resultados, pokemon_por_pagina=10, titulo='Resultados', tipo_formato='completo'):
    '''
    Muestra una lista de Pokémon con sistema de paginación interactivo.
    
    Args:
        resultados (list): Lista de diccionarios con datos de Pokémon
        pokemon_por_pagina (int): Cantidad de Pokémon por página (default: 10)
        titulo (str): Título del listado
        tipo_formato (str): Formato de visualización: 'simple', 'detallado', 'completo'
    
    Controles de navegación:
        - Enter: Avanza a la siguiente página (o vuelve a la primera si está en la última)
        - A: Retrocede a la página anterior
        - [Número]: Salta a una página específica
        - S: Sale de la paginación
    
    Ejemplo de uso:
        pokemon_list = leer_recursivo("pokedex")
        paginar_pokemon(pokemon_list, pokemon_por_pagina=10, titulo='MI POKÉDEX', tipo_formato='completo')
    '''
    try:
        # Verificar si hay resultados para mostrar
        if not resultados:
            print('\nNo hay Pokémon para mostrar.')
            return

        # Validar que pokemon_por_pagina sea un entero positivo; si no, usar 10 por defecto
        if not isinstance(pokemon_por_pagina, int) or pokemon_por_pagina <= 0:
            pokemon_por_pagina = 10

        # Total de elementos y cálculo de páginas (redondeo hacia arriba)
        total_pokemon = len(resultados)
        total_paginas = (total_pokemon + pokemon_por_pagina - 1) // pokemon_por_pagina

        # Caso simple: 10 o menos resultados → una sola pantalla y volver
        if total_pokemon <= 10:
            titulo_completo = f'{titulo}\nMostrando {total_pokemon} Pokémon'
            mostrar_pagina_pokemon(resultados, 1, titulo_completo, tipo_formato)
            input('\nPresione Enter para continuar...')
            return

        # Paginación interactiva para más de 10 resultados
        pagina_actual = 1
        while True:
            # Determina el rango (slice) de la página actual
            inicio = (pagina_actual - 1) * pokemon_por_pagina
            fin = min(inicio + pokemon_por_pagina, total_pokemon)
            pokemon_pagina = resultados[inicio:fin]

            # Muestra la página actual con título informativo
            titulo_pagina = (
                f'{titulo}\n'
                f'Página {pagina_actual} de {total_paginas}\n'
                f'Mostrando {inicio + 1}-{fin} de {total_pokemon} Pokémon'
            )
            mostrar_pagina_pokemon(pokemon_pagina, inicio + 1, titulo_pagina, tipo_formato)

            # Construcción de controles visibles según el contexto
            controles = []
            
            # Enter (siguiente / volver a 1 en última)
            if pagina_actual < total_paginas:
                controles.append('Enter = Siguiente')
            else:
                controles.append('Enter = Volver a página 1')
            
            # A (Anterior) si no estamos en la primera
            if total_paginas >= 2 and pagina_actual > 1:
                controles.append('A = Anterior')
            
            # [Número] para ir a una página específica (si hay más de 2 páginas)
            if total_paginas > 2:
                controles.append('[Número] = Ir a página')
            
            # S (Salir) disponible si hay 2 o más páginas
            if total_paginas >= 2:
                controles.append('S = Salir')

            # Muestra controles y lee la opción del usuario
            print(' | '.join(controles))
            print('-' * 80)
            opcion = input('\nSeleccione una opción: ').lower().strip()

            # Opción salir (con 2 o más páginas)
            if opcion == 's' and total_paginas >= 2:
                break

            # Ir a la página anterior (si es posible)
            elif opcion == 'a' and pagina_actual > 1:
                pagina_actual -= 1
            elif opcion == 'a' and pagina_actual == 1:
                # Ya no se puede ir más atrás
                print('\nYa estás en la primera página.')
                input('Presione Enter para continuar...')

            # Enter: avanzar; si estamos en la última, volver a la primera
            elif opcion == '':
                if pagina_actual < total_paginas:
                    pagina_actual += 1
                else:
                    pagina_actual = 1

            # Número: ir a una página específica (solo si hay > 2 páginas)
            elif opcion.isdigit() and total_paginas > 2:
                pagina_destino = int(opcion)
                if 1 <= pagina_destino <= total_paginas:
                    pagina_actual = pagina_destino
                else:
                    print(f'\nPágina inválida. Debe estar entre 1 y {total_paginas}.')
                    input('Presione Enter para continuar...')

            # Opción no reconocida: muestra ayuda contextual
            else:
                print(f'\nOpción "{opcion}" no reconocida.')
                opciones_validas = ['Enter']
                if total_paginas >= 2 and pagina_actual > 1:
                    opciones_validas.append('A (anterior)')
                if total_paginas > 2:
                    opciones_validas.append('[número] (ir a página)')
                if total_paginas >= 2:
                    opciones_validas.append('S (salir)')
                print(f'Opciones válidas: {", ".join(opciones_validas)}')
                input('Presione Enter para continuar...')

    # Permite interrumpir con Ctrl+C de manera limpia
    except KeyboardInterrupt:
        print('\n\nAVISO: Paginación interrumpida por el usuario')

    # Cualquier otro error inesperado se informa sin romper la app
    except Exception as e:
        print(f'\nAVISO: Error inesperado en el paginador - {e}')