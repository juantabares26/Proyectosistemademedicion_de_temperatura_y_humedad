from animal import Animal


class Perro(Animal):
    def __init__(self, nombre, peso, edad):
        super().__init__(nombre, peso, edad)

    def tipo_animal(self):
        return "perro"

    def rango_ideal(self):
        return {
            "temperatura": (18, 26),
            "humedad": (30, 70)
        }