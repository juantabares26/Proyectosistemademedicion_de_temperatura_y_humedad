# main.py
from errores import ejecutar_sin_cortes
from sistema import iniciar_monitoreo
from interfaz import VentanaPrincipal

if __name__ == "__main__":
    ejecutar_sin_cortes(iniciar_monitoreo)
    app = VentanaPrincipal()
    app.mainloop()