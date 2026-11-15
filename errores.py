def ejecutar_sin_cortes(funcion_principal):
    """
    Atrapa los errores del sistema y reinicia la función principal
    en lugar de terminar el programa abruptamente.
    """
    while True:
        try:
            funcion_principal()
            break

        except (ValueError, TypeError) as error:
            print(f"\n[ERROR EN LOS DATOS]: {error}")
            print("=> Reiniciando el programa...\n")

        except OSError as error:
            print(f"\n[ERROR AL ACCEDER A LOS ARCHIVOS]: {error}")
            print("=> Reiniciando el programa...\n")

        except Exception as error:
            print(f"\n[ERROR INESPERADO]: Se produjo un error -> {error}")
            print("=> Reiniciando el programa...\n")