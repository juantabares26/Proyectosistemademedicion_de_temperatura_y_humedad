class EvaluadorAmbiente:
    def evaluar_temperatura(self, temperatura, rango):
        minimo, maximo = rango

        if temperatura < minimo:
            return "BAJA"

        if temperatura > maximo:
            return "ALTA"

        return "ADECUADA"

    def evaluar_humedad(self, humedad, rango):
        minimo, maximo = rango

        if humedad < minimo:
            return "BAJA"

        if humedad > maximo:
            return "ALTA"

        return "ADECUADA"

    def evaluar_ambiente(self, animal, mediciones):
        rangos = animal.rango_ideal()

        estado_temperatura = self.evaluar_temperatura(
            mediciones["temperatura"],
            rangos["temperatura"]
        )

        estado_humedad = self.evaluar_humedad(
            mediciones["humedad"],
            rangos["humedad"]
        )

        return {
            "temperatura": estado_temperatura,
            "humedad": estado_humedad,
            "apto": (
                estado_temperatura == "ADECUADA"
                and estado_humedad == "ADECUADA"
            )
        }