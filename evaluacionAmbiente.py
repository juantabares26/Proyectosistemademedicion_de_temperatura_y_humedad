class EvaluadorAmbiente:
    def evaluar_ambiente(self, animal, mediciones):
        # Obtenemos los rangos (desde el Excel a través de la clase Perro o Gato)
        rangos = animal.rango_ideal()

        # Obtenemos las mediciones actuales del sensor
        temp_actual = mediciones["temperatura"]
        hum_actual = mediciones["humedad"]
        t_min = rangos.get("t_min", 15)
        t_max = rangos.get("t_max", 30)
        h_min = rangos.get("h_min", 30)
        h_max = rangos.get("h_max", 70)

        # 1. Evaluar la Temperatura
        if t_min <= temp_actual <= t_max:
            eval_temp = "Normal"
            temp_apto = True
        else:
            eval_temp = "¡Alta!" if temp_actual > t_max else "¡Baja!"
            temp_apto = False

        # 2. Evaluar la Humedad
        if h_min <= hum_actual <= h_max:
            eval_hum = "Normal"
            hum_apto = True
        else:
            eval_hum = "¡Alta!" if hum_actual > h_max else "¡Baja!"
            hum_apto = False

        # 3. Empaquetar los resultados para que la interfaz los muestre
        return {
            "temperatura": eval_temp,
            "humedad": eval_hum,
            "apto": temp_apto and hum_apto
        }