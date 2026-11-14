from animal import Animal


class Gato(Animal):
    def __init__(self, nombre, peso, edad):
        super().__init__(nombre, peso, edad)

    def tipo_animal(self):
        return "gato"

    def rango_ideal(self):
        return {
            "temperatura": (20, 26),
            "humedad": (30, 70)
        }