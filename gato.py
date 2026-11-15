from animal import Animal
from gestor_razas import GestorRazas

class Gato(Animal):
    def __init__(self, nombre, peso, edad, raza="Genérico"):
        super().__init__(nombre, peso, edad, raza)

    def tipo_animal(self):
        return "gato"

    def rango_ideal(self):
        gestor = GestorRazas()
        rangos = gestor.obtener_rango_raza(self.tipo_animal(), self.get_raza())

        # Red de seguridad
        if rangos is None:
            return gestor.obtener_rango_raza(self.tipo_animal(), "Genérico")

        return rangos