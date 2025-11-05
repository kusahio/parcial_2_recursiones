from funciones.crud import agregar_pokemon, mostrar_todos, buscar_pokemon, editar_pokemon, borrar_pokemon, estadisticas
from funciones.carga_automatica import precargar_pokemon
from funciones.filtros import filtrar_por_generacion, filtrar_por_tipo
from funciones.menu import menu


def main():
    """
    Función principal que ejecuta el sistema de Pokédex.
    Maneja el ciclo principal del menú y las excepciones globales.
    """
    try:
        # Precarga automática al iniciar
        print("\n" + "="*70)
        print("Iniciando Pokédex")
        print("="*70)
        
        precargar_pokemon()
        
        # Ciclo principal del menú
        while True:
            try:
                opcion = menu()
                
                # Validar que se ingresó algo
                if not opcion:
                    print("\nAVISO: Debes seleccionar una opción.\n")
                    continue
                
                # Validar que sea un número
                if not opcion.strip().isdigit():
                    print("\nAVISO: Opción inválida. Ingresa un número del 1 al 9.\n")
                    continue
                
                opcion_int = int(opcion.strip())
                
                # Validar rango de opciones
                if opcion_int < 1 or opcion_int > 9:
                    print("\nAVISO: Opción inválida. Selecciona un número entre 1 y 9.\n")
                    continue

                match opcion_int:
                    case 1:
                        agregar_pokemon()
                    case 2:
                        mostrar_todos()
                    case 3:
                        buscar_pokemon()
                    case 4:
                        filtrar_por_generacion()
                    case 5:
                        filtrar_por_tipo()
                    case 6:
                        editar_pokemon()
                    case 7:
                        borrar_pokemon()
                    case 8:
                        estadisticas()
                    case 9:
                        print("\n" + "="*70)
                        print("CERRANDO SISTEMA POKÉDEX")
                        print("="*70)
                        print("\n✓ Cerrando sesión de Pokédex...")
                        print("✓ Apagando Pokédex......")
                        print("✓ Proceso de Pokédex finalizado.........\n")
                        break
                    case _:
                        print("\nAVISO: Opción inválida, intenta de nuevo.\n")
                        
            except ValueError as e:
                print(f"\n[Error] Valor inválido ingresado: {e}\n")
                continue
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("INTERRUPCIÓN DETECTADA")
                print("="*70)
                confirmacion = input("\n¿Deseas salir del sistema? (s/n): ").strip().lower()
                if confirmacion == 's':
                    print("\n✓ Saliendo del sistema Pokédex...\n")
                    break
                else:
                    print("\n✓ Continuando con el sistema...\n")
                    continue
            except Exception as e:
                print(f"\n[Error] Error inesperado en el menú: {e}")
                print("Continuando con el sistema...\n")
                continue
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("SISTEMA INTERRUMPIDO POR EL USUARIO")
        print("="*70)
        print("\n✓ Saliendo del sistema Pokédex...\n")
    
    except ImportError as e:
        print("\n" + "="*70)
        print("ERROR CRÍTICO")
        print("="*70)
        print(f"\n[Error Fatal] No se pudieron importar los módulos necesarios: {e}")
        print("Verifica que todos los archivos del sistema estén presentes.\n")
    
    except Exception as e:
        print("\n" + "="*70)
        print("ERROR CRÍTICO")
        print("="*70)
        print(f"\n[Error Fatal] Error inesperado al iniciar el sistema: {e}")
        print("El sistema se cerrará de forma segura.\n")
    
    finally:
        # Este bloque siempre se ejecuta al salir
        print("="*70)
        print("Gracias por usar el sistema Pokédex")
        print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[Error Fatal] El sistema no pudo iniciarse: {e}\n")