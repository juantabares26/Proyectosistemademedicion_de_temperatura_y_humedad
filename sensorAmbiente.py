import random

class SensorAmbiental:
    def leer_mediciones(self):
        # Simulamos una temperatura entre 10 y 35 grados con 1 decimal
        temperatura = round(random.uniform(10.0, 65.0), 1)
        # Simulamos humedad entre 20 y 85 por ciento con 1 decimal
        humedad = round(random.uniform(20.0, 85.0), 1)

        return self.validar_mediciones(temperatura, humedad)

    def validar_mediciones(self, temperatura, humedad):
        if not -50 <= temperatura <= 80:
            raise ValueError("La temperatura simulada no es válida.")

        if not 0 <= humedad <= 100:
            raise ValueError("La humedad simulada debe estar entre 0 y 100 %.")

        return {
            "temperatura": temperatura,
            "humedad": humedad
        }