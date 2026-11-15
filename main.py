# main.py
from errores import ejecutar_sin_cortes
from sistema import iniciar_monitoreo

if __name__ == "__main__":
    # Pasamos la lógica del sistema a nuestra función que evita los cortes
    ejecutar_sin_cortes(iniciar_monitoreo)