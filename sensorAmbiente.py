class SensorAmbiental:
    def leer_mediciones(self):
        temperatura = float(input("Temperatura ambiental (°C): "))
        humedad = float(input("Humedad relativa (%): "))

        return self.validar_mediciones(temperatura, humedad)

    def validar_mediciones(self, temperatura, humedad):
        if not  -50 <= temperatura <= 80:
            raise ValueError("La temperatura ingresada no es válida.")

        if not 0 <= humedad <= 100:
            raise ValueError("La humedad debe estar entre 0 y 100 %.")

        return {
            "temperatura": temperatura,
            "humedad": humedad
        }