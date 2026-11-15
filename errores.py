import sys

def ejecutar_sin_cortes(funcion_principal):
    """
    Atrapa los errores del sistema y reinicia la función principal,
    manteniendo el programa en un bucle continuo hasta que el usuario decida salir.
    """
    while True:
        try:
            funcion_principal()

            # Al finalizar con éxito, en lugar de romper el ciclo, pausamos y preguntamos:
            print("\n" + "=" * 40)
            opcion = input(
                "[SISTEMA]: Monitoreo finalizado. Presione ENTER para volver al menú principal, o escriba 'salir' para cerrar: ").strip().lower()

            if opcion == 'salir':
                print("\nCerrando el sistema... ¡Hasta luego!\n")
                sys.exit(0)  # Cierra el programa limpiamente

            # Si presiona ENTER (o cualquier otra cosa), el 'while True' vuelve a iniciar

        except (ValueError, TypeError) as error:
            print(f"\n[ERROR EN LOS DATOS]: {error}")
            print("=> Reiniciando el menú principal...\n")

        except OSError as error:
            print(f"\n[ERROR AL ACCEDER A LOS ARCHIVOS]: {error}")
            print("=> Reiniciando el menú principal...\n")

        except KeyboardInterrupt:
            # Por si el usuario presiona Ctrl+C en la consola
            print("\n\n[SISTEMA]: Programa interrumpido por el usuario. Cerrando...\n")
            break

        except SystemExit:
            # Permite que el sys.exit(0) de arriba funcione correctamente sin ser atrapado como error
            break

        except Exception as error:
            print(f"\n[ERROR INESPERADO]: Se produjo un error -> {error}")
            print("=> Reiniciando el programa...\n")